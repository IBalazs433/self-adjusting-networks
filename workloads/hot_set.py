import random

def generate_hotset_requests(n, m, hot_fraction, hot_probability, dim):
    """
    Generate requests where a small subset of nodes is used most often.

    Example:
        hot_fraction=0.1
        hot_probability=0.8

    => 10% of nodes are hot and 80% of requests are between hot nodes.
    """
    hot_size = max(1, int(n * hot_fraction))

    hot_nodes = random.sample(range(n), hot_size)
    all_nodes = list(range(n))

    requests = []
    
    if dim == 1:
        for _ in range(m):
            if random.random() < hot_probability:
                u = random.choice(hot_nodes)

            else:
                u = random.choice(all_nodes)

            requests.append(u)


    elif dim == 2:
        for _ in range(m):
            if random.random() < hot_probability:
                u = random.choice(hot_nodes)
                v = random.choice(hot_nodes)
                while v == u:
                    v = random.choice(hot_nodes)

            else:
                u = random.choice(all_nodes)
                v = random.choice(all_nodes)
                while v == u:
                    v = random.choice(all_nodes)

            requests.append([u, v])

    return requests