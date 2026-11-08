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
│   ├── processed/
│   │   └── metrics_summary.csv
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
│       ├── fig1_latency_vs_load.png
│       ├── fig1_latency_vs_load.pdf
│       ├── fig2_latency_distribution.png
│       └── fig2_latency_distribution.pdf
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

The experiment compares two data processing methods:

1. **Baseline Method** – the original data processing implementation using Pandas groupby and concat.
2. **Optimized Method** – the improved implementation using Pandas groupby with aggregation.

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

The following performance metrics are used:

- **Latency (ms):** Time required to complete one benchmark execution.
- **Throughput (RPS):** Number of processing operations per second.
- **Memory Usage (MB):** Average peak memory usage.
- **Error Rate (%):** Percentage of failed benchmark executions.
- **Speedup:** Ratio of baseline median latency to optimized median latency.
- **95% Confidence Interval:** Bootstrap confidence interval for median latency.

## Results & Discussion

### 1. Statistical Summary

The following table presents the experimental results obtained from 200 successful evaluation measurements.

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

The median latency was compared using bootstrap resampling with 2,000 iterations.

| Method | Median (ms) | 95% Confidence Interval |
|---|---:|---:|
| Baseline | 2.571 | [2.490, 2.631] |
| Optimized | 1.995 | [1.966, 2.016] |

**Latency Comparison Figures:**

- [Open Latency Comparison Plot (PNG)](reports/figures/fig1_latency_comparison.png)
- [Open Latency Comparison Plot (PDF)](reports/figures/fig1_latency_comparison.pdf)

The optimized method achieved a lower median execution latency than the baseline method.

### 3. Latency Distribution

The boxplot illustrates the distribution of execution latency across successful evaluation measurements.

**Latency Distribution Figures:**

- [Open Latency Distribution Plot (PNG)](reports/figures/fig2_latency_distribution.png)
- [Open Latency Distribution Plot (PDF)](reports/figures/fig2_latency_distribution.pdf)

The optimized method demonstrates a lower median latency and a narrower interquartile range, indicating more consistent execution times in this experiment.

### 4. Performance Improvement

Speedup is calculated using median latency:

```text
Speedup = Baseline Median Latency / Optimized Median Latency

Speedup = 2.571 / 1.995

Speedup = 1.2886 ≈ 1.29x
```

The optimized method achieved approximately **1.29x speedup** compared with the baseline method.

The median latency reduction is approximately **22.4%**.

Throughput increased from 3086.250 RPS to 3883.861 RPS, while average memory usage decreased from 0.015 MB to 0.012 MB.

Both methods recorded a 0% observed error rate during the evaluation measurements.

### 5. Research Conclusion

The experimental results indicate that the optimized data processing method outperformed the baseline implementation under the tested conditions.

The optimized method demonstrated:

- Lower median execution latency.
- Higher processing throughput.
- Lower average memory usage.
- A 0% observed error rate.

These findings support the effectiveness of the implemented optimization in this experiment.

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

Open and run the following Jupyter Notebook:

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

## System Requirements

- Python 3.10 or later
- pip package manager
- Windows, Linux, or macOS
- Dependencies listed in `requirements.txt`

## Quickstart

Clone the repository:

```bash
git clone https://github.com/BakdauletMaulen/performance-benchmarking-project.git
cd performance-benchmarking-project
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the benchmark:

```bash
python src/benchmark.py
```

Process benchmark data:

```bash
python src/process_data.py
```

Generate visualizations:

```bash
python src/visualize.py
```

For statistical analysis, open `notebooks/01_data_analysis.ipynb` in Jupyter Notebook and run all cells.

## Citation

Maulen, B. (2026). *Performance Benchmarking of Data Processing Algorithms*. GitHub repository: https://github.com/BakdauletMaulen/performance-benchmarking-project
