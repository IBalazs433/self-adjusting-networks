from node import Node


class SplayTree:
    """
    A bottom-up splay tree implementation.

    A splay tree is a self-adjusting binary search tree that moves recently
    accessed nodes to the root using rotations. Frequently accessed keys
    therefore tend to remain near the root

    Attributes: 
        root: Reference to the root node.

        search_cost: Cumulative number of nodes visited during search operations.

        rotations: Cumulative number of rotations during splay operations.

    Methods:
        insert(key): Inserts a node with the given key into the tree.

        search(key): Searches for a node with the given key. If the key is in the tree, 
                     then moves the corresponding node to the root.
    """

    def __init__(self):
        self.root = None
        self.search_cost = 0
        self.rotations = 0

    
    def insert(self, key):
        """
        Insert a node with the given key into the tree.

        Parameters:
            key: The value to insert.

        Returns:
            Node: A reference to the newly inserted node.
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
        Searches for a key in the tree.

        Parameters:
            key: The value to search for.

        Returns:
            A reference to the corresponding node if found,
            otherwise None.

        Side effects:
            Increments search_cost by the number of visited nodes.

            If the key is found, the node is moved to the root
            using the splay operation.
        """

        current = self.root

        if current is None:
            return None

        while current is not None:
            self.search_cost += 1
            if key == current.key:
                self.splay(current)
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        return None
    

    def splay(self, node):
        """
        Moves a node to the root using repeated tree rotations.
        This method repeatedly applies tree rotations until the node
        becomes the root, using Zig, ZigZig, and ZigZag operations.

        Parameters:
            node: The node to be moved to the root.

        Returns:
            A reference to the new root of the tree.

        Side effects:
            Changes the root of the tree to the node splayed up.
        
        """

        while node.parent is not None:
            p = node.parent
            g = p.parent

            # Case 1: The node is the child of the root.
            if g is None:
                if node.is_left_child:
                    self.rotate_right(node)
                else:
                    self.rotate_left(node)
            
            # Case 2: The node has a parent and a grandparent.
            # Apply either a Zig-Zig or Zig-Zag step.
            else:
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
    
    
    def reset_counters(self):
        """
        Resets all performance counters.
        """

        self.search_cost = 0
        self.rotations = 0