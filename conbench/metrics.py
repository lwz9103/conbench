"""
This module documents and initializes Prometheus metrics (Counters, Gauges,
Histograms, Summaries). It also defines functions for integration with the
Flask web application.

Helpful resources about naming metrics, as well as metric types:

- https://prometheus.io/docs/concepts/metric_types/
- https://github.com/prometheus/docs/blob/main/content/docs/practices/naming.md
- https://www.robustperception.io/on-the-naming-of-things/
- https://prometheus.io/docs/practices/naming/

A thread about using normal Python prometheus_client metrics at the same time
as prometheus_flask_exporter metrics ("just works!"):
https://github.com/rycus86/prometheus_flask_exporter/issues/147
"""

import logging
import os

import prometheus_client
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

log = logging.getLogger(__name__)


COUNTER_GITHUB_HTTP_API_REQUESTS = prometheus_client.Counter(
    "conbench_github_httpapi_requests_total",
    "The total number of HTTP requests (attempted) to make to the GitHub HTTP API",
)


COUNTER_GITHUB_HTTP_API_REQUEST_FAILURES = prometheus_client.Counter(
    "conbench_github_httpapi_requests_failed_total",
    "The total number of HTTP requests to the GitHub HTTP API that failed "
    "eventually (either immediately or after retrying).",
)


COUNTER_GITHUB_HTTP_API_RETRYABLE_ERRORS = prometheus_client.Counter(
    "conbench_github_httpapi_retryable_errors_total",
    "The total number of retryable errors observed while interacting with the "
    "GitHub HTTP API (regardless of whether a retry was performed or not).",
)


COUNTER_GITHUB_HTTP_API_403RESPONSES = prometheus_client.Counter(
    "conbench_github_httpapi_403responses_total",
    "The total number of HTTP requests to the GitHub HTTP API that were "
    "responded to with a 403 response. Often rate-limiting/quota related.",
)


GAUGE_GITHUB_HTTP_API_QUOTA_REMAINING = prometheus_client.Gauge(
    "conbench_github_httpapi_quota_remaining",
    "A gauge that shows the last-observed x-ratelimit-remaining response "
    "header value.",
    # multiprocess mode gauges are tricky!
    # https://github.com/prometheus/client_python#multiprocess-mode-eg-gunicorn
    multiprocess_mode="liveall",
)


# The topic of Gauge initiatlization in the Prometheus ecosystem is confusing.
# The spec says "Gauges MUST start at 0"
# (https://prometheus.io/docs/instrumenting/writing_clientlibs/). There are
# client libs that thought about NaN:
# https://github.com/micrometer-metrics/micrometer/issues/1343. With the very
# specific setup we have (Python's client lib in multiprocessing mode) it seems
# to report (from the start) the value 0. The value 0 however in this context
# has a special meaning: quota exhausted. So, once this gauge reports as 0 we
# want to know that this value came from an HTTP response. For now, set a
# special value -1 that by convention in this case here shall mean 'not
# initialized'. That is, if this ever shows a positive value or 0 then the
# value was communciated within an HTTP Response.
GAUGE_GITHUB_HTTP_API_QUOTA_REMAINING.set(-1)


def decorate_flask_app_with_metrics(app) -> None:
    """
    Add flask-prometheus-exporter magic to `app`.

    This mutates `app` in-place.
    """
    # Use `GunicornPrometheusMetrics` when spawning a separate HTTP server for
    # the metrics scrape endpoint. This needs PROMETHEUS_MULTIPROC_DIR to be
    # set to a path to a directory.
    _inspect_prom_multiproc_dir()
    GunicornInternalPrometheusMetrics(
        app=app,
        # Set bucket boundaries (unit: seconds) for tracking the distribution
        # of HTTP request processing durations (Prometheus metric of type
        # histogram). The default histogram buckets are not so useful for
        # Conbench as of today, because they are optimized for low-latency
        # APIs. Set bucket boundaries so that we have some resolution on the
        # high latency tail end. Once we push request processing times more or
        # less reliably below 10 seconds we can change these again. Each value
        # defines the upper inclusive bound for the corresponding histogram
        # bucket. Note that there is an implicit last/upper end bucket here
        # catching all observations up to +inf.
        buckets=(0.05, 0.1, 0.2, 0.5, 1.0, 3.0, 6.0, 10.0, 15.0, 20.0, 30.0, 50.0),
    )


def _inspect_prom_multiproc_dir():
    """
    Log information about the environment variable PROMETHEUS_MULTIPROC_DIR
    and about the path it points to. This is helpful for debugging bad state.
    """
    path = os.environ.get("PROMETHEUS_MULTIPROC_DIR")
    log.info("env PROMETHEUS_MULTIPROC_DIR: `%s`", path)

    if not path:
        return

    try:
        log.info("os.path.isdir('%s'): %s", path, os.path.isdir(path))
    except OSError as exc:
        log.info("os.path.isdir('%s') failed: %s", path, exc)
