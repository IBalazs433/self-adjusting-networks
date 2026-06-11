# Self-Adjusting Networks

Master's thesis project on self-adjusting communication networks based on binary search trees.

The goal of this project is to implement and experimentally compare static and self-adjusting tree-based data structures and communication networks under different request distributions.

## Implemented Data Structures

* Binary Search Tree (BST)
* Optimal Static BST
* Splay Tree

## Implemented Networks

* Binary Search Tree Network
* Optimal Static BST Network
* SplayNet

## Implemented Workloads

* Uniform Random
* Temporal Locality 
* Hot-Set 

## Repository Structure

```text
nodes/
└── node.py

trees/
├── bst.py
├── optimal_bst.py
└── splay_tree.py

networks/
├── bst_network.py
├── optimal_network.py
└── splaynet.py

workloads/
├── uniform.py
├── temporal.py
└── hot_set.py

visualizations/
├── graph_visualization.py
└── results_visualization.py

tests/
├── test_trees.ipynb
└── test_networks.ipynb

experiments/
├── data_structures.ipynb
└── networks.ipynb
```

## Experimental Methodology

### Data Structures

The following data structures are evaluated:

* Binary Search Tree (BST)
* Optimal Static BST
* Splay Tree

Since the BST and Splay Tree depend on the insertion order of the keys, experiments are repeated over multiple random initializations and the reported results are averaged.

The Optimal Static BST is constructed from the request frequencies and serves as a static baseline.

Metrics:

* Search Cost
* Rotation Count

### Networks

The following communication networks are evaluated:

* BST Network
* Optimal Static BST Network
* SplayNet

As with the tree experiments, BST Network and SplayNet results are averaged over multiple random initializations.

The Optimal Static BST Network is constructed from the communication request matrix and serves as a static baseline.

Metrics:

* Total Communication Cost
* Rotation Count

## Visualization

The repository contains functions for:

* Binary tree visualization using NetworkX and Graphviz
* Experimental result visualization using Matplotlib

Left-child edges are displayed in blue and right-child edges in red.

## References

1. D. D. Sleator and R. E. Tarjan, *Self-Adjusting Binary Search Trees*, Journal of the ACM, 1985.

2. D. E. Knuth, *Optimum Binary Search Trees*, Acta Informatica, 1971.

3. C. Avin and S. Schmid, *Toward Demand-Aware Networking: A Theory for Self-Adjusting Networks*, SIGCOMM Computer Communication Review, 2019.

4. S. Schmid, C. Avin, C. Scheideler, M. Borokhovich, B. Haeupler, and Z. Lotker, *SplayNet: Towards Locally Self-Adjusting Networks*, IEEE/ACM Transactions on Networking, 2018.