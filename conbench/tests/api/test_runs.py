from datetime import datetime, timedelta, timezone

import pytest

from conbench.util import tznaive_dt_to_aware_iso8601_for_api

from ...api._examples import _api_run_entity
from ...entities._entity import NotFound
from ...entities.run import Run
from ...tests.api import _asserts, _fixtures
from ...tests.helpers import _uuid

DEFAULT_BRANCH_PLACEHOLDER = {
    "error": "the contender run is already on the default branch",
    "baseline_run_id": None,
    "commits_skipped": None,
}


def _expected_entity(run: Run, candidate_baseline_runs=None):
    parent = run.commit.get_parent_commit() if run.commit else None
    has_errors = False
    entity = _api_run_entity(
        run.id,
        run.name,
        run.reason,
        run.commit_id,
        parent.id if parent else None,
        run.hardware_id,
        run.hardware.name,
        run.hardware.type,
        tznaive_dt_to_aware_iso8601_for_api(run.timestamp),
        has_errors,
        tznaive_dt_to_aware_iso8601_for_api(run.finished_timestamp)
        if run.finished_timestamp
        else None,
        run.info,
        run.error_info,
        run.error_type,
    )
    if candidate_baseline_runs:
        entity["candidate_baseline_runs"] = candidate_baseline_runs
    else:
        del entity["candidate_baseline_runs"]
    return entity


