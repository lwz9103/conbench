import dataclasses
import logging
import signal
import threading
import time
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, NewType, Tuple, TypedDict, cast

import pandas as pd
import sqlalchemy
import sqlalchemy.orm

import conbench.metrics
import conbench.util
from conbench.config import Config
from conbench.db import session_maker
from conbench.entities.benchmark_result import (
    BenchmarkResult,
    ui_mean_and_uncertainty,
    ui_rel_sem,
)
from conbench.hacks import get_case_kvpair_strings

# A memory profiler, and a CPU profiler that are both tested to work well
# with the process/threading model used here.
# from filprofiler.api import profile as filprofile
# import yappi


"""
This module implements a job which populates and provides a cache for the N
most recent benchmark results, the tail end. Benchmark result tail-end cache:
BMRT cache.

Central cache data structure are Python dictionaries (with thread-safe(atomic)
set/get operations).
"""

original_sigint_handler = signal.getsignal(signal.SIGINT)
original_sigquit_handler = signal.getsignal(signal.SIGQUIT)

log = logging.getLogger(__name__)


@dataclasses.dataclass
class CacheUpdateMetaInfo:
    newest_result_time_str: str
    oldest_result_time_str: str
    covered_timeframe_days_approx: str  # stringified integer, for UI
    n_results: int


# CPython 3.10/3.11 feature:  dataclass nicely integrated with slots. __slots__
# saves memory: prevents the automatic creation of __dict__ and __weakref__ for
# each instance. See
# https://docs.python.org/3/reference/datamodel.html#object.__slots__
# https://www.trueblade.com/blogs/news/python-3-10-new-dataclass-features
@dataclasses.dataclass(slots=True)
class BMRTBenchmarkResult:
    id: str
    case_id: str
    context_id: str
    run_id: str
    data: List[float]
    svs: float
    svs_type: str
    unit: str
    benchmark_name: str
    started_at: float
    hardware_id: str
    hardware_name: str
    case_text_id: str
    case_dict: Dict[str, str]
    context_dict: Dict
    ui_time_started_at: str
    ui_hardware_short: str
    ui_non_null_sample_count: str
    run_reason: str

    # There is conceptual duplication between the class BenchmarkResult
    # and this class BMRTBenchmarkResult. Fundamentally, it might make sense
    # that we have two types of classes, with distinct values:
    # - one for database abstraction (the 'big instances', mutable, ...)
    # - one for data mangling (small mem footprint, immutable, ...)
    @property
    def ui_mean_and_uncertainty(self) -> str:
        return ui_mean_and_uncertainty(self.data, self.unit)

    @property
    def ui_rel_sem(self) -> Tuple[str, str]:
        return ui_rel_sem(self.data)

    @property
    def started_at_iso(self) -> str:
        """
        Add an ISO timestring on the object so that JavaScript's `new
        Date(input)` can parse this into a tz-aware object.
        """
        return conbench.util.tznaive_dt_to_aware_iso8601_for_api(
            datetime.fromtimestamp(self.started_at)
        )


# Do this for case ID, etc, too.
TBenchmarkName = NewType("TBenchmarkName", str)

# This type is used often. It's the famous 4-tuple defining a timeseries. Or
# maybe turn this into a namedtuple or sth like this. Watch out a bit for mem
# consumption.
Tt4 = Tuple[TBenchmarkName, str, str, str]

# A type for a dictionary: key is 4-tuple defining a time series, and value is
# a pandas dataframe containing the time series (index: pd.DateTimeIndex
# tz-aware, one column: single value summary).
TDict4tdf = Dict[Tt4, pd.DataFrame]
TDict4tlist = Dict[Tt4, List[BMRTBenchmarkResult]]


class CacheDict(TypedDict):
    by_id: Dict[str, BMRTBenchmarkResult]
    by_benchmark_name: Dict[TBenchmarkName, List[BMRTBenchmarkResult]]
    by_case_id: Dict[str, List[BMRTBenchmarkResult]]
    by_4t_df: TDict4tdf
    by_4t_list: TDict4tlist
    meta: CacheUpdateMetaInfo


@dataclasses.dataclass(slots=True)
class ResultTimeseries:
    t4: Tt4
    benchmark_name: str
    df: pd.DataFrame
    bmrlist: List[BMRTBenchmarkResult]


