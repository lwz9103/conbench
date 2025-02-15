{
    "components": {
        "responses": {
            "200": {"description": "OK"},
            "201": {"description": "Created"},
            "202": {"description": "No Content (accepted)"},
            "204": {"description": "No Content (success)"},
            "302": {"description": "Found"},
            "400": {
                "content": {
                    "application/json": {
                        "example": {
                            "code": 400,
                            "description": {
                                "_errors": ["Empty request body."],
                                "_schema": [
                                    "Invalid input type.",
                                    "Did you specify Content-type: application/json?",
                                ],
                            },
                            "name": "Bad Request",
                        },
                        "schema": {"$ref": "#/components/schemas/ErrorBadRequest"},
                    }
                },
                "description": "Bad Request",
            },
            "401": {
                "content": {
                    "application/json": {
                        "example": {"code": 401, "name": "Unauthorized"},
                        "schema": {"$ref": "#/components/schemas/Error"},
                    }
                },
                "description": "Unauthorized",
            },
            "404": {
                "content": {
                    "application/json": {
                        "example": {"code": 404, "name": "Not Found"},
                        "schema": {"$ref": "#/components/schemas/Error"},
                    }
                },
                "description": "Not Found",
            },
            "BenchmarkEntity": {
                "content": {
                    "application/json": {
                        "example": {
                            "batch_id": "some-batch-uuid-1",
                            "change_annotations": {},
                            "error": None,
                            "id": "some-benchmark-uuid-1",
                            "links": {
                                "context": "http://localhost/api/contexts/some-context-uuid-1/",
                                "info": "http://localhost/api/info/some-info-uuid-1/",
                                "list": "http://localhost/api/benchmarks/",
                                "run": "http://localhost/api/runs/some-run-uuid-1/",
                                "self": "http://localhost/api/benchmarks/some-benchmark-uuid-1/",
                            },
                            "optional_benchmark_info": None,
                            "run_id": "some-run-uuid-1",
                            "stats": {
                                "data": [
                                    0.099094,
                                    0.037129,
                                    0.036381,
                                    0.148896,
                                    0.008104,
                                    0.005496,
                                    0.009871,
                                    0.006008,
                                    0.007978,
                                    0.004733,
                                ],
                                "iqr": 0.030441500000000003,
                                "iterations": 10,
                                "max": 0.148896,
                                "mean": 0.036369,
                                "median": 0.008987499999999999,
                                "min": 0.004733,
                                "q1": 0.0065005,
                                "q3": 0.036942,
                                "stdev": 0.04919372267316679,
                                "time_unit": "s",
                                "times": [
                                    0.099094,
                                    0.037129,
                                    0.036381,
                                    0.148896,
                                    0.008104,
                                    0.005496,
                                    0.009871,
                                    0.006008,
                                    0.007978,
                                    0.004733,
                                ],
                                "unit": "s",
                            },
                            "tags": {
                                "compression": "snappy",
                                "cpu_count": "2",
                                "dataset": "nyctaxi_sample",
                                "file_type": "parquet",
                                "input_type": "arrow",
                                "name": "file-write",
                            },
                            "timestamp": "2020-11-25T21:02:44Z",
                            "validation": None,
                        }
                    }
                },
                "description": "OK",
            },
            "BenchmarkList": {
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "batch_id": "some-batch-uuid-1",
                                "change_annotations": {},
                                "error": None,
                                "id": "some-benchmark-uuid-1",
                                "links": {
                                    "context": "http://localhost/api/contexts/some-context-uuid-1/",
                                    "info": "http://localhost/api/info/some-info-uuid-1/",
                                    "list": "http://localhost/api/benchmarks/",
                                    "run": "http://localhost/api/runs/some-run-uuid-1/",
                                    "self": "http://localhost/api/benchmarks/some-benchmark-uuid-1/",
                                },
                                "optional_benchmark_info": None,
                                "run_id": "some-run-uuid-1",
                                "stats": {
                                    "data": [
                                        0.099094,
                                        0.037129,
                                        0.036381,
                                        0.148896,
                                        0.008104,
                                        0.005496,
                                        0.009871,
                                        0.006008,
                                        0.007978,
                                        0.004733,
                                    ],
                                    "iqr": 0.030441500000000003,
                                    "iterations": 10,
                                    "max": 0.148896,
                                    "mean": 0.036369,
                                    "median": 0.008987499999999999,
                                    "min": 0.004733,
                                    "q1": 0.0065005,
                                    "q3": 0.036942,
                                    "stdev": 0.04919372267316679,
                                    "time_unit": "s",
                                    "times": [
                                        0.099094,
                                        0.037129,
                                        0.036381,
                                        0.148896,
                                        0.008104,
                                        0.005496,
                                        0.009871,
                                        0.006008,
                                        0.007978,
                                        0.004733,
                                    ],
                                    "unit": "s",
                                },
                                "tags": {
                                    "compression": "snappy",
                                    "cpu_count": "2",
                                    "dataset": "nyctaxi_sample",
                                    "file_type": "parquet",
                                    "input_type": "arrow",
                                    "name": "file-write",
                                },
                                "timestamp": "2020-11-25T21:02:44Z",
                                "validation": None,
                            }
                        ]
                    }
                },
                "description": "OK",
            },
            "BenchmarkResultCreated": {
                "content": {
                    "application/json": {
                        "example": {
                            "batch_id": "some-batch-uuid-1",
                            "change_annotations": {},
                            "error": None,
                            "id": "some-benchmark-uuid-1",
                            "links": {
                                "context": "http://localhost/api/contexts/some-context-uuid-1/",
                                "info": "http://localhost/api/info/some-info-uuid-1/",
                                "list": "http://localhost/api/benchmarks/",
                                "run": "http://localhost/api/runs/some-run-uuid-1/",
                                "self": "http://localhost/api/benchmarks/some-benchmark-uuid-1/",
                            },
                            "optional_benchmark_info": None,
                            "run_id": "some-run-uuid-1",
                            "stats": {
                                "data": [
                                    0.099094,
                                    0.037129,
                                    0.036381,
                                    0.148896,
                                    0.008104,
                                    0.005496,
                                    0.009871,
                                    0.006008,
                                    0.007978,
                                    0.004733,
                                ],
                                "iqr": 0.030441500000000003,
                                "iterations": 10,
                                "max": 0.148896,
                                "mean": 0.036369,
                                "median": 0.008987499999999999,
                                "min": 0.004733,
                                "q1": 0.0065005,
                                "q3": 0.036942,
                                "stdev": 0.04919372267316679,
                                "time_unit": "s",
                                "times": [
                                    0.099094,
                                    0.037129,
                                    0.036381,
                                    0.148896,
                                    0.008104,
                                    0.005496,
                                    0.009871,
                                    0.006008,
                                    0.007978,
                                    0.004733,
                                ],
                                "unit": "s",
                            },
                            "tags": {
                                "compression": "snappy",
                                "cpu_count": "2",
                                "dataset": "nyctaxi_sample",
                                "file_type": "parquet",
                                "input_type": "arrow",
                                "name": "file-write",
                            },
                            "timestamp": "2020-11-25T21:02:44Z",
                            "validation": None,
                        }
                    }
                },
                "description": "Created \n\n The resulting entity URL is returned in the Location header.",
            },
            "CommitEntity": {
                "content": {
                    "application/json": {
                        "example": {
                            "author_avatar": "https://avatars.githubusercontent.com/u/878798?v=4",
                            "author_login": "dianaclarke",
                            "author_name": "Diana Clarke",
                            "branch": "some_user_or_org:some_branch",
                            "fork_point_sha": "02addad336ba19a654f9c857ede546331be7b631",
                            "id": "some-commit-uuid-1",
                            "links": {
                                "list": "http://localhost/api/commits/",
                                "parent": "http://localhost/api/commits/some-commit-parent-uuid-1/",
                                "self": "http://localhost/api/commits/some-commit-uuid-1/",
                            },
                            "message": "ARROW-11771: [Developer][Archery] Move benchmark tests (so CI runs them)",
                            "parent_sha": "4beb514d071c9beec69b8917b5265e77ade22fb3",
                            "repository": "https://github.com/org/repo",
                            "sha": "02addad336ba19a654f9c857ede546331be7b631",
                            "timestamp": "2021-02-25T01:02:51",
                            "url": "https://github.com/org/repo/commit/02addad336ba19a654f9c857ede546331be7b631",
                        }
                    }
                },
                "description": "OK",
            },
            "CommitList": {
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "author_avatar": "https://avatars.githubusercontent.com/u/878798?v=4",
                                "author_login": "dianaclarke",
                                "author_name": "Diana Clarke",
                                "branch": "some_user_or_org:some_branch",
                                "fork_point_sha": "02addad336ba19a654f9c857ede546331be7b631",
                                "id": "some-commit-uuid-1",
                                "links": {
                                    "list": "http://localhost/api/commits/",
                                    "parent": "http://localhost/api/commits/some-commit-parent-uuid-1/",
                                    "self": "http://localhost/api/commits/some-commit-uuid-1/",
                                },
                                "message": "ARROW-11771: [Developer][Archery] Move benchmark tests (so CI runs them)",
                                "parent_sha": "4beb514d071c9beec69b8917b5265e77ade22fb3",
                                "repository": "https://github.com/org/repo",
                                "sha": "02addad336ba19a654f9c857ede546331be7b631",
                                "timestamp": "2021-02-25T01:02:51",
                                "url": "https://github.com/org/repo/commit/02addad336ba19a654f9c857ede546331be7b631",
                            }
                        ]
                    }
                },
                "description": "OK",
            },
            "CompareEntity": {
                "content": {
                    "application/json": {
                        "example": {
                            "analysis": {
                                "lookback_z_score": {
                                    "improvement_indicated": False,
                                    "regression_indicated": False,
                                    "z_score": 0.0,
                                    "z_threshold": 5.0,
                                },
                                "pairwise": {
                                    "improvement_indicated": False,
                                    "percent_change": 0.0,
                                    "percent_threshold": 5.0,
                                    "regression_indicated": False,
                                },
                            },
                            "baseline": {
                                "batch_id": "some-batch-uuid-1",
                                "benchmark_name": "file-read",
                                "benchmark_result_id": "some-benchmark-uuid-1",
                                "case_permutation": "snappy, nyctaxi_sample, parquet, arrow",
                                "error": None,
                                "language": "Python",
                                "run_id": "some-run-uuid-1",
                                "single_value_summary": 0.03637,
                                "tags": {
                                    "compression": "snappy",
                                    "cpu_count": "2",
                                    "dataset": "nyctaxi_sample",
                                    "file_type": "parquet",
                                    "input_type": "arrow",
                                    "name": "file-read",
                                },
                            },
                            "contender": {
                                "batch_id": "some-batch-uuid-2",
                                "benchmark_name": "file-read",
                                "benchmark_result_id": "some-benchmark-uuid-2",
                                "case_permutation": "snappy, nyctaxi_sample, parquet, arrow",
                                "error": None,
                                "language": "Python",
                                "run_id": "some-run-uuid-2",
                                "single_value_summary": 0.03637,
                                "tags": {
                                    "compression": "snappy",
                                    "cpu_count": "2",
                                    "dataset": "nyctaxi_sample",
                                    "file_type": "parquet",
                                    "input_type": "arrow",
                                    "name": "file-read",
                                },
                            },
                            "less_is_better": True,
                            "unit": "s",
                        }
                    }
                },
                "description": "OK",
            },
            "CompareList": {
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "analysis": {
                                    "lookback_z_score": {
                                        "improvement_indicated": False,
                                        "regression_indicated": False,
                                        "z_score": 0.0,
                                        "z_threshold": 5.0,
                                    },
                                    "pairwise": {
                                        "improvement_indicated": False,
                                        "percent_change": 0.0,
                                        "percent_threshold": 5.0,
                                        "regression_indicated": False,
                                    },
                                },
                                "baseline": {
                                    "batch_id": "some-batch-uuid-1",
                                    "benchmark_name": "file-read",
                                    "benchmark_result_id": "some-benchmark-uuid-1",
                                    "case_permutation": "snappy, nyctaxi_sample, parquet, arrow",
                                    "error": None,
                                    "language": "Python",
                                    "run_id": "some-run-uuid-1",
                                    "single_value_summary": 0.03637,
                                    "tags": {
                                        "compression": "snappy",
                                        "cpu_count": "2",
                                        "dataset": "nyctaxi_sample",
                                        "file_type": "parquet",
                                        "input_type": "arrow",
                                        "name": "file-read",
                                    },
                                },
                                "contender": {
                                    "batch_id": "some-batch-uuid-2",
                                    "benchmark_name": "file-read",
                                    "benchmark_result_id": "some-benchmark-uuid-3",
                                    "case_permutation": "snappy, nyctaxi_sample, parquet, arrow",
                                    "error": None,
                                    "language": "Python",
                                    "run_id": "some-run-uuid-2",
                                    "single_value_summary": 0.03637,
                                    "tags": {
                                        "compression": "snappy",
                                        "cpu_count": "2",
                                        "dataset": "nyctaxi_sample",
                                        "file_type": "parquet",
                                        "input_type": "arrow",
                                        "name": "file-read",
                                    },
                                },
                                "less_is_better": True,
                                "unit": "s",
                            },
                            {
                                "analysis": {
                                    "lookback_z_score": {
                                        "improvement_indicated": False,
                                        "regression_indicated": False,
                                        "z_score": 0.0,
                                        "z_threshold": 5.0,
                                    },
                                    "pairwise": {
                                        "improvement_indicated": False,
                                        "percent_change": 0.0,
                                        "percent_threshold": 5.0,
                                        "regression_indicated": False,
                                    },
                                },
                                "baseline": {
                                    "batch_id": "some-batch-uuid-1",
                                    "benchmark_name": "file-write",
                                    "benchmark_result_id": "some-benchmark-uuid-2",
                                    "case_permutation": "snappy, nyctaxi_sample, parquet, arrow",
                                    "error": None,
                                    "language": "Python",
                                    "run_id": "some-run-uuid-1",
                                    "single_value_summary": 0.03637,
                                    "tags": {
                                        "compression": "snappy",
                                        "cpu_count": "2",
                                        "dataset": "nyctaxi_sample",
                                        "file_type": "parquet",
                                        "input_type": "arrow",
                                        "name": "file-write",
                                    },
                                },
                                "contender": {
                                    "batch_id": "some-batch-uuid-2",
                                    "benchmark_name": "file-write",
                                    "benchmark_result_id": "some-benchmark-uuid-4",
                                    "case_permutation": "snappy, nyctaxi_sample, parquet, arrow",
                                    "error": None,
                                    "language": "Python",
                                    "run_id": "some-run-uuid-2",
                                    "single_value_summary": 0.03637,
                                    "tags": {
                                        "compression": "snappy",
                                        "cpu_count": "2",
                                        "dataset": "nyctaxi_sample",
                                        "file_type": "parquet",
                                        "input_type": "arrow",
                                        "name": "file-write",
                                    },
                                },
                                "less_is_better": True,
                                "unit": "s",
                            },
                        ]
                    }
                },
                "description": "OK",
            },
            "ContextEntity": {
                "content": {
                    "application/json": {
                        "example": {
                            "arrow_compiler_flags": "-fPIC -arch x86_64 -arch x86_64 -std=c++11 -Qunused-arguments -fcolor-diagnostics -O3 -DNDEBUG",
                            "benchmark_language": "Python",
                            "id": "some-context-uuid-1",
                            "links": {
                                "list": "http://localhost/api/contexts/",
                                "self": "http://localhost/api/contexts/some-context-uuid-1/",
                            },
                        }
                    }
                },
                "description": "OK",
            },
            "ContextList": {
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "arrow_compiler_flags": "-fPIC -arch x86_64 -arch x86_64 -std=c++11 -Qunused-arguments -fcolor-diagnostics -O3 -DNDEBUG",
                                "benchmark_language": "Python",
                                "id": "some-context-uuid-1",
                                "links": {
                                    "list": "http://localhost/api/contexts/",
                                    "self": "http://localhost/api/contexts/some-context-uuid-1/",
                                },
                            }
                        ]
                    }
                },
                "description": "OK",
            },
            "HardwareEntity": {
                "content": {
                    "application/json": {
                        "example": {
                            "architecture_name": "x86_64",
                            "cpu_core_count": 2,
                            "cpu_frequency_max_hz": 3500000000,
                            "cpu_l1d_cache_bytes": 32768,
                            "cpu_l1i_cache_bytes": 32768,
                            "cpu_l2_cache_bytes": 262144,
                            "cpu_l3_cache_bytes": 4194304,
                            "cpu_model_name": "Intel(R) Core(TM) i7-7567U CPU @ 3.50GHz",
                            "cpu_thread_count": 4,
                            "gpu_count": 2,
                            "gpu_product_names": ["Tesla T4", "GeForce GTX 1060 3GB"],
                            "id": "some-machine-uuid-1",
                            "kernel_name": "19.6.0",
                            "links": {
                                "list": "http://localhost/api/hardware/",
                                "self": "http://localhost/api/hardware/some-machine-uuid-1/",
                            },
                            "memory_bytes": 17179869184,
                            "name": "some-machine-name",
                            "os_name": "macOS",
                            "os_version": "10.15.7",
                            "type": "machine",
                        }
                    }
                },
                "description": "OK",
            },
            "HardwareList": {
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "architecture_name": "x86_64",
                                "cpu_core_count": 2,
                                "cpu_frequency_max_hz": 3500000000,
                                "cpu_l1d_cache_bytes": 32768,
                                "cpu_l1i_cache_bytes": 32768,
                                "cpu_l2_cache_bytes": 262144,
                                "cpu_l3_cache_bytes": 4194304,
                                "cpu_model_name": "Intel(R) Core(TM) i7-7567U CPU @ 3.50GHz",
                                "cpu_thread_count": 4,
                                "gpu_count": 2,
                                "gpu_product_names": [
                                    "Tesla T4",
                                    "GeForce GTX 1060 3GB",
                                ],
                                "id": "some-machine-uuid-1",
                                "kernel_name": "19.6.0",
                                "links": {
                                    "list": "http://localhost/api/hardware/",
                                    "self": "http://localhost/api/hardware/some-machine-uuid-1/",
                                },
                                "memory_bytes": 17179869184,
                                "name": "some-machine-name",
                                "os_name": "macOS",
                                "os_version": "10.15.7",
                                "type": "machine",
                            }
                        ]
                    }
                },
                "description": "OK",
            },
            "HistoryList": {
                "content": {
                    "application/json": {
                        "example": [
                            [
                                {
                                    "benchmark_result_id": "some-benchmark-uuid-1",
                                    "case_id": "some-case-uuid-1",
                                    "commit_hash": "02addad336ba19a654f9c857ede546331be7b631",
                                    "commit_msg": "ARROW-11771: [Developer][Archery] Move benchmark tests (so CI runs them)",
                                    "commit_timestamp": "2021-02-25T01:02:51",
                                    "context_id": "some-context-uuid-1",
                                    "data": [
                                        0.099094,
                                        0.037129,
                                        0.036381,
                                        0.148896,
                                        0.008104,
                                        0.005496,
                                        0.009871,
                                        0.006008,
                                        0.007978,
                                        0.004733,
                                    ],
                                    "hardware_hash": "diana-2-2-4-17179869184",
                                    "mean": 0.036369,
                                    "repository": "https://github.com/org/repo",
                                    "run_name": "some run name",
                                    "single_value_summary": 0.036369,
                                    "single_value_summary_type": "mean",
                                    "times": [
                                        0.099094,
                                        0.037129,
                                        0.036381,
                                        0.148896,
                                        0.008104,
                                        0.005496,
                                        0.009871,
                                        0.006008,
                                        0.007978,
                                        0.004733,
                                    ],
                                    "unit": "s",
                                    "zscorestats": {
                                        "begins_distribution_change": False,
                                        "is_outlier": False,
                                        "residual": 0.0,
                                        "rolling_mean": 0.036369,
                                        "rolling_mean_excluding_this_commit": 0.036369,
                                        "rolling_stddev": 0.0,
                                        "segment_id": 0.0,
                                    },
                                }
                            ]
                        ]
                    }
                },
                "description": "OK",
            },
            "Index": {
                "content": {
                    "application/json": {
                        "example": {
                            "links": {
                                "benchmarks": "http://localhost/api/benchmarks/",
                                "commits": "http://localhost/api/commits/",
                                "contexts": "http://localhost/api/contexts/",
                                "docs": "http://localhost/api/docs.json",
                                "hardware": "http://localhost/api/hardware/",
                                "info": "http://localhost/api/info/",
                                "login": "http://localhost/api/login/",
                                "logout": "http://localhost/api/logout/",
                                "ping": "http://localhost/api/ping/",
                                "register": "http://localhost/api/register/",
                                "runs": "http://localhost/api/runs/",
                                "users": "http://localhost/api/users/",
                            }
                        }
                    }
                },
                "description": "OK",
            },
            "InfoEntity": {
                "content": {
                    "application/json": {
                        "example": {
                            "arrow_compiler_id": "AppleClang",
                            "arrow_compiler_version": "11.0.0.11000033",
                            "arrow_version": "2.0.0",
                            "benchmark_language_version": "Python 3.8.5",
                            "id": "some-info-uuid-1",
                            "links": {
                                "list": "http://localhost/api/info/",
                                "self": "http://localhost/api/info/some-info-uuid-1/",
                            },
                        }
                    }
                },
                "description": "OK",
            },
            "InfoList": {
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "arrow_compiler_id": "AppleClang",
                                "arrow_compiler_version": "11.0.0.11000033",
                                "arrow_version": "2.0.0",
                                "benchmark_language_version": "Python 3.8.5",
                                "id": "some-info-uuid-1",
                                "links": {
                                    "list": "http://localhost/api/info/",
                                    "self": "http://localhost/api/info/some-info-uuid-1/",
                                },
                            }
                        ]
                    }
                },
                "description": "OK",
            },
            "Ping": {
                "content": {
                    "application/json": {
                        "example": {
                            "alembic_version": "0d4e564b1876",
                            "date": "Thu, 22 Oct 2020 15:53:55 UTC",
                        },
                        "schema": {"$ref": "#/components/schemas/Ping"},
                    }
                },
                "description": "OK",
            },
            "RunCreated": {
                "content": {
                    "application/json": {
                        "example": {
                            "commit": {
                                "author_avatar": "https://avatars.githubusercontent.com/u/878798?v=4",
                                "author_login": "dianaclarke",
                                "author_name": "Diana Clarke",
                                "branch": "some_user_or_org:some_branch",
                                "fork_point_sha": "02addad336ba19a654f9c857ede546331be7b631",
                                "id": "some-commit-uuid-1",
                                "message": "ARROW-11771: [Developer][Archery] Move benchmark tests (so CI runs them)",
                                "parent_sha": "4beb514d071c9beec69b8917b5265e77ade22fb3",
                                "repository": "https://github.com/org/repo",
                                "sha": "02addad336ba19a654f9c857ede546331be7b631",
                                "timestamp": "2021-02-25T01:02:51",
                                "url": "https://github.com/org/repo/commit/02addad336ba19a654f9c857ede546331be7b631",
                            },
                            "error_info": None,
                            "error_type": None,
                            "finished_timestamp": None,
                            "hardware": {
                                "architecture_name": "x86_64",
                                "cpu_core_count": 2,
                                "cpu_frequency_max_hz": 3500000000,
                                "cpu_l1d_cache_bytes": 32768,
                                "cpu_l1i_cache_bytes": 32768,
                                "cpu_l2_cache_bytes": 262144,
                                "cpu_l3_cache_bytes": 4194304,
                                "cpu_model_name": "Intel(R) Core(TM) i7-7567U CPU @ 3.50GHz",
                                "cpu_thread_count": 4,
                                "gpu_count": 2,
                                "gpu_product_names": [
                                    "Tesla T4",
                                    "GeForce GTX 1060 3GB",
                                ],
                                "id": "some-machine-uuid-1",
                                "kernel_name": "19.6.0",
                                "memory_bytes": 17179869184,
                                "name": "some-machine-name",
                                "os_name": "macOS",
                                "os_version": "10.15.7",
                                "type": "machine",
                            },
                            "has_errors": False,
                            "id": "some-run-uuid-1",
                            "info": None,
                            "links": {
                                "commit": "http://localhost/api/commits/some-commit-uuid-1/",
                                "hardware": "http://localhost/api/hardware/some-machine-uuid-1/",
                                "list": "http://localhost/api/runs/",
                                "self": "http://localhost/api/runs/some-run-uuid-1/",
                            },
                            "name": "some run name",
                            "reason": "some run reason",
                            "timestamp": "2021-02-04T17:22:05.225583",
                        }
                    }
                },
                "description": "Created \n\n The resulting entity URL is returned in the Location header.",
            },
            "RunEntityWithBaselines": {
                "content": {
                    "application/json": {
                        "example": {
                            "candidate_baseline_runs": {
                                "fork_point": {
                                    "baseline_run_id": None,
                                    "commits_skipped": None,
                                    "error": "the contender run is already on the default branch",
                                },
                                "latest_default": {
                                    "baseline_run_id": None,
                                    "commits_skipped": None,
                                    "error": "the contender run is already on the default branch",
                                },
                                "parent": {
                                    "baseline_run_id": "598b44a1a3c94c63a4b17330c82c899e",
                                    "commits_skipped": [
                                        "7376b33c03298f273b9120ad83dd05da3d0c3bef"
                                    ],
                                    "error": None,
                                },
                            },
                            "commit": {
                                "author_avatar": "https://avatars.githubusercontent.com/u/878798?v=4",
                                "author_login": "dianaclarke",
                                "author_name": "Diana Clarke",
                                "branch": "some_user_or_org:some_branch",
                                "fork_point_sha": "02addad336ba19a654f9c857ede546331be7b631",
                                "id": "some-commit-uuid-1",
                                "message": "ARROW-11771: [Developer][Archery] Move benchmark tests (so CI runs them)",
                                "parent_sha": "4beb514d071c9beec69b8917b5265e77ade22fb3",
                                "repository": "https://github.com/org/repo",
                                "sha": "02addad336ba19a654f9c857ede546331be7b631",
                                "timestamp": "2021-02-25T01:02:51",
                                "url": "https://github.com/org/repo/commit/02addad336ba19a654f9c857ede546331be7b631",
                            },
                            "error_info": None,
                            "error_type": None,
                            "finished_timestamp": None,
                            "hardware": {
                                "architecture_name": "x86_64",
                                "cpu_core_count": 2,
                                "cpu_frequency_max_hz": 3500000000,
                                "cpu_l1d_cache_bytes": 32768,
                                "cpu_l1i_cache_bytes": 32768,
                                "cpu_l2_cache_bytes": 262144,
                                "cpu_l3_cache_bytes": 4194304,
                                "cpu_model_name": "Intel(R) Core(TM) i7-7567U CPU @ 3.50GHz",
                                "cpu_thread_count": 4,
                                "gpu_count": 2,
                                "gpu_product_names": [
                                    "Tesla T4",
                                    "GeForce GTX 1060 3GB",
                                ],
                                "id": "some-machine-uuid-1",
                                "kernel_name": "19.6.0",
                                "memory_bytes": 17179869184,
                                "name": "some-machine-name",
                                "os_name": "macOS",
                                "os_version": "10.15.7",
                                "type": "machine",
                            },
                            "has_errors": False,
                            "id": "some-run-uuid-1",
                            "info": None,
                            "links": {
                                "commit": "http://localhost/api/commits/some-commit-uuid-1/",
                                "hardware": "http://localhost/api/hardware/some-machine-uuid-1/",
                                "list": "http://localhost/api/runs/",
                                "self": "http://localhost/api/runs/some-run-uuid-1/",
                            },
                            "name": "some run name",
                            "reason": "some run reason",
                            "timestamp": "2021-02-04T17:22:05.225583",
                        }
                    }
                },
                "description": "OK",
            },
            "RunEntityWithoutBaselines": {
                "content": {
                    "application/json": {
                        "example": {
                            "commit": {
                                "author_avatar": "https://avatars.githubusercontent.com/u/878798?v=4",
                                "author_login": "dianaclarke",
                                "author_name": "Diana Clarke",
                                "branch": "some_user_or_org:some_branch",
                                "fork_point_sha": "02addad336ba19a654f9c857ede546331be7b631",
                                "id": "some-commit-uuid-1",
                                "message": "ARROW-11771: [Developer][Archery] Move benchmark tests (so CI runs them)",
                                "parent_sha": "4beb514d071c9beec69b8917b5265e77ade22fb3",
                                "repository": "https://github.com/org/repo",
                                "sha": "02addad336ba19a654f9c857ede546331be7b631",
                                "timestamp": "2021-02-25T01:02:51",
                                "url": "https://github.com/org/repo/commit/02addad336ba19a654f9c857ede546331be7b631",
                            },
                            "error_info": None,
                            "error_type": None,
                            "finished_timestamp": None,
                            "hardware": {
                                "architecture_name": "x86_64",
                                "cpu_core_count": 2,
                                "cpu_frequency_max_hz": 3500000000,
                                "cpu_l1d_cache_bytes": 32768,
                                "cpu_l1i_cache_bytes": 32768,
                                "cpu_l2_cache_bytes": 262144,
                                "cpu_l3_cache_bytes": 4194304,
                                "cpu_model_name": "Intel(R) Core(TM) i7-7567U CPU @ 3.50GHz",
                                "cpu_thread_count": 4,
                                "gpu_count": 2,
                                "gpu_product_names": [
                                    "Tesla T4",
                                    "GeForce GTX 1060 3GB",
                                ],
                                "id": "some-machine-uuid-1",
                                "kernel_name": "19.6.0",
                                "memory_bytes": 17179869184,
                                "name": "some-machine-name",
                                "os_name": "macOS",
                                "os_version": "10.15.7",
                                "type": "machine",
                            },
                            "has_errors": False,
                            "id": "some-run-uuid-1",
                            "info": None,
                            "links": {
                                "commit": "http://localhost/api/commits/some-commit-uuid-1/",
                                "hardware": "http://localhost/api/hardware/some-machine-uuid-1/",
                                "list": "http://localhost/api/runs/",
                                "self": "http://localhost/api/runs/some-run-uuid-1/",
                            },
                            "name": "some run name",
                            "reason": "some run reason",
                            "timestamp": "2021-02-04T17:22:05.225583",
                        }
                    }
                },
                "description": "OK",
            },
            "RunList": {
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "commit": {
                                    "author_avatar": "https://avatars.githubusercontent.com/u/878798?v=4",
                                    "author_login": "dianaclarke",
                                    "author_name": "Diana Clarke",
                                    "branch": "some_user_or_org:some_branch",
                                    "fork_point_sha": "02addad336ba19a654f9c857ede546331be7b631",
                                    "id": "some-commit-uuid-1",
                                    "message": "ARROW-11771: [Developer][Archery] Move benchmark tests (so CI runs them)",
                                    "parent_sha": "4beb514d071c9beec69b8917b5265e77ade22fb3",
                                    "repository": "https://github.com/org/repo",
                                    "sha": "02addad336ba19a654f9c857ede546331be7b631",
                                    "timestamp": "2021-02-25T01:02:51",
                                    "url": "https://github.com/org/repo/commit/02addad336ba19a654f9c857ede546331be7b631",
                                },
                                "error_info": None,
                                "error_type": None,
                                "finished_timestamp": None,
                                "hardware": {
                                    "architecture_name": "x86_64",
                                    "cpu_core_count": 2,
                                    "cpu_frequency_max_hz": 3500000000,
                                    "cpu_l1d_cache_bytes": 32768,
                                    "cpu_l1i_cache_bytes": 32768,
                                    "cpu_l2_cache_bytes": 262144,
                                    "cpu_l3_cache_bytes": 4194304,
                                    "cpu_model_name": "Intel(R) Core(TM) i7-7567U CPU @ 3.50GHz",
                                    "cpu_thread_count": 4,
                                    "gpu_count": 2,
                                    "gpu_product_names": [
                                        "Tesla T4",
                                        "GeForce GTX 1060 3GB",
                                    ],
                                    "id": "some-machine-uuid-1",
                                    "kernel_name": "19.6.0",
                                    "memory_bytes": 17179869184,
                                    "name": "some-machine-name",
                                    "os_name": "macOS",
                                    "os_version": "10.15.7",
                                    "type": "machine",
                                },
                                "has_errors": False,
                                "id": "some-run-uuid-1",
                                "info": None,
                                "links": {
                                    "commit": "http://localhost/api/commits/some-commit-uuid-1/",
                                    "hardware": "http://localhost/api/hardware/some-machine-uuid-1/",
                                    "list": "http://localhost/api/runs/",
                                    "self": "http://localhost/api/runs/some-run-uuid-1/",
                                },
                                "name": "some run name",
                                "reason": "some run reason",
                                "timestamp": "2021-02-04T17:22:05.225583",
                            }
                        ]
                    }
                },
                "description": "OK",
            },
            "UserCreated": {
                "content": {
                    "application/json": {
                        "example": {
                            "email": "gwen@example.com",
                            "id": "some-user-uuid-1",
                            "links": {
                                "list": "http://localhost/api/users/",
                                "self": "http://localhost/api/users/some-user-uuid-1/",
                            },
                            "name": "Gwen Clarke",
                        }
                    }
                },
                "description": "Created \n\n The resulting entity URL is returned in the Location header.",
            },
            "UserEntity": {
                "content": {
                    "application/json": {
                        "example": {
                            "email": "gwen@example.com",
                            "id": "some-user-uuid-1",
                            "links": {
                                "list": "http://localhost/api/users/",
                                "self": "http://localhost/api/users/some-user-uuid-1/",
                            },
                            "name": "Gwen Clarke",
                        }
                    }
                },
                "description": "OK",
            },
            "UserList": {
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "email": "gwen@example.com",
                                "id": "some-user-uuid-1",
                                "links": {
                                    "list": "http://localhost/api/users/",
                                    "self": "http://localhost/api/users/some-user-uuid-1/",
                                },
                                "name": "Gwen Clarke",
                            },
                            {
                                "email": "casey@example.com",
                                "id": "some-user-uuid-2",
                                "links": {
                                    "list": "http://localhost/api/users/",
                                    "self": "http://localhost/api/users/some-user-uuid-2/",
                                },
                                "name": "Casey Clarke",
                            },
                        ]
                    }
                },
                "description": "OK",
            },
        },
        "schemas": {
            "BenchmarkResultCreate": {
                "properties": {
                    "batch_id": {"type": "string"},
                    "change_annotations": {
                        "description": 'Post-analysis annotations about this BenchmarkResult that\ngive details about whether it represents a change, outlier, etc. in the overall\ndistribution of BenchmarkResults.\n\nCurrently-recognized keys that change Conbench behavior:\n\n- `begins_distribution_change` (bool) - Is this result the first result of a sufficiently\n"different" distribution than the result on the previous commit (for the same\nhardware/case/context)? That is, when evaluating whether future results are regressions\nor improvements, should we treat data from before this result as incomparable?\n',
                        "type": "object",
                    },
                    "cluster_info": {
                        "allOf": [{"$ref": "#/components/schemas/ClusterCreate"}],
                        "description": "Precisely one of `machine_info` and `cluster_info` must be provided. The data is however ignored when the Run (referred to by `run_id`) was previously created.",
                    },
                    "context": {
                        "description": "Information about the context the benchmark was run in (e.g. compiler flags, benchmark langauge) that are reasonably expected to have an impact on benchmark performance. This information is expected to be the same across a number of benchmarks. (free-form JSON)",
                        "type": "object",
                    },
                    "error": {
                        "description": 'Details about an error that occurred while the benchmark was running (free-form JSON).  You may populate both this field and the "data" field of the "stats" object. In that case, the "data" field measures the metric\'s values before the error occurred. Those values will not be compared to non-errored values in analyses and comparisons.',
                        "type": "object",
                    },
                    "github": {"$ref": "#/components/schemas/SchemaGitHubCreate"},
                    "info": {
                        "description": "Additional information about the context the benchmark was run in that is not expected to have an impact on benchmark performance (e.g. benchmark language version, compiler version). This information is expected to be the same across a number of benchmarks. (free-form JSON)",
                        "type": "object",
                    },
                    "machine_info": {
                        "allOf": [{"$ref": "#/components/schemas/MachineCreate"}],
                        "description": "Precisely one of `machine_info` and `cluster_info` must be provided. The data is however ignored when the Run (referred to by `run_id`) was previously created.",
                    },
                    "optional_benchmark_info": {
                        "description": "Optional information about Benchmark results (e.g., telemetry links, logs links). These are unique to each benchmark that is run, but are information that aren't reasonably expected to impact benchmark performance. Helpful for adding debugging or additional links and context for a benchmark (free-form JSON)",
                        "type": "object",
                    },
                    "run_id": {
                        "description": "Identifier for a Run (required). This can be the ID of a known Run (as returned by /api/runs) or a new ID in which case a new Run entity is created in the database.",
                        "type": "string",
                    },
                    "run_name": {
                        "description": "Name for the Run (optional, does not need to be unique). Can be useful for implementing a custom naming convention. For organizing your benchmarks, and for enhanced search & discoverability. Ignored when Run was previously created.",
                        "type": "string",
                    },
                    "run_reason": {
                        "description": "Reason for the Run (optional, does not need to be unique). Ignored when Run was previously created.",
                        "type": "string",
                    },
                    "stats": {"$ref": "#/components/schemas/BenchmarkResultStats"},
                    "tags": {
                        "description": 'The set of key/value pairs that represents a specific benchmark case permutation (a specific set of parameters).  Keys must be non-empty strings. Values should be non-empty strings.  The special key "name" must be provided with a string value: it indicates the name of the conceptual benchmark that was performed for obtaining the result at hand. All case permutations of a conceptual benchmark by definition have this name in common.  Example: a conceptual benchmark with name "foo-write-file" might have meaningful case permutations involving tag names such as `compression-method` (values: `gzip`, `lzma`, ...), `file-format` (values: `csv`, `hdf5`, ...), `dataset-name` (values: `foo`, `bar`, ...).  For each conceptual benchmark, it is valid to have one or many case permutations (if you supply only "name", then there is necessarily a single mutation with the special property that it has no other tags set).  We advise that each unique case (as defined by the complete set of key/value pairs) indeed corresponds to unique benchmarking behavior. That is, typically, all key/value pairs other than "name" directly correspond to input parameters to the same conceptual benchmark. Note however that Conbench benchmark result tags are not meant to store type information. Benchmark authors are advised to find a custom convention for mapping benchmark input parameters to tags.  Currently, primitive value types (int, float, boolean) are accepted, but stored as strings. Keys with empty string values or null values are ignored. In the future, Conbench might disallow all non-string values.',
                        "type": "object",
                    },
                    "timestamp": {
                        "description": "A datetime string indicating the time at which the benchmark was started. Expected to be in ISO 8601 notation. Timezone-aware notation recommended. Timezone-naive strings are interpreted in UTC. Fractions of seconds can be provided but are not returned by the API. Example value: 2022-11-25T22:02:42Z. This timestamp defines the default sorting order when viewing a list of benchmarks via the UI or when enumerating benchmarks via the /api/benchmarks/ HTTP endpoint.",
                        "format": "date-time",
                        "type": "string",
                    },
                    "validation": {
                        "description": "Benchmark results validation metadata (e.g., errors, validation types).",
                        "type": "object",
                    },
                },
                "required": [
                    "batch_id",
                    "context",
                    "info",
                    "run_id",
                    "tags",
                    "timestamp",
                ],
                "type": "object",
            },
            "BenchmarkResultStats": {
                "properties": {
                    "data": {
                        "description": "A list of benchmark results (e.g. durations, throughput). This will be used as the main + only metric for regression and improvement. The values should be ordered in the order the iterations were executed (the first element is the first iteration, the second element is the second iteration, etc.). If an iteration did not complete but others did and you want to send partial data, mark each iteration that didn't complete as `null`.  You may populate both this field and the \"error\" field in the top level of the benchmark result payload. In that case, this field measures the metric's values before the error occurred. These values will not be compared to non-errored values in analyses and comparisons.",
                        "items": {"nullable": True, "type": "number"},
                        "type": "array",
                    },
                    "iqr": {
                        "description": "The inter-quartile range from `data`, will be calculated on the server if not present (the preferred method), but can be overridden if sent. Will be marked `null` if any iterations are missing.",
                        "type": "number",
                    },
                    "iterations": {
                        "description": "Number of iterations that were executed (should be the length of `data` and `times`)",
                        "type": "integer",
                    },
                    "max": {
                        "description": "The maximum from `data`, will be calculated on the server if not present (the preferred method), but can be overridden if sent. Will be marked `null` if any iterations are missing.",
                        "type": "number",
                    },
                    "mean": {
                        "description": "The mean from `data`, will be calculated on the server if not present (the preferred method), but can be overridden if sent. Will be marked `null` if any iterations are missing.",
                        "type": "number",
                    },
                    "median": {
                        "description": "The median from `data`, will be calculated on the server if not present (the preferred method), but can be overridden if sent. Will be marked `null` if any iterations are missing.",
                        "type": "number",
                    },
                    "min": {
                        "description": "The minimum from `data`, will be calculated on the server if not present (the preferred method), but can be overridden if sent. Will be marked `null` if any iterations are missing.",
                        "type": "number",
                    },
                    "q1": {
                        "description": "The first quartile from `data`, will be calculated on the server if not present (the preferred method), but can be overridden if sent. Will be marked `null` if any iterations are missing.",
                        "type": "number",
                    },
                    "q3": {
                        "description": "The third quartile from `data`, will be calculated on the server if not present (the preferred method), but can be overridden if sent. Will be marked `null` if any iterations are missing.",
                        "type": "number",
                    },
                    "stdev": {
                        "description": "The standard deviation from `data`, will be calculated on the server if not present (the preferred method), but can be overridden if sent. Will be marked `null` if any iterations are missing.",
                        "type": "number",
                    },
                    "time_unit": {
                        "description": "The unit of the times object (e.g. seconds, nanoseconds)",
                        "type": "string",
                    },
                    "times": {
                        "description": 'A list of benchmark durations. If `data` is a duration measure, this should be a duplicate of that object. The values should be ordered in the order the iterations were executed (the first element is the first iteration, the second element is the second iteration, etc.). If an iteration did not complete but others did and you want to send partial data, mark each iteration that didn\'t complete as `null`.  You may populate both this field and the "error" field in the top level of the benchmark result payload. In that case, this field measures how long the benchmark took to run before the error occurred. These values will not be compared to non-errored values in analyses and comparisons.',
                        "items": {"nullable": True, "type": "number"},
                        "type": "array",
                    },
                    "unit": {
                        "description": "The unit of the data object (e.g. seconds, B/s)",
                        "type": "string",
                    },
                },
                "required": ["data", "iterations", "time_unit", "times", "unit"],
                "type": "object",
            },
            "BenchmarkResultUpdate": {
                "properties": {
                    "change_annotations": {
                        "description": 'Post-analysis annotations about this BenchmarkResult that\ngive details about whether it represents a change, outlier, etc. in the overall\ndistribution of BenchmarkResults.\n\nCurrently-recognized keys that change Conbench behavior:\n\n- `begins_distribution_change` (bool) - Is this result the first result of a sufficiently\n"different" distribution than the result on the previous commit (for the same\nhardware/case/context)? That is, when evaluating whether future results are regressions\nor improvements, should we treat data from before this result as incomparable?\n\n\nThis endpoint will only update the user-specified keys, and leave the rest alone. To\ndelete an existing key, set the value to null.\n',
                        "type": "object",
                    }
                },
                "type": "object",
            },
            "ClusterCreate": {
                "properties": {
                    "info": {
                        "description": "Information related to cluster (e.g. `hosts`, `nodes` or `number of workers`) configured to run a set of benchmarks. Used to differentiate between similar benchmark runs performed on different sets of hardware",
                        "type": "object",
                    },
                    "name": {
                        "description": "Distinct name of the cluster, to be displayed on the web UI.",
                        "type": "string",
                    },
                    "optional_info": {
                        "description": "Additional optional information about the cluster, which is not likely to impact the benchmark performance (e.g. region, settings like logging type, etc). Despite the name, this field is required. An empty dictionary can be passed.",
                        "type": "object",
                    },
                },
                "required": ["info", "name", "optional_info"],
                "type": "object",
            },
            "Error": {
                "additionalProperties": True,
                "properties": {
                    "code": {"description": "HTTP error code", "type": "integer"},
                    "name": {"description": "HTTP error name", "type": "string"},
                },
                "required": ["code", "name"],
                "type": "object",
            },
            "ErrorBadRequest": {
                "additionalProperties": True,
                "properties": {
                    "code": {"description": "HTTP error code", "type": "integer"},
                    "description": {
                        "allOf": [{"$ref": "#/components/schemas/ErrorValidation"}],
                        "description": "Additional information about the bad request",
                    },
                    "name": {"description": "HTTP error name", "type": "string"},
                },
                "required": ["code", "name"],
                "type": "object",
            },
            "ErrorValidation": {
                "properties": {
                    "_errors": {
                        "description": "Validation error messages",
                        "items": {"type": "string"},
                        "type": "array",
                    },
                    "_schema": {
                        "description": "Schema error messages",
                        "items": {"type": "string"},
                        "type": "array",
                    },
                },
                "type": "object",
            },
            "Login": {
                "properties": {
                    "email": {"format": "email", "type": "string"},
                    "password": {"type": "string"},
                },
                "required": ["email", "password"],
                "type": "object",
            },
            "MachineCreate": {
                "properties": {
                    "architecture_name": {"type": "string"},
                    "cpu_core_count": {"type": "integer"},
                    "cpu_frequency_max_hz": {"type": "integer"},
                    "cpu_l1d_cache_bytes": {"type": "integer"},
                    "cpu_l1i_cache_bytes": {"type": "integer"},
                    "cpu_l2_cache_bytes": {"type": "integer"},
                    "cpu_l3_cache_bytes": {"type": "integer"},
                    "cpu_model_name": {"type": "string"},
                    "cpu_thread_count": {"type": "integer"},
                    "gpu_count": {"type": "integer"},
                    "gpu_product_names": {"items": {"type": "string"}, "type": "array"},
                    "kernel_name": {"type": "string"},
                    "memory_bytes": {"type": "integer"},
                    "name": {"type": "string"},
                    "os_name": {"type": "string"},
                    "os_version": {"type": "string"},
                },
                "required": [
                    "architecture_name",
                    "cpu_core_count",
                    "cpu_frequency_max_hz",
                    "cpu_l1d_cache_bytes",
                    "cpu_l1i_cache_bytes",
                    "cpu_l2_cache_bytes",
                    "cpu_l3_cache_bytes",
                    "cpu_model_name",
                    "cpu_thread_count",
                    "gpu_count",
                    "gpu_product_names",
                    "kernel_name",
                    "memory_bytes",
                    "name",
                    "os_name",
                    "os_version",
                ],
                "type": "object",
            },
            "Ping": {
                "properties": {
                    "date": {
                        "description": "Current date & time",
                        "format": "date-time",
                        "type": "string",
                    }
                },
                "required": ["date"],
                "type": "object",
            },
            "Register": {
                "properties": {
                    "email": {"format": "email", "type": "string"},
                    "name": {"type": "string"},
                    "password": {"type": "string"},
                    "secret": {"type": "string"},
                },
                "required": ["email", "name", "password", "secret"],
                "type": "object",
            },
            "RunCreate": {
                "properties": {
                    "cluster_info": {"$ref": "#/components/schemas/ClusterCreate"},
                    "error_info": {
                        "description": "Metadata for run's error that prevented all or some benchmarks from running",
                        "type": "object",
                    },
                    "error_type": {
                        "description": "Run's error type. Possible values: none, catastrophic, partial.\n                    None = all attempted benchmarks are good.\n                    Catastrophic =no benchmarks completed successfully.\n                    Partial = some benchmarks completed, some failed",
                        "type": "string",
                    },
                    "finished_timestamp": {
                        "description": "A datetime string indicating the time at which the run finished. Expected to be in ISO 8601 notation. Timezone-aware notation recommended. Timezone-naive strings are interpreted in UTC. Fractions of seconds can be provided but are not returned by the API. Example value: 2022-11-25T22:02:42Z",
                        "format": "date-time",
                        "type": "string",
                    },
                    "github": {
                        "allOf": [{"$ref": "#/components/schemas/SchemaGitHubCreate"}],
                        "description": "Use this object to tell Conbench with which commit the Run/BenchmarkResult is associated.  This field can be left out for testing purposes. Note however that commit information is required for powering valuable Conbench capabilities.",
                    },
                    "id": {"type": "string"},
                    "info": {"description": "Run's metadata", "type": "object"},
                    "machine_info": {"$ref": "#/components/schemas/MachineCreate"},
                    "name": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "required": ["id"],
                "type": "object",
            },
            "RunUpdate": {
                "properties": {
                    "error_info": {
                        "description": "Metadata for run's error that prevented all or some benchmarks from running",
                        "type": "object",
                    },
                    "error_type": {
                        "description": "Run's error type. Possible values: none, catastrophic, partial.\n                    None = all attempted benchmarks are good.\n                    Catastrophic =no benchmarks completed successfully.\n                    Partial = some benchmarks completed, some failed",
                        "type": "string",
                    },
                    "finished_timestamp": {
                        "description": "A datetime string indicating the time at which the run finished. Expected to be in ISO 8601 notation. Timezone-aware notation recommended. Timezone-naive strings are interpreted in UTC. Fractions of seconds can be provided but are not returned by the API. Example value: 2022-11-25T22:02:42Z",
                        "format": "date-time",
                        "type": "string",
                    },
                    "info": {"description": "Run's metadata", "type": "object"},
                },
                "type": "object",
            },
            "SchemaGitHubCreate": {
                "properties": {
                    "branch": {
                        "description": "This is an alternative way to indicate that this benchmark result has been obtained for a commit that is not on the default branch. Do not use this for GitHub pull requests (use the `pr_number` argument for that, see above).  If set, this needs to be a string of the form `org:branch`.  Warning: currently, if `branch` and `pr_number` are both provided, there is no error and `branch` takes precedence. Only use this when you know what you are doing.",
                        "nullable": True,
                        "type": "string",
                    },
                    "commit": {
                        "description": "The commit hash of the benchmarked code.  Must not be an empty string.  Expected to be a known commit in the repository as specified by the `repository` URL property below.",
                        "type": "string",
                    },
                    "pr_number": {
                        "description": "If set, this needs to be an integer or a stringified integer.  This is the recommended way to indicate that this benchmark result has been obtained for a specific pull request branch. Conbench will use this pull request number to (try to) obtain branch information via the GitHub HTTP API.  Set this to `null` or leave this out to indicate that this benchmark result has been obtained for the default branch.",
                        "nullable": True,
                        "type": "integer",
                    },
                    "repository": {
                        "description": 'URL pointing to the benchmarked GitHub repository.  Must be provided in the format https://github.com/org/repo.  Trailing slashes are stripped off before database insertion.  As of the time of writing, only URLs starting with "https://github.com" are allowed. Conbench interacts with the GitHub HTTP API in order to fetch information about the benchmarked repository. The Conbench user/operator is expected to ensure that Conbench is configured with a GitHub HTTP API authentication token that is privileged to read commit information for the repository specified here.  Support for non-GitHub repositories (e.g. GitLab) or auxiliary repositories is interesting, but not yet well specified.',
                        "type": "string",
                    },
                },
                "required": ["commit", "repository"],
                "type": "object",
            },
            "UserCreate": {
                "properties": {
                    "email": {"format": "email", "type": "string"},
                    "name": {"type": "string"},
                    "password": {"type": "string"},
                },
                "required": ["email", "name", "password"],
                "type": "object",
            },
            "UserUpdate": {
                "properties": {
                    "email": {"format": "email", "type": "string"},
                    "name": {"type": "string"},
                    "password": {"type": "string"},
                },
                "type": "object",
            },
        },
    },
    "info": {"title": "local-dev-conbench", "version": "1.0.0"},
    "openapi": "3.0.2",
    "paths": {
        "/api/": {
            "get": {
                "description": "Get a list of API endpoints.",
                "responses": {
                    "200": {"$ref": "#/components/responses/Index"},
                    "401": {"$ref": "#/components/responses/401"},
                },
                "tags": ["Index"],
            }
        },
        "/api/benchmarks/": {
            "get": {
                "description": "Return a JSON array of benchmark results.\n\nNote that this endpoint does not provide on-the-fly change\ndetection analysis (lookback z-score method).\n\nBehavior at the time of writing (subject to change):\n\nBenchmark results are usually returned in order of their\ntimestamp property (user-given benchmark start time), newest first.\n\nWhen no argument is provided, the last 1000 benchmark results\nare emitted.\n\nThe `run_id` argument can be provided to obtain benchmark\nresults for one or more specific runs. This attempts to fetch\nall associated benchmark results from the database and tries\nto return them all in a single response; use that with caution:\nkeep the number of run_ids low or equal to, unless you know better.\n",
                "parameters": [
                    {"in": "query", "name": "name", "schema": {"type": "string"}},
                    {"in": "query", "name": "batch_id", "schema": {"type": "string"}},
                    {"in": "query", "name": "run_id", "schema": {"type": "string"}},
                ],
                "responses": {
                    "200": {"$ref": "#/components/responses/BenchmarkList"},
                    "401": {"$ref": "#/components/responses/401"},
                },
                "tags": ["Benchmarks"],
            },
            "post": {
                "description": "Submit a BenchmarkResult within a specific Run.\nIf the Run (as defined by its Run ID) is not known yet in the database it gets implicitly created, using details provided in this request. If the Run ID matches an existing run, then the rest of the fields describing the Run (such as name, hardware info, ...} are silently ignored.",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/BenchmarkResultCreate"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {"$ref": "#/components/responses/BenchmarkResultCreated"},
                    "400": {"$ref": "#/components/responses/400"},
                    "401": {"$ref": "#/components/responses/401"},
                },
                "tags": ["Benchmarks"],
            },
        },
        "/api/benchmarks/{benchmark_result_id}/": {
            "delete": {
                "description": "Delete a benchmark result.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "benchmark_result_id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {
                    "204": {"$ref": "#/components/responses/204"},
                    "401": {"$ref": "#/components/responses/401"},
                    "404": {"$ref": "#/components/responses/404"},
                },
                "tags": ["Benchmarks"],
            },
            "get": {
                "description": 'Get a specific benchmark result.\n\nThe "z_score" key in the response is deprecated and only returns null.\n',
                "parameters": [
                    {
                        "in": "path",
                        "name": "benchmark_result_id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {
                    "200": {"$ref": "#/components/responses/BenchmarkEntity"},
                    "401": {"$ref": "#/components/responses/401"},
                    "404": {"$ref": "#/components/responses/404"},
                },
                "tags": ["Benchmarks"],
            },
            "put": {
                "description": "Edit a benchmark result.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "benchmark_result_id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/BenchmarkResultUpdate"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {"$ref": "#/components/responses/BenchmarkEntity"},
                    "401": {"$ref": "#/components/responses/401"},
                    "404": {"$ref": "#/components/responses/404"},
                },
                "tags": ["Benchmarks"],
            },
        },
        "/api/commits/": {
            "get": {
                "description": "Get a list of commits.",
                "responses": {
                    "200": {"$ref": "#/components/responses/CommitList"},
                    "401": {"$ref": "#/components/responses/401"},
                },
                "tags": ["Commits"],
            }
        },
        "/api/commits/{commit_id}/": {
            "get": {
                "description": "Get a commit.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "commit_id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {
                    "200": {"$ref": "#/components/responses/CommitEntity"},
                    "401": {"$ref": "#/components/responses/401"},
                    "404": {"$ref": "#/components/responses/404"},
                },
                "tags": ["Commits"],
            }
        },
        "/api/compare/benchmark-results/{compare_ids}/": {
            "get": {
                "description": "Compare a baseline and contender benchmark result.\n\nReturns basic information about the baseline and contender benchmark results\nas well as some analyses comparing the performance of the contender to the\nbaseline.\n\nThe `pairwise` analysis computes the percentage difference of the\ncontender's mean value to the baseline's mean value. The reported difference\nis signed such that a more negative value indicates more of a performance\nregression. This difference is then thresholded such that values more\nextreme than the threshold are marked as `regression_indicated` or\n`improvement_indicated`. The threshold is 5.0% by default, but can be\nchanged via the `threshold` query parameter, which should be a positive\npercent value.\n\nThe `pairwise` analysis may be `null` if either benchmark result does not\nhave a mean value, or if the baseline result's mean value is 0.\n\nThe `lookback_z_score` analysis compares the contender's mean value to a\nbaseline distribution of benchmark result mean values (from the git history\nof the baseline result) via the so-called lookback z-score method. The\nreported z-score is also signed such that a more negative value indicates\nmore of a performance regression, and thresholded. The threshold z-score is\n5.0 by default, but can be changed via the `threshold_z` query parameter,\nwhich should be a positive number.\n\nThe `lookback_z_score` analysis object may be `null` if a z-score cannot be\ncomputed for the contender benchmark result, due to not finding a baseline\ndistribution that matches the contender benchmark result. More details about\nthis analysis can be found at\nhttps://conbench.github.io/conbench/pages/lookback_zscore.html.\n\nIf either benchmark result is not found, this endpoint will raise a 404. If\nthe benchmark results don't have the same unit, this endpoint will raise a\n400. Otherwise, you may compare any two benchmark results, no matter if\ntheir cases, contexts, hardwares, or even repositories don't match.\n",
                "parameters": [
                    {
                        "example": "<baseline_id>...<contender_id>",
                        "in": "path",
                        "name": "compare_ids",
                        "required": True,
                        "schema": {"type": "string"},
                    },
                    {"in": "query", "name": "threshold", "schema": {"type": "number"}},
                    {
                        "in": "query",
                        "name": "threshold_z",
                        "schema": {"type": "number"},
                    },
                ],
                "responses": {
                    "200": {"$ref": "#/components/responses/CompareEntity"},
                    "400": {"$ref": "#/components/responses/400"},
                    "401": {"$ref": "#/components/responses/401"},
                    "404": {"$ref": "#/components/responses/404"},
                },
                "tags": ["Comparisons"],
            }
        },
        "/api/compare/runs/{compare_ids}/": {
            "get": {
                "description": "Compare all benchmark results between two runs.\n\nThis endpoint will return a list of comparison objects, pairing benchmark\nresults from the given baseline and contender runs that have the same case,\ncontext, hardware, and unit. The comparison object is the same\nas the `GET /api/compare/benchmark-results/` response; see that endpoint's\ndocumentation for details.\n\nIf a benchmark result from one run does not have a matching result in the\nother run, a comparison object will still be returned for it, with the other\nresult's information replaced by `null` and each analysis also `null`.\n\nIf a benchmark result from one run has multiple matching results in the\nother run, a comparison object will be returned for each match. Filtering\nmust be done clientside.\n",
                "parameters": [
                    {
                        "example": "<baseline_id>...<contender_id>",
                        "in": "path",
                        "name": "compare_ids",
                        "required": True,
                        "schema": {"type": "string"},
                    },
                    {"in": "query", "name": "threshold", "schema": {"type": "number"}},
                    {
                        "in": "query",
                        "name": "threshold_z",
                        "schema": {"type": "number"},
                    },
                ],
                "responses": {
                    "200": {"$ref": "#/components/responses/CompareList"},
                    "401": {"$ref": "#/components/responses/401"},
                    "404": {"$ref": "#/components/responses/404"},
                },
                "tags": ["Comparisons"],
            }
        },
        "/api/contexts/": {
            "get": {
                "description": "Get a list of contexts.",
                "responses": {
                    "200": {"$ref": "#/components/responses/ContextList"},
                    "401": {"$ref": "#/components/responses/401"},
                },
                "tags": ["Contexts"],
            }
        },
        "/api/contexts/{context_id}/": {
            "get": {
                "description": "Get a context.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "context_id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {
                    "200": {"$ref": "#/components/responses/ContextEntity"},
                    "401": {"$ref": "#/components/responses/401"},
                    "404": {"$ref": "#/components/responses/404"},
                },
                "tags": ["Contexts"],
            }
        },
        "/api/docs.json": {},
        "/api/google/": {
            "get": {
                "description": "Google SSO.",
                "responses": {"302": {"$ref": "#/components/responses/302"}},
                "tags": ["Authentication"],
            }
        },
        "/api/google/callback": {
            "get": {
                "description": "Google SSO callback.",
                "responses": {
                    "302": {"$ref": "#/components/responses/302"},
                    "400": {"$ref": "#/components/responses/400"},
                },
                "tags": ["Authentication"],
            }
        },
        "/api/hardware/": {
            "get": {
                "description": "Get a list of hardware.",
                "responses": {
                    "200": {"$ref": "#/components/responses/HardwareList"},
                    "401": {"$ref": "#/components/responses/401"},
                },
                "tags": ["Hardware"],
            }
        },
        "/api/hardware/{hardware_id}/": {
            "get": {
                "description": "Get a hardware.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "hardware_id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {
                    "200": {"$ref": "#/components/responses/HardwareEntity"},
                    "401": {"$ref": "#/components/responses/401"},
                    "404": {"$ref": "#/components/responses/404"},
                },
                "tags": ["Hardware"],
            }
        },
        "/api/history/{benchmark_result_id}/": {
            "get": {
                "description": "Get benchmark history.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "benchmark_result_id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {
                    "200": {"$ref": "#/components/responses/HistoryList"},
                    "401": {"$ref": "#/components/responses/401"},
                    "404": {"$ref": "#/components/responses/404"},
                },
                "tags": ["History"],
            }
        },
        "/api/info/": {
            "get": {
                "description": "Get a list of benchmark info.",
                "responses": {
                    "200": {"$ref": "#/components/responses/InfoList"},
                    "401": {"$ref": "#/components/responses/401"},
                },
                "tags": ["Info"],
            }
        },
        "/api/info/{info_id}/": {
            "get": {
                "description": "Get benchmark info.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "info_id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {
                    "200": {"$ref": "#/components/responses/InfoEntity"},
                    "401": {"$ref": "#/components/responses/401"},
                    "404": {"$ref": "#/components/responses/404"},
                },
                "tags": ["Info"],
            }
        },
        "/api/login/": {
            "post": {
                "description": "Login with email and password.",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Login"}
                        }
                    }
                },
                "responses": {
                    "204": {"$ref": "#/components/responses/204"},
                    "400": {"$ref": "#/components/responses/400"},
                },
                "tags": ["Authentication"],
            }
        },
        "/api/logout/": {
            "get": {
                "description": "Logout.",
                "responses": {"204": {"$ref": "#/components/responses/204"}},
                "tags": ["Authentication"],
            }
        },
        "/api/ping/": {
            "get": {
                "description": "Ping the API for status monitoring.",
                "responses": {"200": {"$ref": "#/components/responses/Ping"}},
                "tags": ["Ping"],
            }
        },
        "/api/redoc": {},
        "/api/register/": {
            "post": {
                "description": "Sign up for a user account.",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Register"}
                        }
                    }
                },
                "responses": {
                    "201": {"$ref": "#/components/responses/UserCreated"},
                    "400": {"$ref": "#/components/responses/400"},
                },
                "tags": ["Authentication"],
            }
        },
        "/api/runs/": {
            "get": {
                "description": "Get a list of runs.",
                "parameters": [
                    {"in": "query", "name": "sha", "schema": {"type": "string"}}
                ],
                "responses": {
                    "200": {"$ref": "#/components/responses/RunList"},
                    "401": {"$ref": "#/components/responses/401"},
                },
                "tags": ["Runs"],
            },
            "post": {
                "description": "Create a run.",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/RunCreate"}
                        }
                    }
                },
                "responses": {
                    "201": {"$ref": "#/components/responses/RunCreated"},
                    "400": {"$ref": "#/components/responses/400"},
                    "401": {"$ref": "#/components/responses/401"},
                },
                "tags": ["Runs"],
            },
        },
        "/api/runs/{run_id}/": {
            "delete": {
                "description": "Delete a run.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "run_id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {
                    "204": {"$ref": "#/components/responses/204"},
                    "401": {"$ref": "#/components/responses/401"},
                    "404": {"$ref": "#/components/responses/404"},
                },
                "tags": ["Runs"],
            },
            "get": {
                "description": 'Get a run and information about its candidate baseline runs.\n\nThe `"candidate_baseline_runs"` key in the response contains information\nabout up to three candidate baseline runs. Each baseline run corresponds to\na different candidate baseline commit, detailed below. If a baseline run is\nnot found for that commit, the response will detail why in the `"error"`\nkey. If a baseline run is found, its ID will be returned in the\n`"baseline_run_id"` key.\n\nThe three candidate baseline commits are:\n\n- the parent commit of the contender run\'s commit (`"parent"`)\n- if the contender run is on a PR branch, the default-branch commit that the\n  PR branch forked from (`"fork_point"`)\n- if the contender run is on a PR branch, the latest commit on the default\n  branch that has benchmark results (`"latest_default"`)\n\nWhen searching for a baseline run, each matching baseline run must:\n\n- be on the respective baseline commit, or in its git ancestry\n- match the contender run\'s hardware\n- have a benchmark result with the `case_id`/`context_id` of any of the\n  contender run\'s benchmark results\n\nIf there are multiple matches, prefer a baseline run with the same reason as\nthe contender run, and then use the baseline run with the most-recent\ncommit, finally tiebreaking by choosing the baseline run with the latest run\ntimestamp.\n\nIf any commits in the git ancestry were skipped to find a matching baseline\nrun, those commit hashes will be returned in the `"commits_skipped"` key.\n',
                "parameters": [
                    {
                        "in": "path",
                        "name": "run_id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {
                    "200": {"$ref": "#/components/responses/RunEntityWithBaselines"},
                    "401": {"$ref": "#/components/responses/401"},
                    "404": {"$ref": "#/components/responses/404"},
                },
                "tags": ["Runs"],
            },
            "put": {
                "description": "Edit a run.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "run_id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/RunUpdate"}
                        }
                    }
                },
                "responses": {
                    "200": {"$ref": "#/components/responses/RunEntityWithoutBaselines"},
                    "401": {"$ref": "#/components/responses/401"},
                    "404": {"$ref": "#/components/responses/404"},
                },
                "tags": ["Runs"],
            },
        },
        "/api/users/": {
            "get": {
                "description": "Get a list of users.",
                "responses": {
                    "200": {"$ref": "#/components/responses/UserList"},
                    "401": {"$ref": "#/components/responses/401"},
                },
                "tags": ["Users"],
            },
            "post": {
                "description": "Create a user.",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UserCreate"}
                        }
                    }
                },
                "responses": {
                    "201": {"$ref": "#/components/responses/UserCreated"},
                    "400": {"$ref": "#/components/responses/400"},
                    "401": {"$ref": "#/components/responses/401"},
                },
                "tags": ["Users"],
            },
        },
        "/api/users/{user_id}/": {
            "delete": {
                "description": "Delete a user.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "user_id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {
                    "204": {"$ref": "#/components/responses/204"},
                    "401": {"$ref": "#/components/responses/401"},
                    "404": {"$ref": "#/components/responses/404"},
                },
                "tags": ["Users"],
            },
            "get": {
                "description": "Get a user.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "user_id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {
                    "200": {"$ref": "#/components/responses/UserEntity"},
                    "401": {"$ref": "#/components/responses/401"},
                    "404": {"$ref": "#/components/responses/404"},
                },
                "tags": ["Users"],
            },
            "put": {
                "description": "Edit a user.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "user_id",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UserUpdate"}
                        }
                    }
                },
                "responses": {
                    "200": {"$ref": "#/components/responses/UserEntity"},
                    "401": {"$ref": "#/components/responses/401"},
                    "404": {"$ref": "#/components/responses/404"},
                },
                "tags": ["Users"],
            },
        },
    },
    "servers": [{"url": "http://127.0.0.1:5000/"}],
    "tags": [
        {"name": "Authentication"},
        {"description": "List of endpoints", "name": "Index"},
        {"description": "Manage users", "name": "Users"},
        {"description": "Record benchmarks", "name": "Benchmarks"},
        {"description": "Benchmarked commits", "name": "Commits"},
        {"description": "Benchmark comparisons", "name": "Comparisons"},
        {"description": "Extra benchmark information", "name": "Info"},
        {"description": "Benchmark contexts", "name": "Contexts"},
        {"description": "Benchmark history", "name": "History"},
        {"description": "Benchmark hardware", "name": "Hardware"},
        {"description": "Benchmark runs", "name": "Runs"},
        {"description": "Monitor status", "name": "Ping"},
        {
            "description": '## BenchmarkResultCreate\n<SchemaDefinition schemaRef="#/components/schemas/BenchmarkResultCreate" />\n\n## BenchmarkResultStats\n<SchemaDefinition schemaRef="#/components/schemas/BenchmarkResultStats" />\n\n## BenchmarkResultUpdate\n<SchemaDefinition schemaRef="#/components/schemas/BenchmarkResultUpdate" />\n\n## ClusterCreate\n<SchemaDefinition schemaRef="#/components/schemas/ClusterCreate" />\n\n## Error\n<SchemaDefinition schemaRef="#/components/schemas/Error" />\n\n## ErrorBadRequest\n<SchemaDefinition schemaRef="#/components/schemas/ErrorBadRequest" />\n\n## ErrorValidation\n<SchemaDefinition schemaRef="#/components/schemas/ErrorValidation" />\n\n## Login\n<SchemaDefinition schemaRef="#/components/schemas/Login" />\n\n## MachineCreate\n<SchemaDefinition schemaRef="#/components/schemas/MachineCreate" />\n\n## Ping\n<SchemaDefinition schemaRef="#/components/schemas/Ping" />\n\n## Register\n<SchemaDefinition schemaRef="#/components/schemas/Register" />\n\n## RunCreate\n<SchemaDefinition schemaRef="#/components/schemas/RunCreate" />\n\n## RunUpdate\n<SchemaDefinition schemaRef="#/components/schemas/RunUpdate" />\n\n## SchemaGitHubCreate\n<SchemaDefinition schemaRef="#/components/schemas/SchemaGitHubCreate" />\n\n## UserCreate\n<SchemaDefinition schemaRef="#/components/schemas/UserCreate" />\n\n## UserUpdate\n<SchemaDefinition schemaRef="#/components/schemas/UserUpdate" />\n',
            "name": "Models",
            "x-displayName": "Object models",
        },
    ],
}
