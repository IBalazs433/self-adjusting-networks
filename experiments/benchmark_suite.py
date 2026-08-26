import csv
import json
import random
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from networks.bst_network import BinarySearchTreeNetwork
from networks.optimal_network import build_optimal_bst_network, requests_to_matrix
from networks.splaynet import SplayNet
from trees.bst import BinarySearchTree
from trees.optimal_bst import build_optimal_bst, request_frequencies
from trees.splay_tree import SplayTree
from workloads.hot_set import generate_hotset_requests
from workloads.temporal import generate_temporal_requests
from workloads.uniform import generate_random_requests

RESULTS_DIR = ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
RAW_DIR = RESULTS_DIR / "raw"
REPORT_DIR = RESULTS_DIR / "report"

plt.rcParams.update({
    "figure.figsize": (5.6, 3.8),
    "figure.dpi": 220,
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "lines.linewidth": 2,
    "axes.linewidth": 1.15,
    "grid.alpha": 0.1,
})

TREE_EXPERIMENTS = [
    {
        "name": "uniform",
        "kind": "tree",
        "n": 100,
        "m": 10000,
        "generator": generate_random_requests,
        "args": {"dim": 1},
    },
    {
        "name": "hotset_0.1",
        "kind": "tree",
        "n": 100,
        "m": 10000,
        "generator": generate_hotset_requests,
        "args": {"hot_fraction": 0.1, "hot_probability": 0.9, "dim": 1},
    },
    {
        "name": "hotset_0.3",
        "kind": "tree",
        "n": 100,
        "m": 10000,
        "generator": generate_hotset_requests,
        "args": {"hot_fraction": 0.3, "hot_probability": 0.9, "dim": 1},
    },
    {
        "name": "hotset_0.5",
        "kind": "tree",
        "n": 100,
        "m": 10000,
        "generator": generate_hotset_requests,
        "args": {"hot_fraction": 0.5, "hot_probability": 0.9, "dim": 1},
    },
    {
        "name": "temporal_0.5",
        "kind": "tree",
        "n": 100,
        "m": 10000,
        "generator": generate_temporal_requests,
        "args": {"p_repeat": 0.5, "dim": 1},
    },
    {
        "name": "temporal_0.9",
        "kind": "tree",
        "n": 100,
        "m": 10000,
        "generator": generate_temporal_requests,
        "args": {"p_repeat": 0.9, "dim": 1},
    },
]

NETWORK_EXPERIMENTS = [
    {
        "name": "uniform",
        "kind": "network",
        "n": 100,
        "m": 10000,
        "generator": generate_random_requests,
        "args": {"dim": 2},
    },
    {
        "name": "hotset_0.1",
        "kind": "network",
        "n": 100,
        "m": 10000,
        "generator": generate_hotset_requests,
        "args": {"hot_fraction": 0.1, "hot_probability": 0.9, "dim": 2},
    },
    {
        "name": "hotset_0.3",
        "kind": "network",
        "n": 100,
        "m": 10000,
        "generator": generate_hotset_requests,
        "args": {"hot_fraction": 0.3, "hot_probability": 0.9, "dim": 2},
    },
    {
        "name": "hotset_0.5",
        "kind": "network",
        "n": 100,
        "m": 10000,
        "generator": generate_hotset_requests,
        "args": {"hot_fraction": 0.5, "hot_probability": 0.9, "dim": 2},
    },
    {
        "name": "temporal_0.5",
        "kind": "network",
        "n": 100,
        "m": 10000,
        "generator": generate_temporal_requests,
        "args": {"p_repeat": 0.5, "dim": 2},
    },
    {
        "name": "temporal_0.9",
        "kind": "network",
        "n": 100,
        "m": 10000,
        "generator": generate_temporal_requests,
        "args": {"p_repeat": 0.9, "dim": 2},
    },
]

TRIALS = list(range(10))
TREE_COMPARISON_MODELS = ["BST", "Optimal BST", "Splay Tree"]
NETWORK_COMPARISON_MODELS = ["BST Network", "Optimal BST Network", "SplayNet"]


def _compact_number(value, _pos=None):
    if value == 0:
        return "0"
    if abs(value) >= 1000000:
        return f"{value/1_000_000:.1f}M"
    if abs(value) >= 1000:
        return f"{value/1000:.0f}k"
    return f"{value:.0f}"


