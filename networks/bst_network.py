from nodes.node import Node


class BinarySearchTreeNetwork:
    """
    Static communication network represented by a binary search tree.

    Each node corresponds to a network participant identified by a unique
    key. Communication requests are routed along tree paths, and the
    communication cost is defined as the distance between the
    communicating nodes.

    Attributes:
        root: Root node of the network, or None if the network is empty.
        total_communication_cost: Cumulative communication cost of all
            processed requests.
    """

    def __init__(self):
        self.root = None
        self.total_communication_cost = 0


    def insert(self, key):
        """
        Insert a node with the given key into the network.

        Args:
            key: Unique identifier of the node.

        Returns:
            Reference to the newly inserted node.

        Precondition:
            The key is not already present in the network.
        """

        if self.root is None:
            self.root = Node(key)
            return self.root

        current_node = self.root

        while True:
            if key < current_node.key:
                if current_node.left is None:
                    current_node.left = Node(key, parent=current_node)
                    return current_node.left
                current_node = current_node.left
            else:
                if current_node.right is None:
                    current_node.right = Node(key, parent=current_node)
                    return current_node.right
                current_node = current_node.right


    def search(self, key):
        """
        Search for a node with the specified key.

        Args:
            key: Key to search for.

        Returns:
            A pair consisting of:

            - the corresponding node,
            - the depth of the node measured from the root.

            If the key is not present, returns (None, 0).
        """

        current_node = self.root
        depth = 0

        if current_node is None:
            return None, 0

        while current_node is not None:
            if key == current_node.key:
                return current_node, depth
            elif key < current_node.key:
                current_node = current_node.left
                depth += 1
            else:
                current_node = current_node.right
                depth += 1
        
        return None, 0


    def least_common_ancestor(self, sender_key, receiver_key):
        """
        Compute the least common ancestor of two nodes.

        The least common ancestor (LCA) is the deepest node that is an
        ancestor of both nodes.

        Args:
            sender_key: Key of the sender node.
            receiver_key: Key of the receiver node.

        Returns:
            A pair consisting of:

            - the least common ancestor,
            - the depth of the least common ancestor.

            If the network is empty, returns (None, 0).

        Precondition:
            Both keys are present in the network.
        """

        current = self.root
        depth = 0

        if current is None:
            return None, 0

        while current is not None:
            if sender_key < current.key and receiver_key < current.key:
                current = current.left
                depth += 1
            elif sender_key > current.key and receiver_key > current.key:
                current = current.right
                depth += 1
            else:
                return current, depth

        return None, 0
    

    def request(self, sender_key, receiver_key):
        """
        Process a communication request between two nodes.

        The communication cost equals the distance between the two nodes
        in the tree. This cost is added to the cumulative communication
        cost maintained by the network.

        Args:
            sender_key: Key of the sender node.
            receiver_key: Key of the receiver node.

        Returns:
            References to the sender, receiver, and their least common
            ancestor if both nodes exist; otherwise (None, None, None).
        """

        sender, sender_depth = self.search(sender_key)
        receiver, receiver_depth = self.search(receiver_key)

        if sender and receiver:
            lca, lca_depth = self.least_common_ancestor(sender_key, receiver_key)

            # Compute the communication cost as the tree distance.
            cost = sender_depth + receiver_depth - 2*lca_depth
            self.total_communication_cost += cost
            return sender, receiver, lca
        
        return None, None, None