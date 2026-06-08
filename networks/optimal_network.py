from networks.bst_network import BinarySearchTreeNetwork


def optimal_static_network_roots(R):
    n = len(R)
    
    dp_cost = [[0 for _ in range(n)] for _ in range(n)]
    dp_root = [[-1 for _ in range(n)] for _ in range(n)]


    W = [[None for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            vec = [0 for _ in range(n)]

            for v in range(i, j+1):
                total = 0
                for u in range(n):
                    if not(i <= u <= j):
                        total += R[u][v] + R[v][u]

                vec[v] = total
            W[i][j] = vec
                

    for i in range(n):
        dp_root[i][i] = i
        dp_cost[i][i] = 0

    for l in range(2, n+1):
        for i in range(0, n-l+1):
            j = i+l-1
            best_cost = float("inf")
            best_root = -1

            WI = W[i][j]

            for r in range(i, j+1):
                cost = 0
                if r > i:
                    cost += dp_cost[i][r-1]
                if r < j:
                    cost += dp_cost[r+1][j]
                
                # depth increase term
                for v in range(i, r):
                    cost += WI[v]
                for v in range(r+1, j+1):
                    cost += WI[v]
                
                if cost < best_cost:
                    best_cost = cost
                    best_root = r
            
            dp_cost[i][j] = best_cost
            dp_root[i][j] = best_root
    
    return dp_root


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

def build_optimal_bst(R):
    """
    Constructs an optimal static binary search tree from a set of keys and
    their access frequencies.

    Parameters:
        keys: List of keys.
        freq: List of access frequencies corresponding to the keys.

    Returns:
        The optimal static BST as a BinarySearchTree object.
    """
    roots = optimal_static_network_roots(R)
    order = insertion_order(roots, 0, len(R)-1)

    net = BinarySearchTreeNetwork()
    for key in order:
        net.insert(key)

    return net