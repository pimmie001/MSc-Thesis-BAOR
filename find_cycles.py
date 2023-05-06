def find_cycles(arcs, nodes, K):
    """returns all cycles of size k or less"""

    # given arcs, create a graph
    graph = {}
    for node in nodes:
        graph[node] = []
    for arc in arcs:
        graph[arc[0]].append(arc[1])


    cycles = set()
    for node in graph:
        visited = set([node])
        stack = [(node, [node])] # (current, path)
        while stack:
            (current, path) = stack.pop()
            if len(path) == K+1: # path too long
                continue
            else: # check for cycle
                if path[0] in graph[current]:
                    cycle = tuple(sorted(path)) ## TODO: this will mess up order of cycle (cycle might be 213 but will now become 123)
                    if cycle not in cycles:
                        cycles.add(cycle)
            # continue path:
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))


    return [list(cycle) for cycle in cycles]




def find_cycles_K(arcs, nodes, K):
    """Similiar to find_cycles function but will only return cycles of size K (not less than K)"""

    # given arcs, create a graph
    graph = {}
    for node in nodes:
        graph[node] = []
    for arc in arcs:
        graph[arc[0]].append(arc[1])


    cycles = set()
    for node in graph:
        visited = set([node])
        stack = [(node, [node])] # (current, path)
        while stack:
            (current, path) = stack.pop()
            if len(path) == K:
                if path[0] in graph[current]: # can complete cycle?
                    cycle = tuple(sorted(path))
                    if cycle not in cycles:
                        cycles.add(cycle)
            else:
                for neighbor in graph[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append((neighbor, path + [neighbor]))


    return [list(cycle) for cycle in cycles]

