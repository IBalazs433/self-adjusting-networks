# Self-Adjusting Networks

This repository studies self-adjusting binary-search trees and their network analogues under different workload patterns. The project combines algorithm implementations, reproducible workload generators, an experiment runner, and saved benchmark outputs for visual and tabular comparison.

## Current project state

As of August 2026, the codebase is a working research prototype with the core implementation in place and benchmark artifacts generated under `results/`.

Implemented pieces include:

- tree structures: BST, optimal static BST, and Splay Tree,
- network structures: BST network, optimal static BST network, and SplayNet,
- workload generators: uniform, hot-set, and temporal-locality request streams,
- deterministic multi-trial benchmarking and report generation in `experiments/benchmark_suite.py`,
- saved raw, summary, and report outputs, including comparison figures and CSV tables.

The project intentionally compares:

- static baselines versus self-adjusting methods,
- tree and network formulations of the same setting,
- cost under locality-free versus locality-heavy workloads,
- cumulative request cost alongside topology reconfiguration cost.

## Repository layout

```text
.
├── README.md
├── requirements.txt
├── experiments/
│   └── benchmark_suite.py
├── networks/
│   ├── bst_network.py
│   ├── optimal_network.py
│   └── splaynet.py
├── nodes/
│   └── node.py
├── results/
│   ├── benchmark_manifest.json
│   ├── figures/
│   ├── raw/
│   ├── report/
│   └── summary/
├── tests/
│   ├── conftest.py
│   ├── test_core_invariants.py
│   ├── test_network_notebook.py
│   └── test_tree_notebook.py
├── trees/
│   ├── bst.py
│   ├── optimal_bst.py
│   └── splay_tree.py
├── workloads/
│   ├── hot_set.py
│   ├── temporal.py
│   └── uniform.py
└── report artifacts generated under results/
```

## Benchmark coverage

The benchmark runner exercises six workload families for both trees and networks:

- uniform
- hotset_0.1
- hotset_0.3
- hotset_0.5
- temporal_0.5
- temporal_0.9

Each scenario evaluates:

- fixed BST / BST network baseline,
- optimal static tree / network reference,
- Splay Tree / SplayNet self-adjusting online method,
- repeated trials with seeded randomness,
- cumulative cost and reconfiguration / rotation counts.

## Generated outputs

The repository already contains benchmark artifacts in `results/`:

- `results/raw/`: per-run raw data
- `results/summary/`: reduced CSV summaries for trees and networks
- `results/report/`: LaTeX and CSV report outputs
- `results/figures/`: generated comparison plots for tree and network experiments
- `results/benchmark_manifest.json`: manifest of benchmark configuration and outputs

## Quick start

```bash
cd /path/to/self-adjusting-networks
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python experiments/benchmark_suite.py
```

To inspect the generated benchmark outputs:

```bash
ls results/
ls results/figures/trees
ls results/figures/networks
```

## References

1. D. D. Sleator and R. E. Tarjan, *Self-Adjusting Binary Search Trees*, Journal of the ACM, 1985.
2. D. E. Knuth, *Optimum Binary Search Trees*, Acta Informatica, 1971.
3. C. Avin and S. Schmid, *Toward Demand-Aware Networking: A Theory for Self-Adjusting Networks*, SIGCOMM Computer Communication Review, 2019.
4. S. Schmid, C. Avin, C. Scheideler, M. Borokhovich, B. Haeupler, and Z. Lotker, *SplayNet: Towards Locally Self-Adjusting Networks*, IEEE/ACM Transactions on Networking, 2018.