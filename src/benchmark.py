
import os
import time
import tracemalloc
import yaml
import pandas as pd


def baseline_method(df, category, metric):
    grouped = df.groupby(category)

    means = grouped[metric].mean()
    sums = grouped[metric].sum()
    counts = grouped[metric].count()

    result = pd.concat(
        [means, sums, counts], axis=1
    )
    result.columns = ["mean", "sum", "count"]

    return result.reset_index()


def optimized_method(df, category, metric):
    result = df.groupby(category)[metric].agg(
        ["mean", "sum", "count"]
    )
    return result.reset_index()


def measure(method, df, category, metric, iterations):
    times = []
    peak_memory = 0

    for _ in range(iterations):
        tracemalloc.start()
        start = time.perf_counter()

        result = method(df, category, metric)

        elapsed = (time.perf_counter() - start) * 1000
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        times.append(elapsed)
        peak_memory = max(peak_memory, peak)

    return {
        "mean_ms": sum(times) / len(times),
        "median_ms": sorted(times)[len(times) // 2],
        "peak_memory_mb": peak_memory / (1024 * 1024),
        "result": result
    }


def run_benchmark():
    with open("configs/config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    data_path = config["input_data"]["sample_path"]
    category = config["benchmark_params"]["aggregation_target"]
    metric = config["benchmark_params"]["metric_target"]
    iterations = config["benchmark_params"]["iterations"]
    warmups = config["benchmark_params"]["warmup_runs"]

    if iterations < 1 or warmups < 0:
        raise ValueError("Iterations must be positive and warmups non-negative")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found: {data_path}")

    df = pd.read_csv(data_path)

    if category not in df.columns or metric not in df.columns:
        raise ValueError("Required columns are missing from the CSV file")

    for method in [baseline_method, optimized_method]:
        for _ in range(warmups):
            method(df, category, metric)

    baseline = measure(
        baseline_method, df, category, metric, iterations
    )
    optimized = measure(
        optimized_method, df, category, metric, iterations
    )

    pd.testing.assert_frame_equal(
        baseline["result"].sort_values(category).reset_index(drop=True),
        optimized["result"].sort_values(category).reset_index(drop=True),
        check_dtype=False,
        check_exact=False,
        rtol=1e-9,
        atol=1e-9
    )

    speedup = baseline["mean_ms"] / optimized["mean_ms"]

    summary = f"""
BENCHMARK RESULTS
=================
Rows processed: {len(df)}
Iterations: {iterations}

BASELINE
Mean latency: {baseline['mean_ms']:.6f} ms
Median latency: {baseline['median_ms']:.6f} ms
Peak Python memory: {baseline['peak_memory_mb']:.6f} MB

OPTIMIZED
Mean latency: {optimized['mean_ms']:.6f} ms
Median latency: {optimized['median_ms']:.6f} ms
Peak Python memory: {optimized['peak_memory_mb']:.6f} MB

Speedup: {speedup:.4f}x
Results match: YES
"""

    print(summary)

    output_file = config["logging"]["output_file"]
    output_dir = os.path.dirname(output_file)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summary)


if __name__ == "__main__":
    run_benchmark()
