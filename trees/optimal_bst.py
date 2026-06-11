from trees.bst import BinarySearchTree


def optimal_bst_roots(n, freq):
    """
    Compute the root table of an optimal static binary search tree using
    bottom-up dynamic programming.

    For every interval [i, j], the algorithm determines the key that should
    be the root of the optimal subtree spanning key i, ..., key j.

    Args: 
        n: Number of keys.
        freq: Access frequencies corresponding to the keys.   

    Returns:
        Two-dimensional array where dp_roots[i][j] stores the index of 
        the root of the optimal subtree spanning the interval [i, j].

    Complexity:
        Time: O(n^3)
        Space: O(n^2)
    """

    # Compute prefix sums to obtain interval frequency sums in O(1).
    prefix_sums = [0 for _ in range(n+1)]
    for i in range(n):
        prefix_sums[i + 1] = prefix_sums[i] + freq[i]

    dp_cost = [[0 for _ in range(n)] for _ in range(n)]
    dp_roots = [[-1 for _ in range(n)] for _ in range(n)]

    # Base case: a single key forms an optimal subtree by itself.
    for i in range(n):
        dp_cost[i][i] = freq[i]
        dp_roots[i][i] = i

    # Process intervals in increasing order of length.
    for interval_length in range(2, n+1):
        for i in range(0, n-interval_length+1):
            j = i + interval_length - 1
            dp_cost[i][j] = float("inf")
            interval_frequency_sum = prefix_sums[j + 1] - prefix_sums[i]
            
            # Evaluate each key as a potential root of the interval [i, j].
            for root_index in range(i, j+1):
                cost = 0
                if root_index > i:
                    cost += dp_cost[i][root_index-1]
                if root_index < j:
                    cost += dp_cost[root_index+1][j]
                cost += interval_frequency_sum

                if cost < dp_cost[i][j]:
                    dp_cost[i][j] = cost
                    dp_roots[i][j] = root_index

    return dp_roots


def insertion_order(roots, i, j):
    """
    Compute the insertion order of keys from an optimal BST root table.

    The resulting sequence can be inserted into an empty binary search
    tree to reconstruct the optimal BST.

    Args: 
        roots: Root table produced by optimal_bst_roots(). 
        i: Left endpoint of the current interval. 
        j: Right endpoint of the current interval.

    Returns:
        List of key indices in preorder.
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


def build_optimal_bst(n, freq):
    """ 
    Construct an optimal static binary search tree. 

    Args: 
        n: Number of keys.
        freq: Access frequencies corresponding to the keys. 

    Returns: 
    BinarySearchTree representing the optimal static BST. 
    """
    
    roots = optimal_bst_roots(n, freq)
    order = [i for i in insertion_order(roots, 0, n-1)]

    tree = BinarySearchTree()
    for key in order:
        tree.insert(key)

    return tree


def request_frequencies(n, requests):
    """ 
    Compute access frequencies from a request sequence. 

    Args: 
        n: Number of keys. 
        requests: Sequence of access requests. 

    Returns: 
        List where the i-th element stores the number of requests for key i. 
    """

    frequencies = [0 for _ in range(n)]

    for request in requests:
        frequencies[request] += 1
    
    return frequencies