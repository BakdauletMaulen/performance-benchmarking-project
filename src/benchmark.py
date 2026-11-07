
import os
import json
import time
import tracemalloc
import pandas as pd
import yaml

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def baseline_method(df, category, metric):

    grouped = df.groupby(category)

    means = grouped[metric].mean()
    sums = grouped[metric].sum()
    counts = grouped[metric].count()

    result = pd.concat(
        [means, sums, counts],
        axis=1
    )

    result.columns = ["mean", "sum", "count"]

    return result.reset_index()


def optimized_method(df, category, metric):

    result = df.groupby(category)[metric].agg(
        ["mean", "sum", "count"]
    )

    return result.reset_index()


def run_single(method, df, category, metric, phase):

    start = time.perf_counter()

    tracemalloc.start()

    success = True

    try:
        result = method(df, category, metric)

    except Exception as error:
        success = False
        result = None
        print("Benchmark error:", error)

    elapsed = (time.perf_counter() - start) * 1000

    current, peak = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    elapsed_seconds = elapsed / 1000

    if success and elapsed_seconds > 0:
        throughput = len(df) / elapsed_seconds
    else:
        throughput = 0

    record = {
        "method": method.__name__,
        "phase": phase,
        "latency_ms": elapsed,
        "throughput_rps": throughput,
        "peak_memory_mb": peak / (1024 * 1024),
        "success": success
    }

    return record, result


def run_benchmark():

    config_path = ROOT / "configs" / "config.yaml"

    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    data_path = ROOT / config["input_data"]["sample_path"]

    df = pd.read_csv(
        data_path,
        encoding=config["input_data"]["encoding"]
    )

    category = config["benchmark_params"]["aggregation_target"]
    metric = config["benchmark_params"]["metric_target"]

    iterations = config["benchmark_params"]["iterations"]
    warmups = config["benchmark_params"]["warmup_runs"]

    methods = [
        baseline_method,
        optimized_method
    ]

    output_path = ROOT / "data" / "raw" / "test_run.jsonl"

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    all_records = []

    # Warm-up runs
    for method in methods:

        for _ in range(warmups):

            record, result = run_single(
                method, df, category, metric, "warmup"
            )

            all_records.append(record)

    # Evaluation runs
    evaluation_results = {}

    for method in methods:

        for _ in range(iterations):

            record, result = run_single(
                method, df, category, metric, "evaluation"
            )

            all_records.append(record)

            if record["success"]:
                evaluation_results[method.__name__] = result

    # Check whether both methods produce the same result
    pd.testing.assert_frame_equal(
        evaluation_results["baseline_method"],
        evaluation_results["optimized_method"],
        check_dtype=False,
        check_exact=False,
        rtol=1e-9,
        atol=1e-9
    )

    # Save all measurements in JSONL format
    with open(output_path, "w", encoding="utf-8") as file:

        for record in all_records:
            file.write(json.dumps(record) + "\n")

    print("Benchmark completed successfully.")
    print("Total measurements:", len(all_records))
    print("Warm-up measurements:", warmups * len(methods))
    print("Evaluation measurements:", iterations * len(methods))
    print("Results saved to:", output_path)


if __name__ == "__main__":
    run_benchmark()