# Think: do work in a child process, provide dictionary via shared memory to
# parent, maybe via https://pypi.org/project/shared-memory-dict/ this is _not_
# as stdlib pickling dict
# https://github.com/luizalabs/shared-memory-dict/issues/10
bmrt_cache: CacheDict = {
    "by_id": {},
    "by_benchmark_name": {},
    "by_case_id": {},
    "by_4t_list": {},
    "by_4t_df": {},
    "meta": CacheUpdateMetaInfo(
        newest_result_time_str="n/a",
        oldest_result_time_str="n/a",
        n_results=0,
        covered_timeframe_days_approx="n/a",
    ),
}

SHUTDOWN = False
_STARTED = False

BMRT_CACHE_SIZE = 0.8 * 10**6
if Config.TESTING:
    # quicker update in testing
    BMRT_CACHE_SIZE = 0.05 * 10**6


# Fetching one million items from a sample DB takes ~1 minute on my machine
# (the `results = Session.scalars(....all())` call takes that long.
def _fetch_and_cache_most_recent_results() -> None:
    # https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker.begin

    # This pattern is weird, see https://github.com/sqlalchemy/sqlalchemy/issues/6519
    # not trivial!
    dbsession = session_maker()
    with dbsession:
        with dbsession.begin():
            _fetch_and_cache_most_recent_results_guts(dbsession)
            # commits transaction, closes session


