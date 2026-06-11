from networks.bst_network import BinarySearchTreeNetwork


def optimal_static_network_roots(request_matrix):
    """
    Compute the root table of an optimal static BST network.

    The algorithm uses dynamic programming to determine the root of
    each interval that minimizes the total communication cost induced
    by the request matrix.

    Args:
        R: Communication request matrix, where R[u][v] denotes the
            number of requests from node u to node v.

    Returns:
        Two-dimensional array where dp_root[i][j] stores the index
        of the optimal root for interval [i, j].

    Complexity:
        Time: O(n^4)
        Space: O(n^2)
    """

    n = len(request_matrix)
    
    dp_cost = [[0 for _ in range(n)] for _ in range(n)]
    dp_roots = [[-1 for _ in range(n)] for _ in range(n)]

    # Precompute interval weights used in the dynamic program.
    W = [[None for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            vec = [0 for _ in range(n)]

            for v in range(i, j+1):
                total = 0
                for u in range(n):
                    if not(i <= u <= j):
                        total += request_matrix[u][v] + request_matrix[v][u]

                vec[v] = total
            W[i][j] = vec      

    # Base case: a single node forms a network of zero internal cost.
    for i in range(n):
        dp_roots[i][i] = i
        dp_cost[i][i] = 0

    # Process intervals in increasing order of length.
    for interval_length in range(2, n+1):
        for i in range(0, n-interval_length+1):
            j = i+interval_length-1
            best_cost = float("inf")
            best_root = -1

            WI = W[i][j]

            # Evaluate each node as a candidate root.
            for root_index in range(i, j+1):
                cost = 0
                if root_index > i:
                    cost += dp_cost[i][root_index-1]
                if root_index < j:
                    cost += dp_cost[root_index+1][j]
                
                # Account for the depth increase induced by the chosen root.
                for v in range(i, root_index):
                    cost += WI[v]
                for v in range(root_index+1, j+1):
                    cost += WI[v]
                
                if cost < best_cost:
                    best_cost = cost
                    best_root = root_index
            
            dp_cost[i][j] = best_cost
            dp_roots[i][j] = best_root
    
    return dp_roots


def insertion_order(roots, i, j):
    """
    Compute the insertion order of keys from an optimal static 
    network root table.

    TThe resulting sequence can be inserted into an empty binary search
    tree network to reconstruct the optimal topology.

    Args: 
        roots: Root table produced by optimal_static_network_roots(). 
        i: Left endpoint of the current interval. 
        j: Right endpoint of the current interval.

    Returns:
        List of key indices in preorder.
    """

    if i > j:
        return []

    root_index = roots[i][j]
    left = []
    right = []

    if root_index > i:
        left = insertion_order(roots, i, root_index-1)
    if root_index < j:
        right = insertion_order(roots, root_index+1, j)

    return [root_index] + left + right


def build_optimal_bst_network(request_matrix):
    """
    Construct an optimal static BST network.

    Args:
        R: Communication request matrix.

    Returns:
        BinarySearchTreeNetwork representing the optimal static network.
    """

    roots = optimal_static_network_roots(request_matrix)
    order = insertion_order(roots, 0, len(request_matrix)-1)

    net = BinarySearchTreeNetwork()
    for key in order:
        net.insert(key)

    return net


def requests_to_matrix(n, requests):
    """
    Convert a communication request sequence into a request matrix.

    Args:
        n: Number of network nodes.
        requests: Sequence of communication requests represented as
            (sender, receiver) pairs.

    Returns:
        Request matrix R where R[u][v] stores the number of requests
        from node u to node v.
    """
    request_matrix = [[0 for _ in range(n)] for _ in range(n)]

    for request in requests:
        request_matrix[request[0]][request[1]] += 1

    return request_matrix