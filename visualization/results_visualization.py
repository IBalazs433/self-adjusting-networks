import matplotlib.pyplot as plt


def plot_tree_metrics(bst_search_cost,
                      optimal_bst_search_cost,
                      splay_tree_search_cost,
                      splay_tree_rotations,
                      logarithmic=False):
    """
    Plot cumulative performance metrics for tree data structures.

    Args:
        BST_search_cost: Search cost history of the binary search tree.
        opt_BST_search_cost: Search cost history of the optimal BST.
        ST_search_cost: Search cost history of the splay tree.
        ST_rotations: Rotation count history of the splay tree.
        logarithmic: Whether logarithmic scales should be used on both axes.
    """

    plt.figure()
    plt.plot(bst_search_cost, label="BST Search Cost")
    plt.plot(optimal_bst_search_cost, label="Opt BST Search Cost")
    plt.plot(splay_tree_search_cost, label="Splay Tree Search Cost")
    plt.plot(splay_tree_rotations, label="Splay Tree Rotations")

    if logarithmic:
        plt.yscale("log")
        plt.xscale("log")

    plt.legend()
    plt.xlabel("Query Index")
    plt.ylabel("Count")
    plt.show()


def plot_network_metrics(bst_network_communication_cost,
                         optimal_bst_network_communication_cost,
                         splaynet_communication_cost,
                         splaynet_rotations,
                         logarithmic=False):
    """
    Plot cumulative performance metrics for network structures.

    Args:
        BST_net_total_communication_cost: Communication cost history of the BST network.
        opt_BST_net_total_communication_cost: Communication cost history of the optimal BST network.
        SplayNet_total_communication_cost: Communication cost history of SplayNet.
        SplayNet_rotations: Rotation count history of SplayNet.
        logarithmic: Whether logarithmic scales should be used on both axes.
    """

    plt.figure()
    plt.plot(bst_network_communication_cost, label="BST Net Total Communication Cost")
    plt.plot(optimal_bst_network_communication_cost, label="Opt BST Net Total Communication Cost")
    plt.plot(splaynet_communication_cost, label="SplayNet Total Communication Cost")
    plt.plot(splaynet_rotations, label="SplayNet Rotation Count")

    if logarithmic:
        plt.yscale("log")
        plt.xscale("log")

    plt.legend()
    plt.xlabel("Query Index")
    plt.ylabel("Count")
    plt.show()