def _fetch_and_cache_most_recent_results_guts(
    dbsession: sqlalchemy.orm.session.Session,
):
    log.debug(
        "BMRT cache: keys in cache: %s",
        len(bmrt_cache["by_id"]),
    )
    t0 = time.monotonic()

    # Note(JP): process query result rows in a streaming-like fashion in
    # smaller chunks to keep peak memory usage in check. Also see
    # https://docs.sqlalchemy.org/en/20/core/connections.html#using-server-side-cursors-a-k-a-stream-results
    # https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#fetching-large-result-sets-with-yield-per
    # Also fetch hardware from associated Run, so that result.run is in cache,
    # too, and so that result.run.hardware is a quick lookup. Use selectinload
    # for fetching Run data -- "The yield_per execution option is not
    # compatible with “subquery” eager loading loading or “joined” eager
    # loading when using collections. It is potentially compatible with “select
    # in” eager loading , provided the database driver supports multiple,
    # independent cursors." -- seems to result in overall less queries.
    query_statement = (
        sqlalchemy.select(BenchmarkResult)
        .options(sqlalchemy.orm.selectinload(BenchmarkResult.run))
        .order_by(BenchmarkResult.timestamp.desc())
        .limit(int(BMRT_CACHE_SIZE))
    ).execution_options(yield_per=2000)

    # Corresponding to the `yield_per` magic, consume the returned value as an
    # iterator. `all()` would consume all results and would defeat the purpose
    # of the memory-saving exercise. The following line of code does not do
    # much of the work yet; that begins once the iterator is consumed (maybe it
    # fetches the first chunk?).
    result_rows_iterator = dbsession.scalars(query_statement)

    by_id_dict: Dict[str, BMRTBenchmarkResult] = {}
    by_name_dict: Dict[TBenchmarkName, List[BMRTBenchmarkResult]] = defaultdict(list)
    by_case_id_dict: Dict[str, List[BMRTBenchmarkResult]] = defaultdict(list)

    first_result = None
    last_result = None
    for result in result_rows_iterator:  # pylint: disable=E1133
        # Note that the DB might feed us so quickly that this loop body becomes
        # CPU-bound. In that case, given the current deployment model, we
        # starve the other threads (hello, GIL!) that want to process HTTP
        # requests. Pragmatic solution could be to sleep a bit in each loop
        # iteration here (e.g. 0.1 s). We will see. Better would be do do the
        # update from a separate process, and share the outcome via shared mem
        # (e.g. SHM, but anything goes as long as we don't re-serialize).
        # Update: Spread out the CPU work a little more.
        time.sleep(0.0001)

        # Keep track of the first (newest) and last (oldest) result
        # while consuming the iterator. If n=1 they are the same.
        last_result = result
        if first_result is None:
            first_result = result

        # For now: put both, failed and non-failed results into the cache.
        # It would be a nice code simplification to only consider succeeded
        # ones, but then we miss out on reporting about the failed ones.
        # Note: with named types it's here not enough to to # type: ...
        # but an explicit cast is required? perf impact? dunno.
        # Related: https://github.com/python/typing/discussions/1146
        benchmark_name = cast(TBenchmarkName, str(result.case.name))

        # A textual representation of the case permutation. As it is 'complete'
        # it should also work as a proper identifier (like primary key).
        casedict = result.case.to_dict()
        case_text_id = " ".join(get_case_kvpair_strings(casedict))

        bmrrun = result.run

        # Skip results that have not been obtained for the default code branch.
        bmrcommit = bmrrun.commit
        if bmrcommit is None:
            continue

        if not bmrcommit.on_default_branch:
            continue

        bmr = BMRTBenchmarkResult(
            id=str(result.id),
            benchmark_name=benchmark_name,
            started_at=result.timestamp.timestamp(),
            data=result.measurements,
            svs=result.svs,  # float(result.mean) if result.mean else None,
            svs_type=result.svs_type,
            unit=str(result.unit) if result.unit else "n/a",
            hardware_id=str(bmrrun.hardware.id),
            hardware_name=str(bmrrun.hardware.name),
            case_id=str(result.case_id),
            context_id=str(result.context_id),
            run_id=str(result.run_id),
            # These context dictionaries are often the largest part of these
            # BMRTBenchmarkResult object (in terms of memory usage) -- they can
            # be a rather big collection of strings. However, by the nature of
            # the processed data there can be a high degree of duplication
            # across benchmark results. The data source uses a unique
            # constraint (enforced in DB) with an index on the entire
            # dictionary, i.e. use the _same_ object here and assume it may be
            # shared across potentially many BMRTBenchmarkResult objects.
            context_dict=result.context.to_dict(),
            case_text_id=case_text_id,
            case_dict=casedict,
            ui_hardware_short=str(result.ui_hardware_short),
            ui_time_started_at=str(result.ui_time_started_at),
            ui_non_null_sample_count=result.ui_non_null_sample_count,
            run_reason=bmrrun.reason if bmrrun.reason else "n/a",
        )

        # The str() indirections below (and above) are here to quickly make
        # sure that there is no more SQLAlchemy magic associated to objects we
        # store here (no more mapping to columns). Maybe that is not needed
        # but instead of making that experiment I took the quick way.
        by_id_dict[str(result.id)] = bmr
        by_name_dict[benchmark_name].append(bmr)

        # Add a property on the Case object, on the fly.
        # Build the textual representation of this case which should also
        # uniquely / unambiguously define/identify this specific case.
        by_case_id_dict[str(result.case_id)].append(bmr)

    t1 = time.monotonic()

    if len(by_name_dict) == 0:
        log.info("BMRT cache: no results")
        return

    # This helps mypy, too.
    assert first_result
    assert last_result

    # Group all benchmark results into timeseries
    dict4tdf, bmrlist_by_4tuple = _generate_tsdf_per_4tuple(by_name_dict)

    # Mutate the dictionary which is accessed by other threads, do this in a
    # quick fashion -- each of this assignments is atomic (thread-safe), but
    # between those two assignments a thread might perform read access. (minor
    # inconsistency is possible). Of course we can add another lookup
    # indirection layer by assembling a completely new dictionary here and then
    # re-defining the name bmrt_cache.
    bmrt_cache["by_id"] = by_id_dict
    bmrt_cache["by_benchmark_name"] = by_name_dict
    bmrt_cache["by_case_id"] = by_case_id_dict
    bmrt_cache["by_4t_df"] = dict4tdf
    bmrt_cache["by_4t_list"] = bmrlist_by_4tuple
    bmrt_cache["meta"] = CacheUpdateMetaInfo(
        newest_result_time_str=first_result.ui_time_started_at,
        covered_timeframe_days_approx=str(
            (first_result.timestamp - last_result.timestamp).days
        ),
        oldest_result_time_str=last_result.ui_time_started_at,
        n_results=len(by_id_dict),
    )

    conbench.metrics.GAUGE_BMRT_CACHE_LAST_UPDATE_SECONDS.set(t1 - t0)

    log.info(
        ("BMRT cache population done (%s results, took %.3f s)"),
        len(bmrt_cache["by_id"]),
        t1 - t0,
    )