class TestRunGet(_asserts.GetEnforcer):
    url = "/api/runs/{}/"
    public = True

    def _create(self, baseline=False, name=None, language=None):
        if baseline:
            contender = _fixtures.benchmark_result(
                name=name,
                sha=_fixtures.CHILD,
                language=language,
            )
            baseline = _fixtures.benchmark_result(
                name=name,
                sha=_fixtures.PARENT,
                language=language,
            )
            return contender.run, baseline.run
        else:
            contender = _fixtures.benchmark_result()
        return contender.run

    def test_get_run(self, client):
        # change anything about the context so we get only one baseline
        language, name = _uuid(), _uuid()

        self.authenticate(client)
        run, baseline = self._create(baseline=True, name=name, language=language)
        response = client.get(f"/api/runs/{run.id}/")
        self.assert_200_ok(
            response,
            _expected_entity(
                run,
                candidate_baseline_runs={
                    "fork_point": DEFAULT_BRANCH_PLACEHOLDER,
                    "latest_default": {
                        "baseline_run_id": baseline.id,
                        "commits_skipped": [run.commit.sha],
                        "error": None,
                    },
                    "parent": {
                        "baseline_run_id": baseline.id,
                        "commits_skipped": [],
                        "error": None,
                    },
                },
            ),
        )

    def test_get_run_without_commit(self, client):
        self.authenticate(client)
        result = _fixtures.benchmark_result(no_github=True)
        run = result.run
        response = client.get(f"/api/runs/{run.id}/")
        expected = _expected_entity(
            run,
            candidate_baseline_runs={
                "fork_point": {
                    "baseline_run_id": None,
                    "commits_skipped": None,
                    "error": "the contender run is not connected to the git graph",
                },
                "latest_default": {
                    "baseline_run_id": None,
                    "commits_skipped": None,
                    "error": "this baseline commit type does not exist for this run",
                },
                "parent": {
                    "baseline_run_id": None,
                    "commits_skipped": None,
                    "error": "the contender run is not connected to the git graph",
                },
            },
        )
        expected["commit"] = None
        expected["links"].pop("commit")
        self.assert_200_ok(response, expected)

    def test_get_run_should_not_prefer_test_runs_as_baseline(self, client):
        """Test runs shouldn't be preferred, but if they are the only runs that exist,
        we'll pick them up"""
        # change anything about the context so we get only one baseline
        language, name = _uuid(), _uuid()

        self.authenticate(client)
        run, baseline = self._create(baseline=True, name=name, language=language)
        baseline.name = "testing"
        baseline.reason = "test"
        baseline.save()
        response = client.get(f"/api/runs/{run.id}/")
        self.assert_200_ok(
            response,
            _expected_entity(
                run,
                candidate_baseline_runs={
                    "fork_point": DEFAULT_BRANCH_PLACEHOLDER,
                    "latest_default": {
                        "baseline_run_id": baseline.id,
                        "commits_skipped": [run.commit.sha],
                        "error": None,
                    },
                    "parent": {
                        "baseline_run_id": baseline.id,
                        "commits_skipped": [],
                        "error": None,
                    },
                },
            ),
        )

    def test_get_run_find_correct_baseline_many_matching_contexts(self, client):
        # same context for different benchmark runs, but different benchmarks
        language, name_1, name_2 = _uuid(), _uuid(), _uuid()

        self.authenticate(client)
        run_1, baseline_1 = self._create(baseline=True, name=name_1, language=language)
        run_2, baseline_2 = self._create(baseline=True, name=name_2, language=language)
        response = client.get(f"/api/runs/{run_1.id}/")
        self.assert_200_ok(
            response,
            _expected_entity(
                run_1,
                candidate_baseline_runs={
                    "fork_point": DEFAULT_BRANCH_PLACEHOLDER,
                    "latest_default": {
                        "baseline_run_id": baseline_1.id,
                        "commits_skipped": [run_1.commit.sha],
                        "error": None,
                    },
                    "parent": {
                        "baseline_run_id": baseline_1.id,
                        "commits_skipped": [],
                        "error": None,
                    },
                },
            ),
        )
        response = client.get(f"/api/runs/{run_2.id}/")
        self.assert_200_ok(
            response,
            _expected_entity(
                run_2,
                candidate_baseline_runs={
                    "fork_point": DEFAULT_BRANCH_PLACEHOLDER,
                    "latest_default": {
                        "baseline_run_id": baseline_2.id,
                        "commits_skipped": [run_2.commit.sha],
                        "error": None,
                    },
                    "parent": {
                        "baseline_run_id": baseline_2.id,
                        "commits_skipped": [],
                        "error": None,
                    },
                },
            ),
        )

    def test_get_run_find_correct_baseline_with_multiple_runs(self, client):
        language_1, language_2, name_1, name_2 = _uuid(), _uuid(), _uuid(), _uuid()
        contender_run_id, baseline_run_id_1, baseline_run_id_2 = (
            _uuid(),
            _uuid(),
            _uuid(),
        )

        self.authenticate(client)
        # Create contender run with two benchmark results
        a_contender_result = _fixtures.benchmark_result(
            name=name_1,
            sha=_fixtures.CHILD,
            language=language_1,
            run_id=contender_run_id,
        )
        _fixtures.benchmark_result(
            name=name_2,
            sha=_fixtures.CHILD,
            language=language_1,
            run_id=contender_run_id,
        )
        # Create baseline run one benchmark result matching contender's
        _fixtures.benchmark_result(
            name=name_1,
            sha=_fixtures.PARENT,
            language=language_1,
            run_id=baseline_run_id_1,
        )
        # Create baseline run with no benchmark results matching contender's
        _fixtures.benchmark_result(
            name=name_1,
            sha=_fixtures.PARENT,
            language=language_2,
            run_id=baseline_run_id_2,
        )
        response = client.get(f"/api/runs/{contender_run_id}/")
        assert response.json["candidate_baseline_runs"] == {
            "fork_point": DEFAULT_BRANCH_PLACEHOLDER,
            "latest_default": {
                "baseline_run_id": baseline_run_id_1,
                "commits_skipped": [a_contender_result.run.commit.sha],
                "error": None,
            },
            "parent": {
                "baseline_run_id": baseline_run_id_1,
                "commits_skipped": [],
                "error": None,
            },
        }

    def test_get_run_without_baseline_run_with_matching_benchmarks(self, client):
        (
            language_1,
            language_2,
            name,
        ) = (
            _uuid(),
            _uuid(),
            _uuid(),
        )
        contender_run_id, baseline_run_id = _uuid(), _uuid()

        self.authenticate(client)
        # Create contender run with one benchmark result
        _fixtures.benchmark_result(
            name=name, sha=_fixtures.CHILD, language=language_1, run_id=contender_run_id
        )
        # Create baseline run with no benchmark results matching contender's
        _fixtures.benchmark_result(
            name=name, sha=_fixtures.PARENT, language=language_2, run_id=baseline_run_id
        )
        response = client.get(f"/api/runs/{contender_run_id}/")
        assert response.json["candidate_baseline_runs"] == {
            "fork_point": DEFAULT_BRANCH_PLACEHOLDER,
            "latest_default": {
                "baseline_run_id": None,
                "commits_skipped": None,
                "error": "no matching baseline run was found",
            },
            "parent": {
                "baseline_run_id": None,
                "commits_skipped": None,
                "error": "no matching baseline run was found",
            },
        }

    def test_closest_commit_different_machines(self, client):
        # same benchmarks, different machines
        name, machine_1, machine_2 = _uuid(), _uuid(), _uuid()

        self.authenticate(client)
        contender = _fixtures.benchmark_result(
            name=name,
            sha=_fixtures.CHILD,
            hardware_name=machine_1,
        )
        parent = _fixtures.benchmark_result(
            name=name,
            sha=_fixtures.PARENT,
            hardware_name=machine_2,
        )
        baseline = _fixtures.benchmark_result(
            name=name,
            sha=_fixtures.GRANDPARENT,
            hardware_name=machine_1,
        )
        _fixtures.benchmark_result(
            name=name,
            sha=_fixtures.ELDER,
            hardware_name=machine_1,
        )

        contender_run = contender.run
        baseline_run = baseline.run

        response = client.get(f"/api/runs/{contender_run.id}/")
        self.assert_200_ok(
            response,
            _expected_entity(
                contender_run,
                candidate_baseline_runs={
                    "fork_point": DEFAULT_BRANCH_PLACEHOLDER,
                    "latest_default": {
                        "baseline_run_id": baseline_run.id,
                        "commits_skipped": [
                            contender.run.commit.sha,
                            parent.run.commit.sha,
                        ],
                        "error": None,
                    },
                    "parent": {
                        "baseline_run_id": baseline_run.id,
                        "commits_skipped": [parent.run.commit.sha],
                        "error": None,
                    },
                },
            ),
        )

    def test_closest_commit_different_machines_should_not_prefer_test_runs_as_baseline(
        self, client
    ):
        """Test runs shouldn't be preferred, but if they are the only runs that exist,
        we'll pick them up"""
        # same benchmarks, different machines, skip test run
        name, machine_1, machine_2 = _uuid(), _uuid(), _uuid()

        self.authenticate(client)
        contender = _fixtures.benchmark_result(
            name=name,
            sha=_fixtures.CHILD,
            hardware_name=machine_1,
        )
        parent = _fixtures.benchmark_result(
            name=name,
            sha=_fixtures.PARENT,
            hardware_name=machine_2,
        )
        testing = _fixtures.benchmark_result(
            name=name,
            sha=_fixtures.GRANDPARENT,
            hardware_name=machine_1,
        )
        baseline = _fixtures.benchmark_result(
            name=name,
            sha=_fixtures.ELDER,
            hardware_name=machine_1,
        )

        testing_run = testing.run
        testing_run.name = "testing"
        testing_run.reason = "test"
        testing_run.save()

        contender_run = contender.run
        baseline_run = baseline.run

        response = client.get(f"/api/runs/{contender_run.id}/")
        self.assert_200_ok(
            response,
            _expected_entity(
                contender_run,
                candidate_baseline_runs={
                    "fork_point": DEFAULT_BRANCH_PLACEHOLDER,
                    "latest_default": {
                        "baseline_run_id": baseline_run.id,
                        "commits_skipped": [
                            contender.run.commit.sha,
                            parent.run.commit.sha,
                            testing.run.commit.sha,
                        ],
                        "error": None,
                    },
                    "parent": {
                        "baseline_run_id": baseline_run.id,
                        "commits_skipped": [
                            parent.run.commit.sha,
                            testing.run.commit.sha,
                        ],
                        "error": None,
                    },
                },
            ),
        )


