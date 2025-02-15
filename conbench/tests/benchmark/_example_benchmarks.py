import json

import conbench.runner


@conbench.runner.register_list
class BenchmarkList(conbench.runner.BenchmarkList):
    def list(self, classes):
        benchmarks = []
        for name, benchmark in classes.items():
            instance, parts = benchmark(), [name]
            if instance.cases:
                parts.append("--all=true")
            parts.append("--iterations=2")
            benchmarks.append({"command": " ".join(parts)})
        return sorted(benchmarks, key=lambda k: k["command"])


@conbench.runner.register_benchmark
class SimpleBenchmark(conbench.runner.Benchmark):
    """Example benchmark without cases."""

    name = "addition"

    def run(self, **kwargs):
        yield self.conbench.benchmark(
            self._get_benchmark_function(), self.name, options=kwargs
        )

    def _get_benchmark_function(self):
        return lambda: 1 + 1


@conbench.runner.register_benchmark
class SimpleBenchmarkWithClusterInfo(conbench.runner.Benchmark):
    """Example benchmark without cases."""

    name = "product"

    def run(self, **kwargs):
        cluster_info = {
            "name": "cluster 1",
            "info": {"gpu": 1},
            "optional_info": {"workers": 2},
        }
        yield self.conbench.benchmark(
            self._get_benchmark_function(),
            self.name,
            cluster_info=cluster_info,
            options=kwargs,
        )

    def _get_benchmark_function(self):
        return lambda: 1 * 2


@conbench.runner.register_benchmark
class CasesBenchmark(conbench.runner.Benchmark):
    """Example benchmark with cases."""

    name = "matrix"
    valid_cases = (
        ("rows", "columns"),
        ("10", "10"),
        ("2", "10"),
        ("10", "2"),
    )

    def run(self, case=None, **kwargs):
        for case in self.get_cases(case, kwargs):
            rows, columns = case
            tags = {"rows": rows, "columns": columns}
            func = self._get_benchmark_function(rows, columns)
            benchmark, output = self.conbench.benchmark(
                func,
                self.name,
                tags=tags,
                options=kwargs,
            )
            yield benchmark, output

    def _get_benchmark_function(self, rows, columns):
        return lambda: int(rows) * [int(columns) * [0]]


@conbench.runner.register_benchmark
class CasesBenchmarkTypeCasting(conbench.runner.Benchmark):
    """Example benchmark with cases."""

    name = "matrix-types"
    valid_cases = (
        ("rows", "columns", "flag"),
        (10, 10.0, False),
        (2, 2.0, False),
        (10, 10.0, True),
        (2, 2.0, True),
    )

    def run(self, case=None, **kwargs):
        for case in self.get_cases(case, kwargs):
            rows, columns, flag = case
            tags = {"rows": rows, "columns": columns, "flag": flag}
            func = self._get_benchmark_function(rows, columns, flag)
            benchmark, output = self.conbench.benchmark(
                func,
                self.name,
                tags=tags,
                options=kwargs,
            )
            yield benchmark, output

    def _get_benchmark_function(self, rows, columns, flag):
        return lambda: rows * [int(columns) * [flag]]


@conbench.runner.register_benchmark
class ExternalBenchmark(conbench.runner.Benchmark):
    """Example benchmark that just records external results."""

    external = True
    name = "external"

    def run(self, **kwargs):
        # external results from an API call, command line execution, etc
        result = {
            "data": [100, 200, 300],
            "unit": "i/s",
            "times": [0.100, 0.200, 0.300],
            "time_unit": "s",
        }

        context = {"benchmark_language": "C++"}
        yield self.conbench.record(
            result, self.name, context=context, options=kwargs, output=result
        )