def _periodically_fetch_last_n_benchmark_results() -> None:
    """
    Immediately return after having spawned a thread triggers periodic action.
    """
    first_sleep_seconds = 3
    min_delay_between_runs_seconds = 120

    if Config.TESTING:
        first_sleep_seconds = 2
        min_delay_between_runs_seconds = 20

    def _run_forever():
        global SHUTDOWN
        global _STARTED
        _STARTED = True

        delay_s = first_sleep_seconds

        while True:
            # Build responsive sleep loop that inspects SHUTDOWN often.
            deadline = time.monotonic() + delay_s
            while time.monotonic() < deadline:
                if SHUTDOWN:
                    log.debug("_run_forever: shut down")
                    return

                time.sleep(0.1)

            t0 = time.monotonic()

            # yappi.start()

            try:
                # filprofile(lambda: _fetch_and_cache_most_recent_results(), "fil-result")
                _fetch_and_cache_most_recent_results()
            except Exception as exc:
                # For now, log all error detail. (but handle all exceptions; do
                # some careful log-reading after rolling this out).
                log.exception("BMRT cache: exception during update: %s", exc)

            # yappi.stop()
            # yappi_print_threads_stats()

            last_call_duration_s = time.monotonic() - t0

            # Generally we want to spent the majority of the time _not_ doing
            # this thing here. So, if the last iteration lasted for e.g. ~60
            # seconds, then keep waiting for ~five minutes until triggering the
            # next run.
            delay_s = max(min_delay_between_runs_seconds, 5 * last_call_duration_s)
            log.info("BMRT cache: trigger next fetch in %.3f s", delay_s)

    if not Config.CREATE_ALL_TABLES:
        # This needs to be done more cleanly -- when running the DB migration,
        # the app should not even initialize so far.
        log.info(
            "BMRT cache: CREATE_ALL_TABLES is false, assume migration; disable cache job"
        )
        return

    threading.Thread(target=_run_forever).start()
    # Do not attempt to explicitly join thread. Terminate thread cleanly as
    # part of gunicorn's worker process shutdown -- therefore the signal
    # handler-based logic below which injects a shutdown signal into the
    # thread.


