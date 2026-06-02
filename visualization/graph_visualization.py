import networkx as nx
import matplotlib.pyplot as plt


def build_graph(node, D=None):
    """
    Construct a NetworkX directed graph from a binary tree.

    Parameters:
        node: Root node of the subtree to convert.
        D: Existing graph to extend. If None, a new graph is created.

    Returns:
        A NetworkX DiGraph whose vertices correspond to tree nodes and 
        whose edges represent parent-child relationships.

    Notes:
        Left edges are labeled with type="L" and right edges with
        type="R".
    """

    if D is None:
        D = nx.DiGraph()

    if node is None:
        return D

    if node.left is not None:
        D.add_edge(node.key, node.left.key, type="L")
        build_graph(node.left, D)

    if node.right is not None:
        D.add_edge(node.key, node.right.key, type="R")
        build_graph(node.right, D)

    return D


def plot_tree(
    tree,
    title="",
    figsize=(5, 5),
    destination="",
    with_labels=True,
    node_size=1000,
    node_color="lightblue",
    arrows=False,
    ):
    """
    Visualize a binary tree using NetworkX and Graphviz.

    Parameters:
        tree: The binary tree to visualize.
        title: Figure title.
        figsize: Figure size as (width, height).
        destination: Output file path. If empty, the figure is not saved.
        with_labels: Whether node labels should be displayed.
        node_size: Size of the nodes.
        node_color: Color of the nodes.
        arrows: Whether directed edges should be drawn.

    Notes:
        Left child edges are drawn in blue and right child edges
        are drawn in red.
    """
    
    if tree.root is None:
        print("Tree is empty.")
        return

    plt.figure(figsize=figsize)
    D = build_graph(tree.root)
    pos = nx.nx_pydot.graphviz_layout(D, prog="dot")

    edge_colors = [
        "blue" if D[u][v]["type"] == "L" else "red"
        for u, v in D.edges()
    ]

    nx.draw(
        D, 
        pos,
        with_labels=with_labels,
        node_size=node_size,
        node_color=node_color,
        arrows=arrows,
        edge_color=edge_colors
    )

    plt.title(title)
    if destination:
        plt.savefig(destination)
    plt.show()