class TestRunList(_asserts.ListEnforcer):
    url = "/api/runs/"
    public = True

    def _create(self):
        _fixtures.benchmark_result(sha=_fixtures.PARENT)
        benchmark_result = _fixtures.benchmark_result()
        return benchmark_result.run

    def test_run_list(self, client):
        self.authenticate(client)
        run = self._create()
        response = client.get("/api/runs/")
        self.assert_200_ok(response, contains=_expected_entity(run))

    def test_run_list_filter_by_sha(self, client):
        sha = _fixtures.CHILD
        self.authenticate(client)
        run = self._create()
        response = client.get(f"/api/runs/?sha={sha}")
        self.assert_200_ok(response, contains=_expected_entity(run))

    def test_run_list_filter_by_multiple_sha(self, client):
        sha1 = _fixtures.CHILD
        sha2 = _fixtures.PARENT
        self.authenticate(client)
        _fixtures.benchmark_result(sha=_fixtures.PARENT)
        run_1 = _fixtures.benchmark_result()
        _fixtures.benchmark_result(sha=_fixtures.CHILD)
        run_2 = _fixtures.benchmark_result()
        response = client.get(f"/api/runs/?sha={sha1},{sha2}")

        self.assert_200_ok(response, contains=_expected_entity(run_1.run))

        self.assert_200_ok(response, contains=_expected_entity(run_2.run))

    def test_run_list_filter_by_sha_no_match(self, client):
        sha = "some unknown sha"
        self.authenticate(client)
        self._create()
        response = client.get(f"/api/runs/?sha={sha}")
        self.assert_200_ok(response, [])


