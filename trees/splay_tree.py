from nodes.node import Node


class SplayTree:
    """
    Bottom-up splay tree implementation.

    A splay tree is a self-adjusting binary search tree that moves recently
    accessed nodes to the root using rotations. Frequently accessed keys
    therefore tend to remain near the root.

    Attributes:
        root: Root node of the tree, or None if the tree is empty.
        search_cost: Cumulative number of nodes visited during search operations.
        rotations: Cumulative number of rotations performed during splaying.
    """

    def __init__(self):
        self.root = None
        self.search_cost = 0
        self.rotations = 0

    
    def insert(self, key):
        """
        Insert a node with the given key into the tree.

        Args:
            key: Key of the node to insert.

        Returns:
            Reference to the newly inserted node.
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
        Search for a node with the given key.

        Args:
            key: Key to search for.

        Returns:
            The corresponding node if found, otherwise None.

        Side Effects:
            Increments search_cost by the number of visited nodes.

            If the key is found, the corresponding node is splayed to
            the root of the tree.
        """

        current_node = self.root

        if current_node is None:
            return None

        while current_node is not None:
            self.search_cost += 1
            if key == current_node.key:
                self.splay(current_node)
                return current_node
            elif key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
        
        return None
    

    def splay(self, node):
        """
        Move a node to the root using repeated tree rotations.

        The procedure applies Zig, Zig-Zig, and Zig-Zag steps until
        the node becomes the root of the tree.

        Args:
            node: Node to splay.

        Returns:
            The node after it has been moved to the root.

        Side Effects:
            Modifies the tree structure and updates the root.
        """

        while node.parent is not None:
            parent = node.parent
            grandparent = parent.parent

            # Zig step: the parent is the root.
            if grandparent is None:
                if node.is_left_child:
                    self.rotate_right(node)
                else:
                    self.rotate_left(node)
            
            
            else:
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