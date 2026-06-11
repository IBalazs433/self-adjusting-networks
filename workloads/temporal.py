import random

def generate_temporal_requests(n, m, p_repeat, dim):
    """
    Generate requests with temporal locality.

    With probability p_repeat, the previously generated request is
    repeated. Otherwise, a new random request is generated.

    Args:
        n: Number of nodes.
        m: Number of requests to generate.
        p_repeat: Probability of repeating the previous request.
        dim: Request dimension.

            - 1: Generates single-node access requests.
            - 2: Generates communication requests represented as
            (sender, receiver) pairs.

    Returns:
        List of generated requests.
    """

    requests = []

    if m == 0:
        return requests

    if dim == 1:
        requests.append(random.randrange(n))

        for _ in range(1, m): 
            if random.random() < p_repeat:
                requests.append(requests[-1])
            else:
                requests.append(random.randrange(n))
        
    elif dim == 2:
        sender = random.randrange(n)
        receiver = random.randrange(n)
        while sender == receiver:
            receiver = random.randrange(n)
        requests.append((sender, receiver))

        for _ in range(1, m):
            if random.random() < p_repeat:
                requests.append(requests[-1])
            else:
                sender = random.randrange(n)
                receiver = random.randrange(n)
                while sender == receiver:
                    receiver = random.randrange(n)
                requests.append((sender, receiver))

    return requests