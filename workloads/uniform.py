import random


def generate_random_requests(n, m, dim):
    """
    Generate uniformly random requests.

    Args:
        n: Number of nodes.
        m: Number of requests to generate.
        dim: Request dimension.

            - 1: Generates single-node access requests.
            - 2: Generates communication requests represented as
            (sender, receiver) pairs.

    Returns:
        List of generated requests.
    """

    requests = []

    if dim == 1:
        for _ in range(m):
            requests.append(random.randrange(n))

    elif dim == 2:
        for _ in range(m):
            sender = random.randrange(n)
            receiver = random.randrange(n)
            while sender == receiver:
                receiver = random.randrange(n)
            requests.append((sender, receiver))

    return requests