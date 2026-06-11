from nodes.node import Node


class BinarySearchTree:
    """
    Binary search tree (BST) implementation.

    Attributes:
        root: Root node of the tree, or None if the tree is empty.
        search_cost: Cumulative number of nodes visited during search operations.
    """

    def __init__(self):
        self.root = None
        self.search_cost = 0


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
        """

        current_node = self.root

        if current_node is None:
            return None

        while current_node is not None:
            self.search_cost += 1
            if key == current_node.key:
                return current_node
            elif key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
        
        return None