class TestRunDelete(_asserts.DeleteEnforcer):
    url = "api/runs/{}/"

    def test_delete_run(self, client):
        self.authenticate(client)
        benchmark_result = _fixtures.benchmark_result()
        run_id = benchmark_result.run_id

        # can get before delete
        Run.one(id=run_id)

        # delete
        response = client.delete(f"/api/runs/{run_id}/")
        self.assert_204_no_content(response)

        # cannot get after delete
        with pytest.raises(NotFound):
            Run.one(id=run_id)


class TestRunPut(_asserts.PutEnforcer):
    url = "/api/runs/{}/"
    valid_payload = {
        "finished_timestamp": "2022-11-25T21:02:45Z",
        "info": {"setup": "passed"},
        "error_info": {"error": "error", "stack_trace": "stack_trace", "fatal": True},
        "error_type": "fatal",
    }

    def setup_method(self):
        Run.delete_all()

    def _create_entity_to_update(self):
        _fixtures.benchmark_result(sha=_fixtures.PARENT)
        # This writes to the database.
        benchmark_result = _fixtures.benchmark_result()
        run = benchmark_result.run
        return run

    def test_update_allowed_fields(self, client):
        self.authenticate(client)

        # before
        run_before = self._create_entity_to_update()
        for key in self.valid_payload.keys():
            assert getattr(run_before, key) is None

        # mutate run in db
        resp = client.put(f"/api/runs/{run_before.id}/", json=self.valid_payload)
        assert resp.status_code == 200, resp.status_code

        # receive (hopefully) mutated run from db
        resp = client.get(f"/api/runs/{run_before.id}/")
        assert resp.status_code == 200, resp.status_code

        run_after_mod = resp.json

        for key, value in self.valid_payload.items():
            # if key == "finished_timestamp":
            #     assert (
            #         tznaive_dt_to_aware_iso8601_for_api(run_after_mod.get(key)) == value
            #     )
            # else:
            assert run_after_mod.get(key) == value

    @pytest.mark.parametrize(
        "timeinput, timeoutput",
        [
            ("2022-11-25 21:02:41", "2022-11-25T21:02:41Z"),
            ("2022-11-25 22:02:42Z", "2022-11-25T22:02:42Z"),
            ("2022-11-25T22:02:42Z", "2022-11-25T22:02:42Z"),
            # That next pair confirms timezone conversion.
            ("2022-11-25 23:02:00+07:00", "2022-11-25T16:02:00Z"),
            # Confirm that fractions of seconds can be provided, but are not
            # returned (we can dispute that of course).
            ("2022-11-25T22:02:42.123456Z", "2022-11-25T22:02:42Z"),
        ],
    )
    def test_finished_timestamp_tz(self, client, timeinput, timeoutput):
        self.authenticate(client)
        before = self._create_entity_to_update()
        resp = client.put(
            f"/api/runs/{before.id}/",
            json={
                "finished_timestamp": timeinput,
            },
        )
        assert resp.status_code == 200, resp.text

        resp = client.get(f"/api/runs/{before.id}/")
        assert resp.json["finished_timestamp"] == timeoutput

    @pytest.mark.parametrize(
        "timeinput, expected_err",
        # first item: bad input, second item: expected err msg
        [
            ("2022-11-2521:02:41x", "Not a valid datetime"),
            ("foobar", "Not a valid datetime"),
        ],
    )
    def test_finished_timestamp_invalid(
        self, client, timeinput: str, expected_err: str
    ):
        self.authenticate(client)
        run = self._create_entity_to_update()
        resp = client.put(
            f"/api/runs/{run.id}/",
            json={
                "finished_timestamp": timeinput,
            },
        )
        assert resp.status_code == 400, resp.text
        assert expected_err in resp.text


