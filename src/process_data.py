import json
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def bootstrap_ci(values, n_boot=2000):
    values = np.asarray(values, dtype=float)
    rng = np.random.default_rng(42)
    bootstrap_medians = []

    for _ in range(n_boot):

        sample = rng.choice(
            values,
            size=len(values),
            replace=True
        )

        bootstrap_medians.append(np.median(sample))
    lower = np.percentile(bootstrap_medians, 2.5)
    upper = np.percentile(bootstrap_medians, 97.5)
    return lower, upper
def process_benchmark_data(input_path, output_path):
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(
            f"Raw data not found: {input_path}"
        )
        
    records = []
    with open(input_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))

            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {error}"
                )

    if not records:
        raise ValueError("The raw JSONL file is empty.")

    df = pd.DataFrame(records)
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
            raise ValueError(
                f"Missing required column: {column}"
            )
    df_eval = df[
        df["phase"] == "evaluation"
    ].copy()
    if df_eval.empty:
        raise ValueError("No evaluation measurements found.")
    results = []
    for method, group in df_eval.groupby("method"):
        total_runs = len(group)
        successful = group[
            group["success"].astype(bool)
        ].copy()
        failed_runs = total_runs - len(successful)
        error_rate = failed_runs / total_runs * 100
        if successful.empty:
            raise ValueError(
                f"No successful runs for {method}"
            )
        latency = successful["latency_ms"].astype(float)
        throughput = successful["throughput_rps"].astype(float)
        memory = successful["peak_memory_mb"].astype(float)
        ci_lower, ci_upper = bootstrap_ci(latency)
        results.append({
            "method": method,
            "total_runs": total_runs,
            "successful_runs": len(successful),
            "failed_runs": failed_runs,
            "error_rate_pct": error_rate,
            "latency_mean": latency.mean(),
            "latency_std": latency.std(),
            "latency_median": latency.median(),
            "latency_p95": np.percentile(latency, 95),
            "latency_p99": np.percentile(latency, 99),
            "latency_ci_lower": ci_lower,
            "latency_ci_upper": ci_upper,
            "throughput_mean": throughput.mean(),
            "memory_mean_mb": memory.mean()

        })

    summary = pd.DataFrame(results)
    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )
    summary.to_csv(
        output_path,
        index=False
    )
    print("Statistical analysis completed.")
    print("\nResults:")
    print(summary.round(3).to_string(index=False))
    print("\nSaved to:", output_path)
    return summary
if __name__ == "__main__":
    input_path = ROOT / "data" / "raw" / "test_run.jsonl"
    output_path = (
        ROOT / "data" / "processed" / "metrics_summary.csv"
    )
    process_benchmark_data(
        input_path,
        output_path
    )
