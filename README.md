
# Quantitative Benchmark Analysis of Data Processing Pipelines

## Research Metadata

- **Project Title:** Performance Benchmarking of Data Processing Algorithms
- **Author:** Bakdaulet Maulen
- **Repository:** https://github.com/BakdauletMaulen/performance-benchmarking-project

## Abstract

This project presents an empirical benchmarking framework designed to evaluate the performance of data processing algorithms.

The main objective is to compare a baseline data processing method with an optimized method using execution latency, throughput, memory usage, and error rate.

The experiment includes warm-up measurements and evaluation measurements to ensure more reliable performance analysis.

## Research Question

To what extent do localized algorithmic optimizations reduce data aggregation latency without breaching hardware memory and processing safety thresholds?

## Project Structure

```text
performance-benchmarking-project/
│
├── configs/
│   └── config.yaml
│
├── data/
│   ├── raw/
│   │   └── test_run.jsonl
│   │
│   ├── processed/
│   │   └── metrics_summary.csv
│   │
│   └── sample/
│       └── test_data.csv
│
├── docs/
│   └── domain_model.md
│
├── notebooks/
│   └── 01_data_analysis.ipynb
│
├── reports/
│   └── figures/
│       ├── fig1_latency_comparison.png
│       ├── fig1_latency_comparison.pdf
│       ├── fig2_distribution_boxplot.png
│       └── fig2_distribution_boxplot.pdf
│
├── src/
│   ├── benchmark.py
│   ├── process_data.py
│   └── visualize.py
│
├── .gitignore
├── Dockerfile
├── LICENSE
├── requirements.txt
└── README.md
```

## Experimental Methodology

The experiment compares two processing methods:

1. **Baseline Method** – the original data processing implementation.
2. **Optimized Method** – the improved implementation using algorithmic optimizations.

### Experimental Configuration

| Parameter | Value |
|---|---|
| Total measurements | 210 |
| Warm-up measurements | 10 |
| Evaluation measurements | 200 |
| Baseline evaluations | 100 |
| Optimized evaluations | 100 |
| Bootstrap iterations | 2,000 |
| Confidence level | 95% |
| Random seed | 42 |

Warm-up measurements are excluded from the final statistical analysis.

Only successful evaluation measurements are used for latency, throughput, and memory calculations.

## Performance Metrics

The following metrics are used:

- **Latency (ms):** Time required to process data.
- **Throughput (RPS):** Number of processing operations per second.
- **Memory Usage (MB):** Average peak memory usage.
- **Error Rate (%):** Percentage of failed measurements.
- **Speedup:** Ratio of baseline median latency to optimized median latency.
- **95% Confidence Interval:** Bootstrap confidence interval for median latency.

## Results & Discussion

### 1. Statistical Summary

The following table presents the experimental results obtained from the benchmark evaluation.

| Metric | Baseline Method | Optimized Method |
|---|---:|---:|
| Observations | 100 | 100 |
| Mean Latency (ms) | 2.632 | 2.082 |
| Median Latency (ms) | 2.571 | 1.995 |
| Standard Deviation (ms) | 0.350 | 0.256 |
| P95 Latency (ms) | 3.226 | 2.436 |
| P99 Latency (ms) | 3.800 | 3.261 |
| Throughput (RPS) | 3086.250 | 3883.861 |
| Memory Usage (MB) | 0.015 | 0.012 |
| Error Rate (%) | 0.0 | 0.0 |

### 2. Latency Comparison with 95% Confidence Interval

The median latency was compared using a bootstrap confidence interval with 2,000 resampling iterations.

| Method | Median (ms) | 95% CI |
|---|---:|---:|
| Baseline | 2.571 | [2.490, 2.631] |
| Optimized | 1.995 | [1.966, 2.016] |


The optimized method achieved a lower median execution latency than the baseline method.

### 3. Latency Distribution

The boxplot illustrates the distribution of execution latency across successful evaluation measurements.



The optimized method demonstrates a lower median latency and a narrower interquartile range, indicating more consistent execution times in this experiment.

### 4. Performance Improvement

The speedup is calculated as:

Speedup = Baseline Median Latency / Optimized Median Latency

Speedup = 2.571 / 1.995 = 1.2886

The optimized method achieved approximately **1.29x speedup** compared with the baseline method.

The median latency reduction is approximately **22.4%**.

Throughput increased, while average memory usage decreased.

Both methods recorded a 0% error rate during the evaluation measurements.

### 5. Research Conclusion

The experimental results indicate that the optimized data processing method outperformed the baseline implementation.

The optimized method demonstrated:

- Lower median execution latency.
- Higher processing throughput.
- Lower average memory usage.
- A 0% observed error rate.

These findings support the effectiveness of the implemented optimization under the tested experimental conditions.

However, the results are limited to the current dataset and hardware environment. Further experiments with larger datasets and different hardware configurations would be useful to validate the findings.

## Reproducibility

### Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Step 1: Run Benchmark

```bash
python src/benchmark.py
```

### Step 2: Process Benchmark Data

```bash
python src/process_data.py
```

### Step 3: Generate Visualizations

```bash
python src/visualize.py
```

### Step 4: Data Analysis

Open and run:

```text
notebooks/01_data_analysis.ipynb
```

The notebook performs statistical analysis and generates the corresponding figures.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook
- JSONL
- CSV

## License

This project is distributed under the MIT License.