@conbench.runner.register_benchmark
class DataAndErrorBenchmark(conbench.runner.Benchmark):
    """Example benchmark that supplies both data and an error."""

    external = True
    name = "data_and_error"

    def run(self, **kwargs):
        # external results from an API call, command line execution, etc
        result = {
            "data": [100, 200, 300],
            "unit": "i/s",
            "times": [0.100, 0.200, 0.300],
            "time_unit": "s",
        }

        context = {"benchmark_language": "C++"}
        yield self.conbench.record(
            result,
            self.name,
            error={"something": "bad"},
            context=context,
            options=kwargs,
            output=result,
        )


@conbench.runner.register_benchmark
class ExternalBenchmarkR(conbench.runner.Benchmark):
    """Example benchmark that records an R benchmark result."""

    external = True
    name = "external-r"

    def run(self, **kwargs):
        result, output = self._run_r_command()
        info, context = self.conbench.get_r_info_and_context()

        yield self.conbench.record(
            {"data": [result], "unit": "s"},
            self.name,
            info=info,
            context=context,
            options=kwargs,
            output=output,
        )

    def _run_r_command(self):
        output, _ = self.conbench.execute_r_command(self._get_r_command())
        result = float(output.split("\n")[-1].split("[1] ")[1])
        return result, output

    def _get_r_command(self):
        return (
            f"addition <- function() { 1 + 1 }; "
            "start_time <- Sys.time();"
            "addition(); "
            "end_time <- Sys.time(); "
            "result <- end_time - start_time; "
            "as.numeric(result); "
        )


@conbench.runner.register_benchmark
class ExternalBenchmarkOptionsR(conbench.runner.Benchmark):
    """Example benchmark that records an R benchmark result (with options)."""

    external = True
    name = "external-r-options"
    options = {
        "iterations": {"default": 1, "type": int},
        "drop_caches": {"type": bool, "default": "false"},
    }

    def run(self, **kwargs):
        data, iterations = [], kwargs.get("iterations", 1)
        info, context = self.conbench.get_r_info_and_context()

        for _ in range(iterations):
            if kwargs.get("drop_caches", False):
                self.conbench.sync_and_drop_caches()
            result, output = self._run_r_command()
            data.append(result["result"][0]["real"])

        yield self.conbench.record(
            {"data": data, "unit": "s"},
            self.name,
            info=info,
            context=context,
            options=kwargs,
            output=output,
        )

    def _run_r_command(self):
        r_command = self._get_r_command()
        self.conbench.execute_r_command(r_command)
        with open("placebo.json") as json_file:
            data = json.load(json_file)
        return data, json.dumps(data, indent=2)

    def _get_r_command(self):
        return (
            "library(arrowbench); "
            "out <- run_one(arrowbench:::placebo); "
            "cat(jsonlite::toJSON(out), file='placebo.json'); "
        )


# Overriding Conbench so it is possible to test what benchmark results are published
class TestConbench(conbench.runner.Conbench):
    def __init__(self):
        self.published_benchmark = None
        super().__init__()

    def publish(self, benchmark):
        self.published_benchmark = benchmark


@conbench.runner.register_benchmark
class SimpleBenchmarkThatFails(conbench.runner.Benchmark):
    name = "division-with-failure"

    def __init__(self):
        self.conbench = TestConbench()

    def run(self, **kwargs):
        yield self.conbench.benchmark(
            self._get_benchmark_function(), self.name, options=kwargs
        )

    def _get_benchmark_function(self):
        return lambda: 1 / 0


class ExternalBenchmarkWithWrongName(conbench.runner.Benchmark):
    """Example benchmark that uses a different name in tags than in record()."""

    external = True
    name = "some_name"

    def run(self, **kwargs):
        result = {
            "data": [100, 200, 300],
            "unit": "i/s",
            "times": [0.100, 0.200, 0.300],
            "time_unit": "s",
        }
        tags = {"name": "different_name"}

        context = {"benchmark_language": "C++"}
        yield self.conbench.record(
            result, self.name, context=context, options=kwargs, output=result, tags=tags
        )