class TestRunPost(_asserts.PostEnforcer):
    url = "/api/runs/"
    valid_payload = _fixtures.VALID_RUN_PAYLOAD
    valid_payload_for_cluster = _fixtures.VALID_RUN_PAYLOAD_FOR_CLUSTER
    valid_payload_with_error = _fixtures.VALID_RUN_PAYLOAD_WITH_ERROR
    required_fields = ["id"]

    # This test does not apply because we expect users to send run id when creating runs
    def test_cannot_set_id(self, client):
        pass

    def test_create_run(self, client):
        for hardware_type, payload in [
            ("machine", self.valid_payload),
            ("cluster", self.valid_payload_for_cluster),
        ]:
            self.authenticate(client)
            run_id = payload["id"]
            assert not Run.first(id=run_id)
            response = client.post(self.url, json=payload)
            # print(response)
            # print(response.json)
            run = Run.one(id=run_id)
            location = f"http://localhost/api/runs/{run_id}/"
            self.assert_201_created(response, _expected_entity(run), location)

            assert run.hardware.type == hardware_type
            for attr, value in payload[f"{hardware_type}_info"].items():
                assert getattr(run.hardware, attr) == value or getattr(
                    run.hardware, attr
                ) == int(value)

    def test_create_run_with_error(self, client):
        self.authenticate(client)
        run_id = self.valid_payload_with_error["id"]
        assert not Run.first(id=run_id)
        response = client.post(self.url, json=self.valid_payload_with_error)
        run = Run.one(id=run_id)
        location = f"http://localhost/api/runs/{run_id}/"
        self.assert_201_created(response, _expected_entity(run), location)

    def test_create_run_same_id(self, client):
        self.authenticate(client)
        run_id = self.valid_payload_with_error["id"]
        assert not Run.first(id=run_id)
        resp = client.post(self.url, json=self.valid_payload_with_error)
        assert resp.status_code == 201
        resp = client.post(self.url, json=self.valid_payload_with_error)
        assert resp.status_code == 409, resp.text
        assert "conflict" in resp.json["description"].lower()
        assert resp.json["error"] == 409
        assert run_id in resp.json["description"].lower()

    def test_create_run_timestamp_not_allowed(self, client):
        self.authenticate(client)
        payload = self.valid_payload.copy()

        # Confirm that setting the timestamp is not possible as an API client,
        # i.e. that the resulting `timestamp` property when fetching the run
        # details via API later on reflects the point in time of inserting this
        # run into the DB.
        payload["timestamp"] = "2022-12-13T13:37:00Z"
        resp = client.post(self.url, json=payload)
        assert resp.status_code == 400, resp.text
        assert '{"timestamp": ["Unknown field."]}' in resp.text

    def test_auto_generated_run_timestamp_value(self, client):
        self.authenticate(client)
        payload = self.valid_payload.copy()
        resp = client.post(self.url, json=payload)
        assert resp.status_code == 201, resp.text
        run_id = payload["id"]

        resp = client.get(f"http://localhost/api/runs/{run_id}/")
        assert resp.status_code == 200, resp.text
        assert "timestamp" in resp.json

        # Get current point in time from test runner's perspective (tz-aware
        # datetime object).
        now_testrunner = datetime.now(timezone.utc)

        # Get Run entity DB insertion time (set by the DB). This is also a
        # tz-aware object because `resp.json["timestamp"]` is expected to be an
        # ISO 8601 timestring _with_ timezone information.
        run_time_created_in_db = datetime.fromisoformat(resp.json["timestamp"])

        # Build timedelta between those two tz-aware datetime objects (that are
        # not necessarily in the same timezone).
        delta: timedelta = run_time_created_in_db - now_testrunner

        # Convert the timedelta object to a float (number of seconds). Check
        # for tolerance interval but use abs(), i.e. don't expect a certain
        # order between test runner clock and db clock.
        assert abs(delta.total_seconds()) < 5.0