def _generate_tsdf_per_4tuple(
    by_name_dict: Dict[TBenchmarkName, List[BMRTBenchmarkResult]]
) -> Tuple[TDict4tdf, TDict4tlist]:
    t2 = time.monotonic()
    by_name_dict_with_timeseries_tuplekeys: Dict[
        TBenchmarkName, Dict[Tuple, List[BMRTBenchmarkResult]]
    ] = {}

    for bname, results in by_name_dict.items():
        # The magic time series 4-tuple is
        # bname, caseid, hwid, ctxid
        by_ts_tuple: Dict[Tuple, List[BMRTBenchmarkResult]] = defaultdict(list)
        for r in results:
            by_ts_tuple[(r.case_id, r.context_id, r.hardware_id)].append(r)
        by_name_dict_with_timeseries_tuplekeys[bname] = by_ts_tuple

    t3 = time.monotonic()

    tsdf_by_4tuple: TDict4tdf = {}
    bmrlist_by_4tuple: TDict4tlist = {}

    # Brutal, slow, approach: (ideally we find a way to represent all data in a
    # single dataframe with decent multi-index -- that could be a major speedup
    # for timeseries analysis on all of these series in a bulk.) one dataframe
    # per 4-tuple: (bname, case_id, context_id, hardware_id).
    # I have seen this below DF construction loop to take 3 seconds for 2*10^5
    # results.
    for bname, unsorted_timeseries in by_name_dict_with_timeseries_tuplekeys.items():
        for (
            case_id,
            context_id,
            hardware_id,
        ), usresults in unsorted_timeseries.items():
            # Think: `usresults` is a list not yet sorted by time.

            df = pd.DataFrame(
                # Note(jp:): cannot use a generator expression here, len needs
                # to be known.
                {"svs": [r.svs for r in usresults]},
                # Note(jp): also no generator expression possible. The
                # `unit="s"` is the critical ingredient to convert this list of
                # floaty unix timestamps to datetime representation. `utc=True`
                # is required to localize the pandas DateTimeIndex to UTC
                # (input is tz-naive).
                index=pd.to_datetime(
                    [r.started_at for r in usresults], unit="s", utc=True
                ),
            )
            # Sort by time.
            df = df.sort_index()
            df.index.rename("time", inplace=True)
            tsdf_by_4tuple[(bname, case_id, context_id, hardware_id)] = df
            bmrlist_by_4tuple[(bname, case_id, context_id, hardware_id)] = usresults

    t4 = time.monotonic()
    log.info("BMRT cache pop: quadratic sort loop took %.3f s", t3 - t2)
    log.info(
        "BMRT cache pop: df constr took %.3f s (%s time series)",
        t4 - t3,
        len(tsdf_by_4tuple),
    )

    # The following comment is provides insight into the structure of the
    # return value. It shows one example for the key (4-tuple) and
    # corresponding value (and its properties; Index, h)

    # for i, (t4, dffff) in enumerate(tsdf_per_4tuple.items()):
    #     if i % 1000 == 0:
    #         print(t4)
    #         print(dffff)
    # ('tpch-foobar', '750317efddda4b76a80f72d9ac44f882', 'c99e3d44ccf9415996209006244d6b10', '31ce04b765d44f32a4f2c6a7762e2ddb')
    #                                             svs
    # 2022-09-28 02:25:54.315165043+00:00   93.072853
    # 2022-09-28 10:32:56.099033117+00:00  100.253622
    # 2022-09-28 13:51:49.347893+00:00     102.833077
    # 2022-09-28 15:57:35.356076002+00:00   99.807175
    # 2022-09-28 17:06:46.327281952+00:00  102.777138
    # 2022-09-28 17:14:14.036443949+00:00  100.854897
    # 2022-09-28 20:08:16.950268984+00:00   99.565141
    # 2022-09-28 20:10:27.393528938+00:00   93.057321
    # 2022-09-29 00:02:27.419251919+00:00   99.077197
    # 2022-09-29 00:17:44.202492952+00:00   96.842827
    # 2022-09-29 02:26:19.996010065+00:00   91.103735
    # 2022-09-29 03:18:40.925746918+00:00         NaN
    # 2022-09-29 03:52:28.406414986+00:00         NaN

    return tsdf_by_4tuple, bmrlist_by_4tuple


def start_jobs():
    log.info("start job: periodic BMRT cache population")
    _periodically_fetch_last_n_benchmark_results()
    log.info("start job: metrics.periodically_set_q_rem()")
    conbench.metrics.periodically_set_q_rem()


def shutdown_handler(sig, frame):
    log.info(
        "BMRT cache job (started: %s): saw signal %s, set shutdown flag", _STARTED, sig
    )
    global SHUTDOWN
    SHUTDOWN = True
    if sig == signal.SIGINT:
        original_sigint_handler(sig, frame)


# def yappi_print_threads_stats():
#     """ """
#     threads = yappi.get_thread_stats()
#     print("\n\n")
#     for thread in threads:
#         print("Stats for (%s) (%d)" % (thread.name, thread.id))
#         # Didn't find docs, but after code inspection I found a way to
#         # increase column width in output.
#         columns = {
#             0: ("name", 150),
#             1: ("ncall", 10),
#             2: ("tsub", 12),
#             3: ("ttot", 12),
#             4: ("tavg", 12),
#         }
#         yappi.get_func_stats(ctx_id=thread.id).print_all(columns=columns)


# Handle the common signals that instruct us to gracefully shut down. We have
# installed custom logic in the gunicorn worker_interrupt hook where we send
# ourselves a SIGTERM sinal. Don't worry, I don't generally hurt myself.
signal.signal(signal.SIGTERM, shutdown_handler)

# For interactive sessions (such as when running make run-app-dev)
signal.signal(signal.SIGINT, shutdown_handler)

# There is no clear purpose for this yet; I wonder which mechanism docker
# compose really uses to signal its containers a graceful shutdown -- so far I
# need to send SIGINT twice, and I think then it immediately sends SIGKILL to
# containerized processes.
signal.signal(signal.SIGQUIT, shutdown_handler)
