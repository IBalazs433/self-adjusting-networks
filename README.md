# Self-Adjusting Networks

Master's thesis project on self-adjusting communication networks based on binary search trees.

The goal of this project is to implement and compare static and self-adjusting tree-based network topologies under different communication workloads.

## Implemented Data Structures

- Binary Search Tree (BST)
- Optimal Static BST
- Splay Tree

## Implemented Networks

- BST-Based Network
- Optimal Static Network
- SplayNet

## Workloads

- Uniform Random Requests
- Zipf-Distributed Requests
- Temporal Locality Requests

## Repository Structure

```text
src/
├── trees/
│   ├── node.py
│   ├── bst.py
│   ├── optimal_bst.py
│   └── splay_tree.py
│
├── networks/
│   ├── bst_network.py
│   ├── optimal_network.py
│   └── splaynet.py
│
├── workloads/
│   ├── uniform.py
│   ├── zipf.py
│   └── temporal_locality.py
│
├── experiments/
│   └── run_experiments.py
│
└── visualization/
    └── plots.py
```

## Running Experiments

Run:

```bash
python src/experiments/run_experiments.py
```

The script generates communication requests, executes the selected network models, and stores the results.

## Results

Experimental results are stored in CSV format and can be visualized using:

```bash
python src/visualization/plots.py
```

## References

## References

1. Sleator, D. D., & Tarjan, R. E. *Self-Adjusting Binary Search Trees* (1985).
2. Knuth, D. E. *Optimum Binary Search Trees* (1971).
3. Avin, C., & Schmid, S. *Toward Demand-Aware Networking: A Theory for Self-Adjusting Networks* (2019).
4. Schmid, S., Avin, C., Scheideler, C., Borokhovich, M., Haeupler, B., & Lotker, Z. *SplayNet: Towards Locally Self-Adjusting Networks* (2018).


