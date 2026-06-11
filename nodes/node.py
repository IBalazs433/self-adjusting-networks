class Node:
    """
    Node of a binary tree.

    Attributes:
        key: Unique identifier of the node.
        parent: Parent node, or None if the node is the root.
        left: Left child node, or None.
        right: Right child node, or None.

    Properties:
        is_left_child: True if the node is the left child of its parent.
        is_right_child: True if the node is the right child of its parent.
    """


    def __init__(self, key, parent=None):
        self.key = key
        self.parent = parent
        self.left = None
        self.right = None


    def __str__(self):
        """
        Return a string representation of the node.
        """
        return f"Node({self.key})"


    @property
    def is_left_child(self):
        """
        Check whether the node is the left child of its parent.
        """
        return (self.parent is not None) and (self.parent.left is self)


    @property
    def is_right_child(self):
        """
        Check whether the node is the right child of its parent.
        """
        return (self.parent is not None) and (self.parent.right is self)