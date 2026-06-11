from nodes.node import Node

class SplayNet:
    """
    SplayNet communication network.

    SplayNet is a self-adjusting network based on a binary search tree.
    After serving a communication request, the network performs local
    rotations to adapt its topology to the observed communication pattern.

    Attributes:
        root: Root node of the network.
        total_communication_cost: Cumulative communication cost of all
            processed requests.
        rotations: Cumulative number of rotations performed during
            network reconfiguration.
    """

    def __init__(self):
        self.root = None
        self.total_communication_cost = 0
        self.rotations = 0


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
            The corresponding node if found, otherwise None.
        """

        current_node = self.root

        if current_node is None:
            return None

        while current_node is not None:
            if key == current_node.key:
                return current_node
            elif key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
        
        return None

    def least_common_ancestor(self, sender_key, receiver_key):
        """
        Compute the least common ancestor of two nodes.

        The least common ancestor (LCA) is the deepest node that is an
        ancestor of both nodes.

        Args:
            sender_key: Key of the first node.
            receiver_key: Key of the second node.

        Returns:
            Reference to the least common ancestor if it exists,
            otherwise None.

        Precondition:
            Both keys are present in the network.
        """

        current_node = self.root

        if current_node is None:
            return None

        while current_node is not None:
            if sender_key < current_node.key and receiver_key < current_node.key:
                current_node = current_node.left
            elif sender_key > current_node.key and receiver_key > current_node.key:
                current_node = current_node.right
            else:
                return current_node

        return None 

    def request(self, sender_key, receiver_key):
        """
        Process a communication request between two nodes.

        The request is served according to the SplayNet algorithm.
        After identifying the communicating nodes and their least
        common ancestor, local splay operations are performed to
        adapt the network topology.

        Args:
            sender_key: Sender node identifier.
            receiver_key: Receiver node identifier.

        Returns:
            References to the sender, receiver, and their least
            common ancestor if both nodes exist; otherwise
            (None, None, None).
        """
        sender = self.search(sender_key)
        receiver = self.search(receiver_key)

        if sender and receiver:
            self.total_communication_cost += 1
            lca = self.least_common_ancestor(sender_key, receiver_key)
            self.splay(sender, lca)
            if sender_key < receiver_key:
                self.splay(receiver, sender.right)
            else:
                self.splay(receiver, sender.left)

            return sender, receiver, lca

        return None, None, None
    
    def splay(self, node, stop_node):
        """
        Move a node toward a specified stop node using rotations.

        The procedure applies Zig, Zig-Zig, and Zig-Zag steps until
        the node reaches the position immediately below the stop node
        or replaces the stop node.

        Args:
            node: Node to be moved.
            stop_node: Ancestor at which the splaying process stops.

        Returns:
            The moved node.
        """
        
        if node == stop_node:
            return node

        while True:
            parent = node.parent
            if parent == stop_node:
                # Zig step: the parent is the stop_node.
                if node.is_left_child:
                    self.rotate_right(node)
                else:
                    self.rotate_left(node)
                return node
            
            grandparent = parent.parent
            # Zig-Zig step: node and parent are on the same side.
            if node.is_left_child and parent.is_left_child:
                self.rotate_right(parent)
                self.rotate_right(node)

            elif node.is_right_child and parent.is_right_child:
                self.rotate_left(parent)
                self.rotate_left(node)

            # Zig-Zag step: node and parent are on opposite sides.
            elif node.is_left_child and parent.is_right_child:
                self.rotate_right(node)
                self.rotate_left(node)

            elif node.is_right_child and parent.is_left_child:
                self.rotate_left(node)
                self.rotate_right(node)

            # Stop after the final step.
            if grandparent == stop_node:
                return node


    def rotate_right(self, node):
        """
        Perform a right rotation between a node and its parent.

        Args:
            node: Child node that moves above its parent.

        Returns:
            The promoted node.

        Side Effects:
            Updates parent-child relationships while preserving the
            binary search tree property.
        """

        self.rotations += 1

        parent = node.parent
        grandparent = parent.parent

        parent.left = node.right
        if node.right is not None:
            node.right.parent = parent
        node.right = parent
        parent.parent = node
        node.parent = grandparent
        if grandparent is not None:
            if grandparent.left == parent:
                grandparent.left = node
            else:
                grandparent.right = node
        
        if self.root is parent:
            self.root = node
        
        return node


    def rotate_left(self, node):
        """
        Perform a left rotation between a node and its parent.

        Args:
            node: Child node that moves above its parent.

        Returns:
            The promoted node.

        Side Effects:
            Updates parent-child relationships while preserving the
            binary search tree property.
        """

        self.rotations += 1

        parent = node.parent
        grandparent = parent.parent

        parent.right = node.left
        if node.left:
            node.left.parent = parent
        node.left = parent
        parent.parent = node
        node.parent = grandparent
        if grandparent is not None:
            if grandparent.left == parent:
                grandparent.left = node
            else:
                grandparent.right = node

        if self.root is parent:
            self.root = node
        
        return node