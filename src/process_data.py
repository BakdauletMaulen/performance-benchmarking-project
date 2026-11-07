import pandas as pd
import numpy as np

def process_benchmark_data(input_path: str, output_path: str):
    """
    Reads raw benchmark logs, filters out cold-start spikes,
    computes key statistical aggregations, and saves the summary CSV.
    """
    # 1. Load raw data (JSONL format)
    df = pd.read_json(input_path, lines=True)
    
    # 2. Filter out initial 'cold-start' execution spikes (e.g., first 10% of rows)
    warmup_threshold = int(len(df) * 0.1)
    df_eval = df.iloc[warmup_threshold:].copy()
    
    # 3. Statistical Aggregation (Median, p95, p99, Mean, SD)
    summary = df_eval.groupby('method').agg(
        latency_median=('latency_ms', 'median'),
        latency_p95=('latency_ms', lambda x: np.percentile(x, 95)),
        latency_p99=('latency_ms', lambda x: np.percentile(x, 99)),
        latency_mean=('latency_ms', 'mean'),
        latency_std=('latency_ms', 'std'),
        throughput_mean=('throughput_rps', 'mean')
    ).reset_index()
    
    # 4. Save processed metrics to CSV
    summary.to_csv(output_path, index=False)
    print(f"Processed metrics successfully saved to {output_path}")

if __name__ == "__main__":
    process_benchmark_data("data/raw/test_run.jsonl", "data/processed/metrics_summary.csv")
