import random


def generate_random_requests(n, m, dim):
    """
    Generate a uniformly random communication requests over n nodes and m length.

    Parameters:
        n: Number of nodes.

        m: Number of requests.

        dim: dimension of array. 1 or 2
    """

    requests = []

    if dim == 1:
        for _ in range(m):
            u = random.randrange(n)
            requests.append(u)

    elif dim == 2:
        for _ in range(m):
            u = random.randrange(n)
            v = random.randrange(n)
            while u == v:
                v = random.randrange(n)
            requests.append([u, v])

    return requests