def _apply_compact_ticks(ax):
    ax.yaxis.set_major_formatter(FuncFormatter(_compact_number))
    ax.xaxis.set_major_formatter(FuncFormatter(_compact_number))


def _generate_requests(generator, n, m, args, seed):
    previous_state = random.getstate()
    random.seed(seed)
    try:
        return generator(n, m, **args)
    finally:
        random.setstate(previous_state)


def _compute_tree_trial_metrics(n, requests, seed):
    frequencies = request_frequencies(n, requests)
    optimal_bst = build_optimal_bst(n, frequencies)
    optimal_cost = np.zeros(len(requests), dtype=float)
    for index, request in enumerate(requests):
        optimal_bst.search(request)
        optimal_cost[index] = optimal_bst.search_cost

    bst_cost = np.zeros(len(requests), dtype=float)
    splay_cost = np.zeros(len(requests), dtype=float)
    splay_rotations = np.zeros(len(requests), dtype=float)

    for repeat_index in range(10):
        local_random = random.Random(seed + repeat_index * 997 + 17)
        bst = BinarySearchTree()
        splay_tree = SplayTree()

        keys = list(range(n))
        local_random.shuffle(keys)

        for key in keys:
            bst.insert(key)
            splay_tree.insert(key)

        for index, request in enumerate(requests):
            bst.search(request)
            splay_tree.search(request)
            bst_cost[index] += bst.search_cost
            splay_cost[index] += splay_tree.search_cost
            splay_rotations[index] += splay_tree.rotations

    bst_cost /= 10.0
    splay_cost /= 10.0
    splay_rotations /= 10.0

    return {
        "BST": bst_cost,
        "Optimal BST": optimal_cost,
        "Splay Tree": splay_cost,
        "Splay Tree Rotations": splay_rotations,
    }


def _compute_network_trial_metrics(n, requests, seed):
    request_matrix = requests_to_matrix(n, requests)
    optimal_network = build_optimal_bst_network(request_matrix)
    optimal_cost = np.zeros(len(requests), dtype=float)
    for index, (sender, receiver) in enumerate(requests):
        optimal_network.request(sender, receiver)
        optimal_cost[index] = optimal_network.total_communication_cost

    bst_network = BinarySearchTreeNetwork()
    splay_network = SplayNet()

    keys = list(range(n))
    local_random = random.Random(seed)
    local_random.shuffle(keys)
    for key in keys:
        bst_network.insert(key)
        splay_network.insert(key)

    bst_cost = np.zeros(len(requests), dtype=float)
    splay_cost = np.zeros(len(requests), dtype=float)
    splay_rotations = np.zeros(len(requests), dtype=float)

    for index, (sender, receiver) in enumerate(requests):
        bst_network.request(sender, receiver)
        splay_network.request(sender, receiver)

        bst_cost[index] = bst_network.total_communication_cost
        splay_cost[index] = splay_network.total_communication_cost
        splay_rotations[index] = splay_network.rotations

    return {
        "BST Network": bst_cost,
        "Optimal BST Network": optimal_cost,
        "SplayNet": splay_cost,
        "SplayNet Rotations": splay_rotations,
    }


def _summarize_series(series_matrix):
    array = np.asarray(series_matrix, dtype=float)
    return {
        "mean": np.mean(array, axis=0),
        "std": np.std(array, axis=0, ddof=0),
        "min": np.min(array, axis=0),
        "max": np.max(array, axis=0),
    }


def _write_summary_csv(path, experiment_name, metric_name, summary, x_values):
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["experiment", "metric", "query_index", "mean", "std", "min", "max"])
        for index in range(len(summary["mean"])):
            writer.writerow([
                experiment_name,
                metric_name,
                x_values[index],
                summary["mean"][index],
                summary["std"][index],
                summary["min"][index],
                summary["max"][index],
            ])


