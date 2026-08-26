import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from trees.bst import BinarySearchTree
from trees.optimal_bst import build_optimal_bst
from trees.splay_tree import SplayTree


def test_bst_empty_tree():
    tree = BinarySearchTree()
    assert tree.root is None
    assert tree.search(5) is None


def test_bst_insert_root_and_children():
    tree = BinarySearchTree()
    node = tree.insert(10)

    assert tree.root is node
    assert node.key == 10
    assert node.parent is None


def test_bst_insert_left_and_right_children():
    tree = BinarySearchTree()
    root = tree.insert(10)
    left = tree.insert(5)
    right = tree.insert(15)

    assert root.left is left
    assert root.right is right
    assert left.parent is root
    assert right.parent is root
    assert left.is_left_child
    assert right.is_right_child


def test_bst_structure():
    tree = BinarySearchTree()
    for x in [10, 5, 15, 3, 7, 12, 20]:
        tree.insert(x)

    assert tree.root.key == 10
    assert tree.root.left.key == 5
    assert tree.root.right.key == 15
    assert tree.root.left.left.key == 3
    assert tree.root.left.right.key == 7
    assert tree.root.right.left.key == 12
    assert tree.root.right.right.key == 20


def test_bst_search_and_cost_tracking():
    tree = BinarySearchTree()
    for x in [10, 5, 15, 3]:
        tree.insert(x)

    assert tree.search_cost == 0
    assert tree.search(3).key == 3
    assert tree.search(7) is None
    assert tree.search_cost == 5

    tree.search_cost = 0
    tree.search(3)
    assert tree.search_cost == 3


def test_optimal_bst_single_key():
    tree = build_optimal_bst(1, [10])
    assert tree.root.key == 0
    assert tree.root.left is None
    assert tree.root.right is None


def test_optimal_bst_three_keys():
    tree = build_optimal_bst(3, [3, 10, 3])
    assert tree.root.key == 1
    assert tree.root.left.key == 0
    assert tree.root.right.key == 2


def test_splay_tree_rotate_right():
    tree = SplayTree()
    n50 = tree.insert(50)
    n30 = tree.insert(30)
    n20 = tree.insert(20)
    n40 = tree.insert(40)
    n35 = tree.insert(35)

    tree.rotate_right(n30)

    assert n30.parent is None
    assert n30.left == n20
    assert n20.parent == n30
    assert n30.right == n50
    assert n50.parent == n30
    assert n50.left == n40
    assert n40.parent == n50
    assert n40.left == n35
    assert n35.parent == n40


def test_splay_tree_rotate_left():
    tree = SplayTree()
    n30 = tree.insert(30)
    n50 = tree.insert(50)
    n40 = tree.insert(40)
    n35 = tree.insert(35)

    tree.rotate_left(n50)

    assert n50.parent is None
    assert n50.left == n30
    assert n30.parent == n50
    assert n30.right == n40
    assert n40.parent == n30
    assert n40.left == n35
    assert n35.parent == n40


def test_splay_tree_zig_and_zag():
    tree = SplayTree()
    n20 = tree.insert(20)
    n10 = tree.insert(10)
    tree.splay(n10)

    assert tree.root == n10
    assert n10.right == n20
    assert n20.parent == n10

    tree = SplayTree()
    n10 = tree.insert(10)
    n20 = tree.insert(20)
    tree.splay(n20)

    assert tree.root == n20
    assert n20.left == n10
    assert n10.parent == n20
