import json
import logging
import os
import time
import urllib.parse
from datetime import datetime, timezone
from typing import Union

import click
import requests
import yaml
from _pytest.pathlib import import_path
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(
    total=5,
    status_forcelist=[502, 503, 504],
    allowed_methods=frozenset(["GET", "POST"]),
    backoff_factor=4,  # will retry in 2, 4, 8, 16, 32 seconds
)
adapter = HTTPAdapter(max_retries=retry_strategy)


log = logging.getLogger()


def tznaive_iso8601_to_tzaware_dt(
    input: Union[str, list[str]]
) -> Union[datetime, list[datetime]]:
    """
    Convert time strings into datetime objects.

    If a list of strings is provided return a list of datetime objects.

    If a single string is provided return a single datetime object.

    Assume that each provided string is in ISO 8601 notation without timezone
    information, but that the time is actually meant to be interpreted in the
    UTC timezone.

    Note: this was built with and tested for a value like 2022-03-03T19:48:06
    which in this example represents a commit timestamp (in UTC, additional
    knowledge).
    """

    def _convert(s: str):
        # Do some sanity-checking. If unexpected input is seen, only emit the
        # warning but then still hard-set UTC timezone.
        if "Z" in s:
            # Input seems to be tz-aware but the timezone it specifies matches
            # the one we want to set anyway.
            log.warning("expected tz-naive timestring, but saw UTC: %s", s)

        if "+" in s and "00:00" not in s:
            # Input seems to be tz-aware but the timezone it specifies does
            # not match UTC.
            log.warning("expected tz-naive timestring, but saw non-UTC: %s", s)

        return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)

    # Handle case where input is a single string.
    if isinstance(input, str):
        return _convert(input)

    # Handle case where input is a list of strings.
    return [_convert(s) for s in input]


class Connection:
    def __init__(self):
        self.config = Config(get_config())
        self.session = None

    def publish(self, benchmark):
        self.post(self.config.benchmarks_url, benchmark)

    def post(self, url, data):
        if self.session:
            # already authenticated, just do post
            self._post(url, data, 201)

        if not self.session:
            # not already authenticated, or authentication expired (try again)
            self._post(self.config.login_url, self.config.credentials, 204)
            self._post(url, data, 201)

    def _post(self, url, data, expected):
        try:
            if not self.session:
                self.session = requests.Session()
                self.session.mount("https://", adapter)
            start = time.monotonic()
            response = self.session.post(url, json=data)
            print("Time to POST", url, time.monotonic() - start)
            if response.status_code != expected:
                self._unexpected_response("POST", response, url)
        except requests.exceptions.ConnectionError:
            self.session = None

    def _unexpected_response(self, method, response, url):
        self._print_error(f"\n{method} {url} failed", red=True)
        if response.content:
            try:
                message = json.loads(response.content)
                self._print_error(f"{json.dumps(message, indent=2)}\n")
            except json.JSONDecodeError:
                self._print_error(f"{response.content}\n")
        self.session = None

    def _print_error(self, msg, red=False):
        if red:
            click.echo(click.style(msg, fg="red"))
        else:
            click.echo(msg)


def places_to_look():
    current_dir = os.getcwd()
    benchmarks_dir = os.path.join(current_dir, "benchmarks")
    if os.path.exists(benchmarks_dir):
        return [current_dir, benchmarks_dir]
    return [current_dir]


class Config:
    def __init__(self, config):
        url = config.get("url", "http://localhost:5000")
        email = config.get("email", "conbench@example.com")
        password = str(config.get("password", "conbench"))
        self.host_name = config.get("host_name")
        self.login_url = urllib.parse.urljoin(url, "api/login/")
        self.benchmarks_url = urllib.parse.urljoin(url, "api/benchmarks/")
        self.credentials = {"email": email, "password": password}


def get_config(filename=None):
    """Get config from a yaml file named .conbench in the current
    working directory, or a sub directory called "benchmarks".
    """
    config = {}
    if filename is None:
        filename = ".conbench"
    for directory in places_to_look():
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            with open(file_path) as f:
                return yaml.load(f, Loader=yaml.FullLoader)
    return config


def register_benchmarks(directory=None):
    """Look for files matching the following patterns in the current
    working directory or a sub directory called "benchmarks", and
    import them.

        benchmark*.py
        *benchmark.py
        *benchmarks.py

    This registers benchmarks that are decorated as conbench benchmarks.

        import conbench.runner

        @conbench.runner.register_benchmark
        class ExampleBenchmark:
            ...

    It also registers the benchmark list class.

        import conbench.runner

        @conbench.runner.register_list
        class ExampleBenchmarkList:
            ...
    """
    dirs = places_to_look() if directory is None else [directory]
    for directory in dirs:
        with os.scandir(directory) as scan:
            for entry in scan:
                filename = entry.name
                if (
                    filename.startswith(".")
                    or not entry.is_file()
                    or not filename.endswith(".py")
                ):
                    continue
                if (
                    filename.startswith("benchmark")
                    or filename.endswith("benchmark.py")
                    or filename.endswith("benchmarks.py")
                ):
                    import_path(f"{directory}/{filename}", root=entry)
