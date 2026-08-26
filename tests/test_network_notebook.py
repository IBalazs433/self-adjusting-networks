import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from networks.bst_network import BinarySearchTreeNetwork
from networks.optimal_network import build_optimal_bst_network
from networks.splaynet import SplayNet


def test_bst_network_empty():
    network = BinarySearchTreeNetwork()
    assert network.root is None
    assert network.total_communication_cost == 0


def test_bst_network_insert_root_and_structure():
    network = BinarySearchTreeNetwork()
    node = network.insert(8)
    assert network.root == node
    assert node.key == 8
    assert node.parent is None

    for key in [4, 12, 2, 6, 10, 14]:
        network.insert(key)

    assert network.root.key == 8
    assert network.root.left.key == 4
    assert network.root.right.key == 12
    assert network.root.left.left.key == 2
    assert network.root.left.right.key == 6
    assert network.root.right.left.key == 10
    assert network.root.right.right.key == 14


def test_bst_network_search_and_lca():
    network = BinarySearchTreeNetwork()
    for key in [8, 4, 12, 2, 6, 10, 14]:
        network.insert(key)

    node, depth = network.search(10)
    assert node.key == 10
    assert depth == 2

    node, depth = network.search(2)
    assert node.key == 2
    assert depth == 2

    node, depth = network.search(99)
    assert node is None

    lca, depth = network.least_common_ancestor(2, 6)
    assert lca.key == 4
    assert depth == 1

    lca, depth = network.least_common_ancestor(2, 14)
    assert lca.key == 8
    assert depth == 0

    lca, depth = network.least_common_ancestor(4, 6)
    assert lca.key == 4
    assert depth == 1


def test_bst_network_requests_add_communication_cost():
    network = BinarySearchTreeNetwork()
    for key in [8, 4, 12, 2, 6, 10, 14]:
        network.insert(key)

    sender, receiver, lca = network.request(2, 6)
    assert sender.key == 2
    assert receiver.key == 6
    assert lca.key == 4
    assert network.total_communication_cost == 2

    network.request(2, 14)
    network.request(10, 14)
    assert network.total_communication_cost == 8


def test_optimal_network_single_node():
    matrix = [[0]]
    net = build_optimal_bst_network(matrix)

    assert net.root.key == 0
    assert net.root.left is None
    assert net.root.right is None
    assert net.root.parent is None


def test_optimal_network_two_nodes():
    matrix = [
        [0, 10],
        [10, 0],
    ]
    net = build_optimal_bst_network(matrix)
    assert net.root.key in [0, 1]


def test_optimal_network_three_keys_uniform_case():
    matrix = [
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
    ]
    net = build_optimal_bst_network(matrix)
    assert net.root.key == 1


def test_splaynet_insert_and_search():
    net = SplayNet()
    for key in [10, 5, 15, 3, 7, 12, 20]:
        net.insert(key)

    assert net.root.key == 10
    assert net.root.left.key == 5
    assert net.root.right.key == 15
    assert net.root.left.left.key == 3
    assert net.root.left.right.key == 7
    assert net.root.right.left.key == 12
    assert net.root.right.right.key == 20

    assert net.search(10).key == 10
    assert net.search(5).key == 5
    assert net.search(7).key == 7
    assert net.search(999) is None


def test_splaynet_lca_and_rotations():
    net = SplayNet()
    for key in [10, 5, 15, 3, 7, 12, 20]:
        net.insert(key)

    lca = net.least_common_ancestor(3, 7)
    assert lca.key == 5

    lca = net.least_common_ancestor(3, 20)
    assert lca.key == 10

    lca = net.least_common_ancestor(12, 20)
    assert lca.key == 15

    lca = net.least_common_ancestor(12, 15)
    assert lca.key == 15

    net = SplayNet()
    for key in [10, 5, 3]:
        net.insert(key)
    node = net.search(5)
    net.rotate_right(node)

    assert net.root.key == 5
    assert net.root.left.key == 3
    assert net.root.right.key == 10
    assert net.root.left.parent is net.root
    assert net.root.right.parent is net.root

    net = SplayNet()
    for key in [10, 15, 20]:
        net.insert(key)
    node = net.search(15)
    net.rotate_left(node)

    assert net.root.key == 15
    assert net.root.left.key == 10
    assert net.root.right.key == 20
    assert net.root.left.parent is net.root
    assert net.root.right.parent is net.root


def test_splaynet_request_lca_is_root_and_rotation_counter():
    net = SplayNet()
    for key in [10, 5, 15, 3, 20]:
        net.insert(key)

    assert net.total_communication_cost == 0
    assert net.rotations == 0

    net.request(3, 20)
    assert net.rotations == 5
    assert net.total_communication_cost == 1

    net = SplayNet()
    for key in [20, 10, 5, 3, 7]:
        net.insert(key)

    net.request(3, 7)
    assert net.rotations == 2
    assert net.total_communication_cost == 1

    for _ in range(9):
        net.request(3, 7)
    assert net.rotations == 2
    assert net.total_communication_cost == 10
