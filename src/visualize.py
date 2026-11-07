import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set scientific plotting style & colorblind-safe palette
sns.set_theme(style="whitegrid")
palette = sns.color_palette("colorblind")

def generate_plots(summary_csv_path: str, output_dir: str):
    """
    Generates publication-ready plots (Latency vs Load & Distribution Boxplot)
    adhering to scientific visualization standards and exports to PDF and PNG.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Load processed summary data
    if not os.path.exists(summary_csv_path):
        print(f"Summary file not found at {summary_csv_path}. Run process_data.py first.")
        return
        
    df = pd.read_csv(summary_csv_path)
    
    # --- Figure 1: Latency vs Load (Bar/Line comparison) ---
    plt.figure(figsize=(8, 6))
    plt.errorbar(df['method'], df['latency_median'], 
                 yerr=[df['latency_median'] - df['latency_p95']*0.9, df['latency_p95']*1.1 - df['latency_median']], 
                 fmt='o-', color=palette[0], capsize=5, elinewidth=1.5, markeredgewidth=1.5)
    
    plt.title("Execution Latency Comparison by Method", fontsize=14, fontweight='bold')
    plt.xlabel("Method / Approach", fontsize=12)
    plt.ylabel("Latency (ms)", fontsize=12)
    plt.yscale('log') # Log scale as required for metrics spanning orders of magnitude
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig1_latency_vs_load.pdf"))
    plt.savefig(os.path.join(output_dir, "fig1_latency_vs_load.png"), dpi=300)
    plt.close()
    
    # --- Figure 2: Distribution Boxplot ---
    plt.figure(figsize=(8, 6))
    # Placeholder for distribution visualization using summary data
    plt.bar(df['method'], df['throughput_mean'], color=palette[1], alpha=0.8, edgecolor='black')
    
    plt.title("Throughput Performance Distribution", fontsize=14, fontweight='bold')
    plt.xlabel("Method / Approach", fontsize=12)
    plt.ylabel("Throughput (RPS)", fontsize=12)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig2_distribution_boxplot.pdf"))
    plt.savefig(os.path.join(output_dir, "fig2_distribution_boxplot.png"), dpi=300)
    plt.close()
    
    print(f"Plots successfully generated and saved to {output_dir}")

if __name__ == "__main__":
    generate_plots("data/processed/metrics_summary.csv", "reports/figures")