def _save_combined_figure(experiment_name, kind, model_names, model_summaries):
    prefix = "data_structure" if kind == "trees" else "network"
    path = FIGURES_DIR / kind / f"{prefix}_{experiment_name}"
    path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    palette = {
        "BST": "#1f77b4",
        "Optimal BST": "#2ca02c",
        "Splay Tree": "#d62728",
        "BST Network": "#1f77b4",
        "Optimal BST Network": "#2ca02c",
        "SplayNet": "#d62728",
        "Splay Tree Rotations": "#d62728",
        "SplayNet Rotations": "#d62728",
    }

    for model_name in model_names:
        summary = model_summaries[model_name]
        x_values = np.arange(len(summary["mean"]))
        color = palette.get(model_name, "#7f7f7f")
        linestyle = "--" if model_name.endswith("Rotations") else "-"
        ax.plot(
            x_values,
            summary["mean"],
            label=model_name,
            color=color,
            linewidth=2.3,
            linestyle=linestyle,
        )
        ax.fill_between(x_values, summary["min"], summary["max"], color=color, alpha=0.18, linewidth=0)

    ax.set_xlabel("Query Index", fontsize=11)
    ax.set_ylabel("Cumulative Metric", fontsize=11)
    ax.grid(True, which="major", alpha=0.15)
    _apply_compact_ticks(ax)

    ax.legend(
        loc="upper left",
        bbox_to_anchor=(0.02, 0.98),
        frameon=True,
        fancybox=False,
        edgecolor="#bdbdbd",
        facecolor="white",
        ncol=1,
        fontsize=10,
        borderpad=0.35,
        labelspacing=0.5,
        handlelength=1.8,
        handletextpad=0.6,
    )

    fig.subplots_adjust(left=0.16, right=0.96, top=0.92, bottom=0.14)

    pdf_path = path.parent / f"{path.name}.pdf"
    png_path = path.parent / f"{path.name}.png"
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    return path


def _benchmark_tree_experiment(experiment):
    name = experiment["name"]
    n = experiment["n"]
    m = experiment["m"]
    generator = experiment["generator"]
    args = experiment["args"]

    raw_records = []
    model_series = {
        "BST": [],
        "Optimal BST": [],
        "Splay Tree": [],
        "Splay Tree Rotations": [],
    }

    for seed in TRIALS:
        requests = _generate_requests(generator, n, m, args, seed)
        trial_metrics = _compute_tree_trial_metrics(n, requests, seed)
        for model_name, metric_values in trial_metrics.items():
            model_series[model_name].append(metric_values)
            for index, value in enumerate(metric_values):
                raw_records.append({
                    "experiment": name,
                    "kind": "tree",
                    "seed": seed,
                    "model": model_name,
                    "query_index": index,
                    "value": float(value),
                })

    raw_path = RAW_DIR / "trees" / f"{name}.csv"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    with raw_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["experiment", "kind", "seed", "model", "query_index", "value"])
        writer.writeheader()
        writer.writerows(raw_records)

    summary_dir = RESULTS_DIR / "summary" / "trees"
    summary_dir.mkdir(parents=True, exist_ok=True)
    for model_name, values in model_series.items():
        summary = _summarize_series(values)
        x_values = np.arange(len(summary["mean"]))
        summary_path = summary_dir / f"{name}_{model_name.lower().replace(' ', '_')}.csv"
        _write_summary_csv(summary_path, name, model_name, summary, x_values)

    comparison_summary = {
        model_name: _summarize_series(model_series[model_name])
        for model_name in TREE_COMPARISON_MODELS + ["Splay Tree Rotations"]
        if model_name in model_series
    }
    _save_combined_figure(name, "trees", list(comparison_summary.keys()), comparison_summary)

    return model_series


def _benchmark_network_experiment(experiment):
    name = experiment["name"]
    n = experiment["n"]
    m = experiment["m"]
    generator = experiment["generator"]
    args = experiment["args"]

    raw_records = []
    model_series = {
        "BST Network": [],
        "Optimal BST Network": [],
        "SplayNet": [],
        "SplayNet Rotations": [],
    }

    for seed in TRIALS:
        requests = _generate_requests(generator, n, m, args, seed)
        trial_metrics = _compute_network_trial_metrics(n, requests, seed)
        for model_name, metric_values in trial_metrics.items():
            model_series[model_name].append(metric_values)
            for index, value in enumerate(metric_values):
                raw_records.append({
                    "experiment": name,
                    "kind": "network",
                    "seed": seed,
                    "model": model_name,
                    "query_index": index,
                    "value": float(value),
                })

    raw_path = RAW_DIR / "networks" / f"{name}.csv"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    with raw_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["experiment", "kind", "seed", "model", "query_index", "value"])
        writer.writeheader()
        writer.writerows(raw_records)

    summary_dir = RESULTS_DIR / "summary" / "networks"
    summary_dir.mkdir(parents=True, exist_ok=True)
    for model_name, values in model_series.items():
        summary = _summarize_series(values)
        x_values = np.arange(len(summary["mean"]))
        summary_path = summary_dir / f"{name}_{model_name.lower().replace(' ', '_')}.csv"
        _write_summary_csv(summary_path, name, model_name, summary, x_values)

    comparison_summary = {
        model_name: _summarize_series(model_series[model_name])
        for model_name in NETWORK_COMPARISON_MODELS + ["SplayNet Rotations"]
        if model_name in model_series
    }
    _save_combined_figure(name, "networks", list(comparison_summary.keys()), comparison_summary)

    return model_series


