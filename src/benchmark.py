
import os
import json
import time
import tracemalloc
import yaml
import pandas as pd

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def baseline_method(df, category, metric):
    grouped = df.groupby(category)

    means = grouped[metric].mean()
    sums = grouped[metric].sum()
    counts = grouped[metric].count()

    result = pd.concat([means, sums, counts], axis=1)
    result.columns = ["mean", "sum", "count"]

    return result.reset_index()


def optimized_method(df, category, metric):
    result = df.groupby(category)[metric].agg(
        ["mean", "sum", "count"]
    )

    return result.reset_index()


def measure(method, df, category, metric, phase, iteration):
    tracemalloc.start()

    start = time.perf_counter()

    try:
        method(df, category, metric)

        elapsed = (time.perf_counter() - start) * 1000

        current, peak = tracemalloc.get_traced_memory()

        return {
            "phase": phase,
            "iteration": iteration,
            "latency_ms": elapsed,
            "throughput_rps": 1000 / elapsed if elapsed > 0 else 0,
            "peak_memory_mb": peak / (1024 * 1024),
            "success": True,
            "error": None
        }

    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000

        current, peak = tracemalloc.get_traced_memory()

        return {
            "phase": phase,
            "iteration": iteration,
            "latency_ms": None,
            "throughput_rps": 0,
            "peak_memory_mb": peak / (1024 * 1024),
            "success": False,
            "error": str(e)
        }

    finally:
        tracemalloc.stop()


def run_benchmark():

    config_path = ROOT / "configs" / "config.yaml"

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    data_path = ROOT / config["input_data"]["sample_path"]

    df = pd.read_csv(
        data_path,
        encoding=config["input_data"]["encoding"]
    )

    category = config["benchmark_params"]["aggregation_target"]
    metric = config["benchmark_params"]["metric_target"]

    iterations = config["benchmark_params"]["iterations"]
    warmups = config["benchmark_params"]["warmup_runs"]

    raw_path = ROOT / config["logging"]["raw_output_file"]

    raw_path.parent.mkdir(parents=True, exist_ok=True)

    # Check input data
    if df.empty:
        raise ValueError("Input dataset is empty")

    if category not in df.columns or metric not in df.columns:
        raise ValueError("Required columns are missing")

    if df[category].isna().any() or df[metric].isna().any():
        raise ValueError("Missing values found")

    if not pd.api.types.is_numeric_dtype(df[metric]):
        raise ValueError("Metric column must be numeric")

    methods = {
        "Pandas": baseline_method,
        "Optimized": optimized_method
    }

    # Check that both methods return equal results
    baseline_result = baseline_method(df, category, metric)
    optimized_result = optimized_method(df, category, metric)

    pd.testing.assert_frame_equal(
        baseline_result.sort_values(category).reset_index(drop=True),
        optimized_result.sort_values(category).reset_index(drop=True),
        check_dtype=False,
        check_exact=False,
        rtol=1e-9,
        atol=1e-9
    )

    records = []

    for method_name, method in methods.items():

        # Warm-up phase
        for i in range(warmups):
            record = measure(
                method, df, category, metric, "warmup", i + 1
            )

            record["method"] = method_name
            records.append(record)

        # Evaluation phase
        for i in range(iterations):
            record = measure(
                method, df, category, metric, "evaluation", i + 1
            )

            record["method"] = method_name
            records.append(record)

    # Save all raw measurements
    with open(raw_path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")

    print("Benchmark completed successfully.")
    print(f"Dataset rows: {len(df)}")
    print(f"Warm-up runs per method: {warmups}")
    print(f"Evaluation runs per method: {iterations}")
    print(f"Total measurements: {len(records)}")
    print(f"Raw results saved to: {raw_path}")


if __name__ == "__main__":
    run_benchmark()
