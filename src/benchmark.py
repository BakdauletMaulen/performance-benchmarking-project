import time
import os
import sys
import yaml
import pandas as pd

def run_empirical_benchmark():
    config_path = os.path.join("configs", "config.yaml")
    if not os.path.exists(config_path):
        print(f"[ERROR] Configuration missing at {config_path}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    print("="*60)
    print(f" EXPERIMENT: {config['experiment']['name']} (v{config['experiment']['version']})")
    print("="*60)

    data_path = config['input_data']['sample_path']
    if not os.path.exists(data_path):
        print(f"[ERROR] Sample data missing at {data_path}")
        sys.exit(1)

    df = pd.read_csv(data_path)
    for _ in range(config['benchmark_params']['warmup_runs']):
        _ = df.groupby(config['benchmark_params']['aggregation_target'])[config['benchmark_params']['metric_target']].mean()

    iterations = config['benchmark_params']['iterations']
    start_time = time.perf_counter()
    
    for _ in range(iterations):
        result = df.groupby(config['benchmark_params']['aggregation_target'])[config['benchmark_params']['metric_target']].agg(['mean', 'sum', 'count'])
    
    total_time_ms = (time.perf_counter() - start_time) * 1000
    avg_latency_ms = total_time_ms / iterations

    summary = (
        f"--- BENCHMARK EXECUTION SUMMARY ---\n"
        f"Status: SUCCESS\n"
        f"Rows Processed: {len(df)}\n"
        f"Total Iterations: {iterations}\n"
        f"Total Time: {total_time_ms:.4f} ms\n"
        f"Primary Metric (Mean Latency per Iteration): {avg_latency_ms:.6f} ms\n"
        f"Aggregated Categories:\n{result.to_string()}\n"
    )

    print(summary)

    with open(config['logging']['output_file'], "w", encoding="utf-8") as log_file:
        log_file.write(summary)

if __name__ == "__main__":
    run_empirical_benchmark()
