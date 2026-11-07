
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

sns.set_theme(style="whitegrid")

PALETTE = sns.color_palette("colorblind")


def generate_plots(summary_csv_path, raw_jsonl_path, output_dir):

    summary = pd.read_csv(summary_csv_path)

    raw = pd.read_json(raw_jsonl_path, lines=True)

    # Keep only successful evaluation measurements
    raw = raw[
        (raw["phase"] == "evaluation") &
        (raw["success"] == True)
    ].copy()

    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    methods = summary["method"].tolist()

    # -----------------------------------
    # FIGURE 1: Latency comparison with 95% CI
    # -----------------------------------

    fig, ax = plt.subplots(figsize=(8, 6))

    x_positions = range(len(methods))

    medians = summary["latency_median"].values

    lower_errors = (
        medians - summary["latency_ci_lower"].values
    )

    upper_errors = (
        summary["latency_ci_upper"].values - medians
    )

    ax.errorbar(
        x_positions,
        medians,
        yerr=[lower_errors, upper_errors],
        fmt="o",
        color=PALETTE[0],
        ecolor=PALETTE[1],
        capsize=7,
        markersize=9,
        elinewidth=2,
        markeredgewidth=1.5
    )

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(methods)

    ax.set_title(
        "Execution Latency Comparison with 95% CI"
    )

    ax.set_xlabel("Processing Method")
    ax.set_ylabel("Latency (ms)")

    ax.grid(True, linestyle="--", alpha=0.5)

    fig.tight_layout()

    fig.savefig(
        output_dir / "fig1_latency_vs_load.png",
        dpi=300,
        bbox_inches="tight"
    )

    fig.savefig(
        output_dir / "fig1_latency_vs_load.pdf",
        bbox_inches="tight"
    )

    plt.show()
    plt.close(fig)

    # -----------------------------------
    # FIGURE 2: Latency Distribution Boxplot
    # -----------------------------------

    fig, ax = plt.subplots(figsize=(8, 6))

    sns.boxplot(
        data=raw,
        x="method",
        y="latency_ms",
        hue="method",
        palette=PALETTE,
        dodge=False,
        showfliers=True,
        legend=False,
        ax=ax
    )

    ax.set_title(
        "Latency Distribution by Processing Method"
    )

    ax.set_xlabel("Processing Method")
    ax.set_ylabel("Latency (ms)")

    ax.grid(
        True,
        axis="y",
        linestyle="--",
        alpha=0.5
    )

    fig.tight_layout()

    fig.savefig(
        output_dir / "fig2_distribution_boxplot.png",
        dpi=300,
        bbox_inches="tight"
    )

    fig.savefig(
        output_dir / "fig2_distribution_boxplot.pdf",
        bbox_inches="tight"
    )

    plt.show()
    plt.close(fig)

    print("Both figures generated successfully.")
    print(f"Figures saved to: {output_dir}")


if __name__ == "__main__":

    generate_plots(
        ROOT / "data" / "processed" / "metrics_summary.csv",
        ROOT / "data" / "raw" / "test_run.jsonl",
        ROOT / "reports" / "figures"
    )
