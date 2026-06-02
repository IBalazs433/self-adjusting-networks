class Node:
    """
    A node in a binary tree.

    Attributes:
        key: The value stored in the node.
        parent: Reference to the parent node, or None if the node is the root.
        left: Reference to the left child node, or None.
        right: Reference to the right child node, or None.

    Properties:
        is_left_child: True if the node is the left child of its parent.
        is_right_child: True if the node is the right child of its parent.
        is_root: True if the node has no parent.

    Methods:
        __str__: 
            Returns a string representation of the node.
    """

    def __init__(self, key, parent=None):
        self.key = key
        self.parent = parent
        self.left = None
        self.right = None

    def __str__(self):
        return f"Node({self.key})"

    @property
    def is_left_child(self):
        return (self.parent is not None) and (self.parent.left is self)

    @property
    def is_right_child(self):
        return (self.parent is not None) and (self.parent.right is self)

    @property
    def is_root(self):
        return self.parent is None