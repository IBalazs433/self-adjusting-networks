import random

def generate_temporal_requests(n, m, p_repeat, dim):
    """
    Generate requests with temporal locality.

    With probability p_repeat, repeat the previous request.
    Otherwise generate a new random request.
    """

    requests = []

    if m == 0:
        return requests

    if dim == 1:
        requests.append(random.randrange(n))

        for _ in range(1, m):
            p = random.random()
            if p < p_repeat:
                requests.append(requests[-1])
            else:
                requests.append(random.randrange(n))
        
    if dim == 2:
        s = random.randrange(n)
        t = random.randrange(n)
        while s == t:
            t = random.randrange(n)
        requests.append([s, t])

        for _ in range(1, m):
            p = random.random()
            if p < p_repeat:
                requests.append(requests[-1])
            else:
                s = random.randrange(n)
                t = random.randrange(n)
                while s == t:
                    t = random.randrange(n)
                requests.append([s, t])

    return requests