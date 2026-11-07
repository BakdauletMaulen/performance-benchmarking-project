
import pandas as pd
import numpy as np

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def bootstrap_ci(values, confidence=0.95, n_boot=2000):
    """
    Calculates bootstrap confidence interval for the median.
    """

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
        bootstrap_medians, alpha / 2 * 100
    )

    upper = np.percentile(
        bootstrap_medians, (1 - alpha / 2) * 100
    )

    return lower, upper


def process_benchmark_data(input_path, output_path):

    # 1. Load raw benchmark data
    df = pd.read_json(input_path, lines=True)

    if df.empty:
        raise ValueError("Raw benchmark file is empty")

    required = [
        "method",
        "phase",
        "latency_ms",
        "throughput_rps",
        "success"
    ]

    for column in required:
        if column not in df.columns:
            raise ValueError(f"Missing column: {column}")

    # 2. Remove warm-up measurements
    df_eval = df[df["phase"] == "evaluation"].copy()

    if df_eval.empty:
        raise ValueError("No evaluation measurements found")

    results = []

    # 3. Calculate statistics for each method
    for method, group in df_eval.groupby("method"):

        total_runs = len(group)

        failed_runs = (~group["success"].astype(bool)).sum()

        error_rate = failed_runs / total_runs * 100

        # Use only successful measurements
        valid = group[group["success"].astype(bool)].copy()

        valid = valid.dropna(subset=["latency_ms"])

        if valid.empty:
            raise ValueError(
                f"No successful measurements for {method}"
            )

        latency = valid["latency_ms"].astype(float)

        throughput = valid["throughput_rps"].astype(float)

        # Median confidence interval
        ci_lower, ci_upper = bootstrap_ci(latency)

        results.append({
            "method": method,
            "total_runs": total_runs,
            "successful_runs": len(valid),
            "failed_runs": int(failed_runs),
            "error_rate_pct": error_rate,

            "latency_mean": latency.mean(),
            "latency_std": latency.std(ddof=1),

            "latency_median": latency.median(),
            "latency_p95": np.percentile(latency, 95),
            "latency_p99": np.percentile(latency, 99),

            "latency_ci_lower": ci_lower,
            "latency_ci_upper": ci_upper,

            "throughput_mean": throughput.mean(),
            "throughput_std": throughput.std(ddof=1)
        })

    # 4. Create summary DataFrame
    summary = pd.DataFrame(results)

    # 5. Save processed results
    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    summary.to_csv(output_path, index=False)

    print("Data processing completed.")
    print("\nStatistical Summary:")
    print(summary.to_string(index=False))

    print(f"\nSaved to: {output_path}")

    return summary


if __name__ == "__main__":

    input_path = ROOT / "data" / "raw" / "test_run.jsonl"

    output_path = (
        ROOT / "data" / "processed" / "metrics_summary.csv"
    )

    process_benchmark_data(input_path, output_path)
