from nodes.node import Node

class SplayNet:
    """
    This is the implementation of SplayNet.
    """

    def __init__(self):
        self.root = None
        self.total_communication_cost = 0
        self.rotations = 0

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
        Searches for a node with the given key.

        Parameters: 
            key: The value to search for in the tree.

        Returns:
            A reference to the node if found, otherwise None.
        """

        current = self.root

        if current is None:
            return None

        while current is not None:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        return None

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
                A reference to the least common ancestor if exists, otherwise None.

        Precondition:
            Both keys are present in the tree.
        """

        current = self.root

        if current is None:
            return None

        while current is not None:
            if key_u < current.key and key_v < current.key:
                current = current.left
            elif key_u > current.key and key_v > current.key:
                current = current.right
            else:
                return current

        return None 

    def request(self, s_key, t_key):
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
        s = self.search(s_key)
        t = self.search(t_key)

        if s and t:
            self.total_communication_cost += 1
            lca = self.least_common_ancestor(s_key, t_key)
            self.splay(s, lca)
            if s_key < t_key:
                self.splay(t, s.right)
            else:
                self.splay(t, s.left)

            return s, t, lca

        return None, None, None
    
    def splay(self, node, stop_node):
        """
        Moves a node to the stop_node by repeated tree rotations.
        This method repeatedly applies tree rotations until the node
        is in the place of stop_node, using Zig, ZigZig, and ZigZag operations.

        Parameters:
            node: The node to be moved to the root.
            stop_node:

        Returns:
            A reference to the node.
        """
        
        if node == stop_node:
            return node

        while True:
            
            p = node.parent
            if p == stop_node:
                if node.is_left_child:
                    self.rotate_right(node)
                else:
                    self.rotate_left(node)
                return node
            
            g = p.parent
            if g == stop_node:
                if node.is_left_child and p.is_left_child:
                    self.rotate_right(p)
                    self.rotate_right(node)

                elif node.is_right_child and p.is_right_child:
                    self.rotate_left(p)
                    self.rotate_left(node)

                elif node.is_left_child and p.is_right_child:
                    self.rotate_right(node)
                    self.rotate_left(node)

                elif node.is_right_child and p.is_left_child:
                    self.rotate_left(node)
                    self.rotate_right(node)
                return node
                
            if node.is_left_child and p.is_left_child:
                self.rotate_right(p)
                self.rotate_right(node)

            elif node.is_right_child and p.is_right_child:
                self.rotate_left(p)
                self.rotate_left(node)

            elif node.is_left_child and p.is_right_child:
                self.rotate_right(node)
                self.rotate_left(node)

            elif node.is_right_child and p.is_left_child:
                self.rotate_left(node)
                self.rotate_right(node)


    def rotate_right(self, node):
        """
        Performs a right rotation around the given node and their parent.

        Parameters:
            node: The child node that moves up during rotation.

        Returns:
            A reference to the node moved higher.

        Side effects:
            The node becomes the parent of its current parent. 
            The binary search tree relations are updated accordingly.
        """

        self.rotations += 1

        p = node.parent
        g = p.parent

        p.left = node.right
        if node.right is not None:
            node.right.parent = p
        node.right = p
        p.parent = node
        node.parent = g
        if g is not None:
            if g.left == p:
                g.left = node
            else:
                g.right = node
        
        if self.root is p:
            self.root = node
        
        return node


    def rotate_left(self, node):
        """
        Performs a left rotation around the given node and their parent.

        Parameters:
            node: The child node that moves up during rotation.

        Returns:
            A reference to the node moved higher.

        Side effects:
            The node becomes the parent of its current parent. 
            The binary search tree relations are updated accordingly.
        """

        self.rotations += 1

        p = node.parent
        g = p.parent

        p.right = node.left
        if node.left:
            node.left.parent = p
        node.left = p
        p.parent = node
        node.parent = g
        if g is not None:
            if g.left == p:
                g.left = node
            else:
                g.right = node

        if self.root is p:
            self.root = node
        
        return node
    