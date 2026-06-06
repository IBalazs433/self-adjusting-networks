from trees.bst import BinarySearchTree


def optimal_bst_roots(keys, freq):
    """
    Computes the root table of an optimal static binary search tree using
    bottom-up dynamic programming.

    For every interval [i, j], the algorithm determines the key that should
    be the root of the optimal subtree spanning keys[i], ..., keys[j+1].

    Parameters:
        keys: List of keys.
        freq: List of access frequencies corresponding to the keys.

    Returns:
        A two-dimensional array dp_roots, dp_roots[i][j] stores the
        index of the root of the optimal subtree for the interval [i, j].

    Complexity:
        Time: O(n^3)
        Space: O(n^2)
    """
    
    n = len(keys)

    # Prefix sums of frequencies
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + freq[i]

    dp_cost = [[0 for _ in range(n)] for _ in range(n)]
    dp_roots = [[-1 for _ in range(n)] for _ in range(n)]

    # If there is only a single key, the cost is the frequency of the key
    for i in range(n):
        dp_cost[i][i] = freq[i]
        dp_roots[i][i] = i

    # Consider intervals in increasing order of length.
    # For each interval [i, j], evaluate every possible root and
    # choose the one yielding the minimum search cost.
    for l in range(2, n+1):
        for i in range(0, n-l+1):
            j = i + l - 1
            dp_cost[i][j] = float("inf")
            rsum = prefix[j + 1] - prefix[i]
            
            # Evaluate key r as the root of the subtree spanning [i, j].
            for r in range(i, j+1):
                cost = 0
                if r > i:
                    cost += dp_cost[i][r-1]
                if r < j:
                    cost += dp_cost[r+1][j]
                cost += rsum

                if cost < dp_cost[i][j]:
                    dp_cost[i][j] = cost
                    dp_roots[i][j] = r

    return dp_roots

def insertion_order(roots, i, j):
    """
    Computes the insertion order of the keys of the optimal BST represented by a root table.

    The resulting sequence can be inserted into an empty binary search tree
    to reconstruct the same tree structure.

    Parameters:
        roots: Root table produced by minBST().
        i: Left endpoint of the current interval.
        j: Right endpoint of the current interval.

    Returns:
        A list containing the indices of the keys in preorder.
    """
    if i > j:
        return []

    r = roots[i][j]
    left = []
    right = []

    if r > i:
        left = insertion_order(roots, i, r-1)
    if r < j:
        right = insertion_order(roots, r+1, j)

    return [r] + left + right

def build_optimal_bst(keys, freq):
    """
    Constructs an optimal static binary search tree from a set of keys and
    their access frequencies.

    Parameters:
        keys: List of keys.
        freq: List of access frequencies corresponding to the keys.

    Returns:
        The optimal static BST as a BinarySearchTree object.
    """
    roots = optimal_bst_roots(keys, freq)
    order = [keys[i] for i in insertion_order(roots, 0, len(keys)-1)]

    tree = BinarySearchTree()
    for key in order:
        tree.insert(key)

    return tree