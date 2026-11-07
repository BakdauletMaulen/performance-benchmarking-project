# Domain Model & Mathematical Formalization

## 1. Loss Function ($L$)
For our performance benchmarking and optimization task, we evaluate prediction errors using Mean Squared Error (MSE):
$$L(y, \hat{y}) = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$$

## 2. Target Metrics
- **Latency ($R_i$):** Execution time per request measured in milliseconds (ms).
- **Throughput ($T$):** Successfully processed requests per second (RPS):
$$T = \frac{\text{Total Requests}}{\text{Total Time (s)}}$$

## 3. Mathematical Notation Table
| Symbol | Description | Unit / Type |
| :--- | :--- | :--- |
| $N$ | Total number of benchmark iterations | Integer |
| $y_i$ | Baseline performance metric (Pandas execution) | Float |
| $\hat{y}_i$ | Optimized performance metric (Vectorized/Polars method) | Float |
| $L$ | Loss function value | Float |
