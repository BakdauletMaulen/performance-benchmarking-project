
import json
import pandas as pd
import numpy as np

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def bootstrap_ci(values, confidence=0.95, n_boot=2000):

    values = np.asarray(values, dtype=float)

    if len(values) < 2:
        return np.nan, np.nan

    rng = np.random.default_rng(42)

    bootstrap_medians = []

    for _ in range(n_boot):
        sample = rng.choice(
            values,
            size=len(values),
            replace=True
        )

        bootstrap_medians.append(np.median(sample))

    alpha = 1 - confidence

    lower = np.percentile(
        bootstrap_medians,
        alpha / 2 * 100
    )

    upper = np.percentile(
        bootstrap_medians,
        (1 - alpha / 2) * 100
    )

    return lower, upper


def process_benchmark_data(input_path, output_path):

    # 1. Read JSONL data
    records = []

    with open(input_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    df = pd.DataFrame(records)

    if df.empty:
        raise ValueError("Raw benchmark file is empty")

    required = [
        "method",
        "phase",
        "latency_ms",
        "throughput_rps",
        "peak_memory_mb",
        "success"
    ]

    for column in required:
        if column not in df.columns:
            raise ValueError(f"Missing column: {column}")

    # 2. Remove warm-up measurements
    df = df[df["phase"] == "evaluation"].copy()

    if df.empty:
        raise ValueError("No evaluation measurements found")

    # Convert numeric columns
    numeric_columns = [
        "latency_ms",
        "throughput_rps",
        "peak_memory_mb"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Convert success values to Boolean
    df["success"] = (
        df["success"]
        .astype(str)
        .str.lower()
        .isin(["true", "1", "yes"])
    )

    results = []

    # 3. Calculate statistics for each method
    for method, group in df.groupby("method"):

        total_runs = len(group)

        failed_runs = (~group["success"]).sum()

        error_rate = failed_runs / total_runs * 100

        # Use successful measurements
        valid = group[group["success"]].dropna(
            subset=numeric_columns
        )

        if valid.empty:
            raise ValueError(
                f"No valid measurements for {method}"
            )

        latency = valid["latency_ms"].to_numpy()

        ci_lower, ci_upper = bootstrap_ci(latency)

        results.append({
            "method": method,
            "observations": len(valid),

            "latency_mean_ms": np.mean(latency),
            "latency_median_ms": np.median(latency),
            "latency_std_ms": np.std(latency, ddof=1)
                if len(latency) > 1 else np.nan,

            "latency_p95_ms": np.percentile(latency, 95),
            "latency_p99_ms": np.percentile(latency, 99),

            "median_ci_lower_ms": ci_lower,
            "median_ci_upper_ms": ci_upper,

            "throughput_mean_rps": valid["throughput_rps"].mean(),
            "memory_mean_mb": valid["peak_memory_mb"].mean(),

            "error_rate_pct": error_rate
        })

    # 4. Create summary table
    summary = pd.DataFrame(results)

    # 5. Calculate speedup
    summary["speedup_vs_baseline"] = np.nan

    baseline = summary[
        summary["method"] == "baseline_method"
    ]

    optimized = summary[
        summary["method"] == "optimized_method"
    ]

    if not baseline.empty and not optimized.empty:

        baseline_latency = baseline[
            "latency_median_ms"
        ].iloc[0]

        optimized_latency = optimized[
            "latency_median_ms"
        ].iloc[0]

        summary.loc[
            summary["method"] == "baseline_method",
            "speedup_vs_baseline"
        ] = 1.0

        if optimized_latency > 0:
            summary.loc[
                summary["method"] == "optimized_method",
                "speedup_vs_baseline"
            ] = baseline_latency / optimized_latency

    # 6. Save CSV
    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    summary.to_csv(
        output_path,
        index=False,
        float_format="%.4f"
    )

    print("Data processing completed successfully!")
    print("\nStatistical Summary:")
    print(summary.to_string(index=False))

    print(f"\nResults saved to: {output_path}")

    return summary


if __name__ == "__main__":

    input_path = ROOT / "data" / "raw" / "test_run.jsonl"

    output_path = (
        ROOT / "data" / "processed" / "metrics_summary.csv"
    )

    process_benchmark_data(input_path, output_path)
