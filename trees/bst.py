from node import Node

class BinarySearchTree:
    """
    A binary search tree (BST) implementation.

    Attributes: 
        root: Reference to the root node.
        hop_count: Cumulative number of nodes visited during search operations.

    Methods:
        insert(key): 
            Inserts a node with the given key into the tree.

            Returns:
                A reference to the newly inserted node.
        
        search(key):
            Searches for a node with the given key.

            Returns:
                A reference to the node if found, otherwise None.

            Side effects:
                Increments hop_count by the number of nodes visited during the search.
    """


    def __init__(self, hop_count=0):
        self.root = None
        self.hop_count = hop_count


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
        Searches for a node with the given key.

        Parameters: 
            key: The value to search for in the tree.

        Returns:
            A reference to the node if found, otherwise None.

        Side effects:
            Increments hop_count by the number of nodes visited during the search.
        """

        current = self.root

        if current is None:
            self.hop_count += 1

        while current is not None:
            self.hop_count += 1
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        return None