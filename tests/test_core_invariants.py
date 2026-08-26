import random
from pathlib import Path

import numpy as np

from trees.bst import BinarySearchTree
from trees.splay_tree import SplayTree
from workloads.hot_set import generate_hotset_requests
from workloads.temporal import generate_temporal_requests
from workloads.uniform import generate_random_requests


def _inorder_keys(node, acc=None):
    if node is None:
        return acc if acc is not None else []

    if acc is None:
        acc = []
    _inorder_keys(node.left, acc)
    acc.append(node.key)
    _inorder_keys(node.right, acc)
    return acc


def test_bst_search_and_cost_tracking():
    tree = BinarySearchTree()
    for key in [5, 3, 8, 2, 4, 7, 9]:
        tree.insert(key)

    assert tree.search(4).key == 4
    assert tree.search_cost >= 3
    assert _inorder_keys(tree.root) == [2, 3, 4, 5, 7, 8, 9]


def test_splay_tree_keeps_bst_order_after_searches():
    tree = SplayTree()
    for key in [5, 3, 8, 2, 4, 7, 9]:
        tree.insert(key)

    for key in [4, 2, 8, 7]:
        tree.search(key)

    keys = _inorder_keys(tree.root)
    assert keys == sorted(keys)
    assert tree.search_cost > 0
    assert tree.rotations >= 0


def test_uniform_requests_are_reproducible_with_seed():
    random.seed(42)
    first = generate_random_requests(10, 100, 1)
    random.seed(42)
    second = generate_random_requests(10, 100, 1)
    assert first == second


def test_temporal_requests_repeat_previous_item():
    requests = generate_temporal_requests(5, 20, p_repeat=1.0, dim=1)
    assert len(requests) == 20
    assert all(request == requests[0] for request in requests[1:])


def test_hotset_requests_do_not_generate_self_pair_for_dim_2():
    requests = generate_hotset_requests(10, 200, hot_fraction=0.5, hot_probability=1.0, dim=2)
    assert all(sender != receiver for sender, receiver in requests)
