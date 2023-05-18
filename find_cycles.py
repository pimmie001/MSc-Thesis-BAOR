def makegraph(arcs, nodes):
    """creates a graph given the arcs and nodes"""
    graph = {}
    for node in nodes:
        graph[node] = []
    for arc in arcs:
        graph[arc[0]].append(arc[1])
    return graph


# TODO: CONFIRM preprocessing
# TODO: check efficiency? 
def find_cycles(arcs, nodes, K):
    """returns all cycles of size K or less"""

    graph = makegraph(arcs, nodes)

    cycles = set()
    cycles_sorted = set()
    for node in graph:
        visited = set([node])
        stack = [(node, [node])] # (current, path)
        while stack:
            (current, path) = stack.pop()
            if len(path) == K+1: # path too long
                continue
            else: # check for cycle
                if path[0] in graph[current]:
                    cycle = tuple(path)
                    cycle_sorted = tuple(sorted(path))
                    if cycle_sorted not in cycles_sorted:
                        cycles.add(cycle)
                        cycles_sorted.add(cycle_sorted)
            # continue path:
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))

    return [list(cycle) for cycle in cycles]



def find_cycles_K(arcs, nodes, K):
    """returns all cycles of size K"""

    graph = makegraph(arcs, nodes)

    cycles = set()
    cycles_sorted = set()
    for node in graph:
        visited = set([node])
        stack = [(node, [node])] # (current, path)
        while stack:
            (current, path) = stack.pop()
            if len(path) == K:
                if path[0] in graph[current]: # can complete cycle?
                    cycle = tuple(path)
                    cycle_sorted = tuple(sorted(path))
                    if cycle_sorted not in cycles_sorted:
                        cycles.add(cycle)
                        cycles_sorted.add(cycle_sorted)
            else:
                for neighbor in graph[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append((neighbor, path + [neighbor]))

    return [list(cycle) for cycle in cycles]



# TODO: test this function (example paper)
# TODO: Preprocessing to remove unneccesasary variables
def find_half_cycles(arcs, nodes, M):
    """find half cycles of size at most M"""

    graph = makegraph(arcs, nodes)

    cycles = set()
    cycles_sorted = set()
    for node in graph:
        visited = set([node])
        stack = [(node, [node])] # (current, path)
        while stack:
            (current, path) = stack.pop()
            if len(path) == M+1: # path too long
                continue
            else:
                if len(path) > 1: ######## TODO ????
                    cycle = tuple(path)
                    cycle_sorted = tuple(sorted(path))
                    if cycle_sorted not in cycles_sorted:
                        cycles.add(cycle)
                        cycles_sorted.add(cycle_sorted)
            # continue path:
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))

    return [list(cycle) for cycle in cycles]