def _format_experiment_name(name):
    if "hotset_" in name:
        return name.replace("hotset_", "hotset$_{") + "}$" if "hotset_" in name else name
    if "temporal_" in name:
        return name.replace("temporal_", "temporal$_{") + "}$" if "temporal_" in name else name
    return name


def _build_report_matrix(tree_results, network_results):
    rows = []

    def append_rows(kind, experiments, model_names, results_map):
        for experiment in experiments:
            name = experiment["name"]
            for model_name in model_names:
                if model_name not in results_map.get(name, {}):
                    continue
                summary = _summarize_series(results_map[name][model_name])
                rows.append({
                    "experiment": _format_experiment_name(name),
                    "kind": kind,
                    "model": model_name,
                    "metric": "access cost",
                    "mean": float(summary["mean"][-1]),
                    "std": float(summary["std"][-1]),
                })

                if model_name in {"Splay Tree", "SplayNet"}:
                    splay_summary = _summarize_series(results_map[name]["Splay Tree Rotations" if model_name == "Splay Tree" else "SplayNet Rotations"])
                    rows.append({
                        "experiment": _format_experiment_name(name),
                        "kind": kind,
                        "model": model_name,
                        "metric": "splay cost",
                        "mean": float(splay_summary["mean"][-1]),
                        "std": float(splay_summary["std"][-1]),
                    })

    append_rows("tree", TREE_EXPERIMENTS, ["BST", "Optimal BST", "Splay Tree"], tree_results)
    append_rows("network", NETWORK_EXPERIMENTS, ["BST Network", "Optimal BST Network", "SplayNet"], network_results)

    csv_path = REPORT_DIR / "results_matrix.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["experiment", "kind", "model", "metric", "mean", "std"]
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    tree_rows = [row for row in rows if row["kind"] == "tree"]
    network_rows = [row for row in rows if row["kind"] == "network"]

    def write_table(handle, rows_for_kind, caption, label):
        handle.write("\\begin{table}[t]\n")
        handle.write("\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write(f"\\label{{{label}}}\n")
        handle.write("\\begin{tabular}{llrr}\n")
        handle.write("\\toprule\n")
        handle.write("Experiment & Model & Mean & Std \\\\ \n")
        handle.write("\\midrule\n")
        for row in rows_for_kind:
            handle.write(f"{row['experiment']} & {row['model']} ({row['metric']}) & {row['mean']:.2f} & {row['std']:.2f} \\\\ \n")
        handle.write("\\bottomrule\n")
        handle.write("\\end{tabular}\n")
        handle.write("\\end{table}\n")

    tex_path = REPORT_DIR / "results_matrix.tex"
    with tex_path.open("w") as handle:
        handle.write("% Tree results\n")
        write_table(handle, tree_rows, "Final cumulative cost for the data-structure models.", "tab:tree_results")
        handle.write("\\n")
        handle.write("% Network results\n")
        write_table(handle, network_rows, "Final cumulative cost for the network models.", "tab:network_results")

    return rows


def run_all_experiments():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    tree_results = {experiment["name"]: _benchmark_tree_experiment(experiment) for experiment in TREE_EXPERIMENTS}
    network_results = {experiment["name"]: _benchmark_network_experiment(experiment) for experiment in NETWORK_EXPERIMENTS}

    report_rows = _build_report_matrix(tree_results, network_results)

    manifest = {
        "trials": TRIALS,
        "tree_experiments": [experiment["name"] for experiment in TREE_EXPERIMENTS],
        "network_experiments": [experiment["name"] for experiment in NETWORK_EXPERIMENTS],
        "results_dir": str(RESULTS_DIR),
    }

    with (RESULTS_DIR / "benchmark_manifest.json").open("w") as handle:
        json.dump(manifest, handle, indent=2)

    return {"trees": tree_results, "networks": network_results, "report_rows": report_rows}


if __name__ == "__main__":
    run_all_experiments()
    print(f"Benchmark outputs saved to: {RESULTS_DIR}")
