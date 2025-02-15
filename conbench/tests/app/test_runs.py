import copy
import re
from typing import Optional

from ...app.runs import _default_hyperlink_text
from ...tests.api import _fixtures
from ...tests.app import _asserts


class TestRunGet(_asserts.GetEnforcer):
    url = "/runs/{}/"
    title = "Run"
    redirect_on_unknown = False

    def _create(self, client):
        self.create_benchmark(client)
        return _fixtures.VALID_RESULT_PAYLOAD["run_id"]

    @staticmethod
    def _assert_baseline_link(
        response_text: str,
        candidate_baseline_type: str,
        baseline_id: Optional[str],
        contender_id: Optional[str],
        recommended: bool = False,
    ) -> None:
        """Assert that a link to compare runs exists in the HTML, or doesn't exist if
        the run IDs aren't provided.
        """
        response_text = " ".join(response_text.split())
        expected_text = _default_hyperlink_text[candidate_baseline_type] + "</a>"
        if recommended:
            expected_text = (
                expected_text + ' <span class="badge bg-primary">Recommended</span>'
            )

        if baseline_id and contender_id:
            assert (
                f'/compare/runs/{baseline_id}...{contender_id}/">{expected_text}'
                in response_text
            )
        else:
            assert expected_text not in response_text

    def test_get_run_without_commit(self, client):
        self.authenticate(client)

        # Post a benchmark without a commit
        payload = copy.deepcopy(_fixtures.VALID_RESULT_PAYLOAD)
        del payload["github"]
        response = client.post("/api/benchmarks/", json=payload)
        assert response.status_code == 201

        # Ensure the run doesn't have a commit
        response = client.get(f'/api/runs/{payload["run_id"]}/')
        assert response.status_code == 200
        assert response.json["commit"] is None

        # Ensure the run page looks as expected
        self._assert_view(client, payload["run_id"])

        # Ensure there are no baseline run links
        self._assert_baseline_link(response.text, "parent", None, None)
        self._assert_baseline_link(response.text, "fork_point", None, None)
        self._assert_baseline_link(response.text, "latest_default", None, None)

    def test_baseline_run_links(self, client):
        _, benchmark_results = _fixtures.gen_fake_data()
        self.authenticate(client)

        # Ensure all the pages return 200 and at least contain an expected title in the HTML
        for benchmark_result in benchmark_results:
            self._assert_view(client, benchmark_result.run_id)

        # 0 (first in history) should only have the latest_default link
        response = client.get(self.url.format(benchmark_results[0].run_id))
        self._assert_baseline_link(response.text, "parent", None, None)
        self._assert_baseline_link(response.text, "fork_point", None, None)
        self._assert_baseline_link(
            response.text,
            "latest_default",
            # the latest default branch run with same reason (commit)
            benchmark_results[9].run_id,
            benchmark_results[0].run_id,
        )

        # 1 (also on default branch) should link to 0 for parent
        response = client.get(self.url.format(benchmark_results[1].run_id))
        self._assert_baseline_link(
            response.text,
            "parent",
            benchmark_results[0].run_id,
            benchmark_results[1].run_id,
            recommended=True,
        )
        self._assert_baseline_link(response.text, "fork_point", None, None)
        self._assert_baseline_link(
            response.text,
            "latest_default",
            # the latest default branch run with same reason (commit)
            benchmark_results[9].run_id,
            benchmark_results[1].run_id,
        )

        # 3 is a PR run forked from 1
        response = client.get(self.url.format(benchmark_results[3].run_id))
        self._assert_baseline_link(
            response.text,
            "parent",
            benchmark_results[2].run_id,
            benchmark_results[3].run_id,
        )
        self._assert_baseline_link(
            response.text,
            "fork_point",
            benchmark_results[1].run_id,
            benchmark_results[3].run_id,
            recommended=True,
        )
        self._assert_baseline_link(
            response.text,
            "latest_default",
            benchmark_results[15].run_id,  # the latest default branch run in general
            benchmark_results[3].run_id,
        )


class TestRunDelete(_asserts.DeleteEnforcer):
    def test_authenticated(self, client):
        self.create_benchmark(client)
        run_id = _fixtures.VALID_RESULT_PAYLOAD["run_id"]
        self.authenticate(client)
        response = client.get(f"/runs/{run_id}/")
        self.assert_page(response, "Run")
        assert f"{run_id}".encode() in response.data

        data = {"delete": ["Delete"], "csrf_token": self.get_csrf_token(response)}
        response = client.post(f"/runs/{run_id}/", data=data, follow_redirects=True)
        self.assert_page(response, "Home")
        assert b"Run deleted." in response.data

        response = client.get(f"/runs/{run_id}/", follow_redirects=True)
        assert re.search(r"Run ID unknown: \w+", response.text, flags=re.ASCII)

    def test_unauthenticated(self, client):
        self.create_benchmark(client)
        run_id = _fixtures.VALID_RESULT_PAYLOAD["run_id"]
        self.logout(client)
        data = {"delete": ["Delete"]}
        response = client.post(f"/runs/{run_id}/", data=data, follow_redirects=True)
        self.assert_login_page(response)

    def test_no_csrf_token(self, client):
        self.create_benchmark(client)
        run_id = _fixtures.VALID_RESULT_PAYLOAD["run_id"]
        self.authenticate(client)
        data = {"delete": ["Delete"]}
        response = client.post(f"/runs/{run_id}/", data=data, follow_redirects=True)
        self.assert_page(response, "Home")
        assert b"The CSRF token is missing." in response.data
