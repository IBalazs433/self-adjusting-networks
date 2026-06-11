import random

def generate_hotset_requests(n, m, hot_fraction, hot_probability, dim):
    """
    Generate requests with hot-set locality.

    A subset of nodes is designated as the hot set. With probability
    hot_probability, requests are generated from the hot set;
    otherwise they are generated from the entire node set.

    Args:
        n: Number of nodes.
        m: Number of requests to generate.
        hot_fraction: Fraction of nodes belonging to the hot set.
        hot_probability: Probability of generating a request involving
            hot-set nodes.
        dim: Request dimension.

            - 1: Generates single-node access requests.
            - 2: Generates communication requests represented as
            (sender, receiver) pairs.

    Returns:
        List of generated requests.

    Example:
        hot_fraction = 0.1
        hot_probability = 0.8

        => 10% of nodes belong to the hot set and 80% of requests
        are generated from hot-set nodes.
    """

    # Ensure that the hot set contains at least one node.
    hot_size = max(1, int(n * hot_fraction))

    hot_nodes = random.sample(range(n), hot_size)
    all_nodes = list(range(n))

    requests = []
    
    if dim == 1:
        for _ in range(m):
            if random.random() < hot_probability:
                node = random.choice(hot_nodes)
            else:
                node = random.choice(all_nodes)

            requests.append(node)


    elif dim == 2:
        for _ in range(m):
            if random.random() < hot_probability:
                sender = random.choice(hot_nodes)
                receiver = random.choice(hot_nodes)
                while receiver == sender:
                    receiver = random.choice(hot_nodes)

            else:
                sender = random.choice(all_nodes)
                receiver = random.choice(all_nodes)
                while receiver == sender:
                    receiver = random.choice(all_nodes)

            requests.append((sender, receiver))

    return requests