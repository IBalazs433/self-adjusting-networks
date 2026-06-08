from nodes.node import Node


class BinarySearchTreeNetwork:
    """
    A static communication network represented by a binary search tree.

    Each node in the tree corresponds to a network participant identified
    by a unique key. Communication requests between nodes are routed along
    tree paths, and the communication cost is defined as the distance
    between the communicating nodes.

    Attributes:
        root:
            Root of the binary search tree.

        total_communication_cost:
            Cumulative communication cost incurred by all processed
            communication requests.

    Methods:
        insert(key):
            Inserts a node with the given key into the network.

        search(key):
            Locate a node and return both the node reference and its depth.

        least_common_ancestor(key_u, key_v):
            Compute the least common ancestor of two nodes and its depth.

        request(key_u, key_v):
            Process a communication request between two nodes and update
            the cumulative communication cost.
    """

    def __init__(self):
        self.root = None
        self.total_communication_cost = 0


    def insert(self, key):
        """
        Inserts a node with the given key into the network.

        The node is placed according to the binary search tree property.

        Parameters:
            key:
                Unique identifier of the node.

        Returns:
            Node:
                Reference to the inserted node.

        Precondition:
            The key is not already in the tree.
        """

        if self.root is None:
            self.root = Node(key)
            return self.root

        current = self.root

        while True:
            if key < current.key:
                if current.left is None:
                    current.left = Node(key, parent=current)
                    return current.left
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(key, parent=current)
                    return current.right
                current = current.right

    def search(self, key):
        """
        Search for a node with the specified key.

        Parameters:
            key:
                key: The value to search for in the network.

        Returns:
                A pair consisting of
                - a reference to the node whose key equals the requested key,
                - the depth of that node measured from the root.

                If the key is not in the network, returns (None, 0).
        """

        current = self.root
        depth = 0

        if current is None:
            return None, 0

        while current is not None:
            if key == current.key:
                return current, depth
            elif key < current.key:
                current = current.left
                depth += 1
            else:
                current = current.right
                depth += 1
        
        return None, 0

    def least_common_ancestor(self, key_u, key_v):
        """
        Compute the least common ancestor of two nodes.

        The least common ancestor (LCA) of two nodes is the deepest node
        that is an ancestor of both.

        Parameters:
            key_u:
                Key of the first node.

            key_v:
                Key of the second node.

        Returns:
            tuple[Node | None, int]:
                A pair consisting of

                - the least common ancestor,
                - the depth of the least common ancestor.

                If the tree is empty, returns (None, 0).

        Precondition:
            Both keys are present in the tree.
        """

        current = self.root
        depth = 0

        if current is None:
            return None, 0

        while current is not None:
            if key_u < current.key and key_v < current.key:
                current = current.left
                depth += 1
            elif key_u > current.key and key_v > current.key:
                current = current.right
                depth += 1
            else:
                return current, depth

        return None, 0

    def request(self, key_u, key_v):
        """
        Process a communication request between two nodes.

        The communication cost equals the distance between the two nodes
        in the binary search tree. The cost is added to the cumulative
        communication cost maintained by the network.

        Parameters:
            key_u:
                Sender node identifier.

            key_v:
                Receiver node identifier.

        Returns:
            tuple[Node, Node, Node] | None:
                References to the sender, receiver and their least common
                ancestor if both nodes exist; otherwise None.
        """
        u, u_depth = self.search(key_u)
        v, v_depth = self.search(key_v)

        if u and v:
            lca, lca_depth = self.least_common_ancestor(key_u, key_v)

            # Distance between two nodes in the tree.
            cost = u_depth + v_depth - 2*lca_depth
            self.total_communication_cost += cost
            return u, v, lca
        
        return None, None, None