import random
def construct_de_bruijn_graph(text, k):
    graph = {}
    kmers = [text[pos:pos+k] for pos in range(len(text) - k + 1)]
    for kmer in kmers:
        prefix = kmer[:-1]
        suffix = kmer[1:]
        if prefix not in graph:
            graph[prefix] = [suffix]
        else:
            graph[prefix].append(suffix)
    return graph


def eulerian_cycle(graph):
    # 每次traverse后去掉当前的edge并且判断此时的to节点有无其他连接
    # 如果没有则意味着cycle又回到了起点
    def traverse(graph, from_node, to_node):
        graph[from_node].remove(to_node)
        if not graph[to_node]:
            return False
        return True
    current_node = random.choice(list(graph.keys()))
    cycle = [current_node]
    finished = False
    while not finished:
        # rearrange cycle before next cycle
        new_start_pos = cycle.index(current_node)
        cycle = cycle[new_start_pos:] + cycle[:new_start_pos]
        if len(cycle) > 1:
            cycle.append(current_node)
        while True:
            next_node = random.choice(graph[current_node])
            # traverse until end of one cycle
            if traverse(graph, current_node, next_node):
                cycle.append(next_node)
                current_node = next_node
            else:
                current_node = next_node
                break
        # test if unexplored edges after each cycle
        finished = True
        for node in graph:
            if graph[node]:
                finished = False
                current_node = random.choice([node for node in cycle if graph[node]])
    # add the last node, which is also the beginning node
    cycle.append(current_node)
    return cycle

