
def compute_ranks(graph: dict) -> dict:
    DAMPING_FACTOR: float = 0.8
    RANK_ACCURACY: int = 10

    ranks: dict = {}
    total_pages_number: int = len(graph)

    for page in graph:
        # initializes ranks
        ranks[page] = 1.0 / total_pages_number

    for _ in range(RANK_ACCURACY):
        new_ranks: dict = {}
        for page in graph:
            new_rank: float = (1 - DAMPING_FACTOR) / total_pages_number

            for node in graph:
                # this loop looks for a page in all the graph's nodes
                # each time it finds the page in a node, means its refered to
                # so we increase its popularity record
                if page in graph[node]:
                    # pages current popularity / all links on the page
                    # which means if the page has a lot of links, decreases popularity
                    # https://classroom.udacity.com/courses/cs101/lessons/48756019/concepts/484202570923
                    new_rank += DAMPING_FACTOR * (ranks[node] /len(graph[node]))

            new_ranks[page] = new_rank

        ranks =  new_ranks
    return ranks