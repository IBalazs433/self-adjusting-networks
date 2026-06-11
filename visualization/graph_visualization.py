import networkx as nx
import matplotlib.pyplot as plt


def build_graph(node, graph=None):
    """
    Construct a NetworkX directed graph from a binary tree.

    Args:
        node: Root node of the subtree to convert.
        graph: Existing graph to extend. If None, a new graph is created.

    Returns:
        NetworkX DiGraph whose vertices correspond to tree nodes and
        whose edges represent parent-child relationships.

    Notes:
        Left-child edges are labeled with type="L" and right-child
        edges with type="R".
    """

    if graph is None:
        graph = nx.DiGraph()

    if node is None:
        return graph
    
    # Ensure isolated nodes are included in the graph.
    graph.add_node(node.key)

    if node.left is not None:
        graph.add_edge(node.key, node.left.key, type="L")
        build_graph(node.left, graph)

    if node.right is not None:
        graph.add_edge(node.key, node.right.key, type="R")
        build_graph(node.right, graph)

    return graph


def plot_tree(tree,
              title="",
              figsize=(5, 5),
              destination="",
              with_labels=True,
              node_size=1000,
              node_color="lightblue",
              arrows=False):
    """
    Visualize a binary tree using NetworkX and Graphviz.

    Args:
        tree: Binary tree to visualize.
        title: Figure title.
        figsize: Figure size as (width, height).
        destination: Output file path. If empty, the figure is not saved.
        with_labels: Whether node labels are displayed.
        node_size: Size of the nodes.
        node_color: Color of the nodes.
        arrows: Whether directed edges are drawn.

    Notes:
        Left-child edges are drawn in blue and right-child edges
        are drawn in red.
    """
    
    if tree.root is None:
        print("Tree is empty.")
        return

    plt.figure(figsize=figsize)
    graph = build_graph(tree.root)
    pos = nx.nx_pydot.graphviz_layout(graph, prog="dot")

    edge_colors = [
        "blue" if graph[u][v]["type"] == "L" else "red"
        for u, v in graph.edges()
    ]

    nx.draw(graph, 
            pos,
            with_labels=with_labels,
            node_size=node_size,
            node_color=node_color,
            arrows=arrows,
            edge_color=edge_colors)

    plt.title(title)
    if destination:
        plt.savefig(destination)
    plt.show()