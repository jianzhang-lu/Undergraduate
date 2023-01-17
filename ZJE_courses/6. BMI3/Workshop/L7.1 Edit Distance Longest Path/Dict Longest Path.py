def AddGraph(graph: dict, graph_line: tuple) -> dict:
    start, end, edge = graph_line
    if start not in graph:
        graph[start] = {end: edge}
    else:
        graph[start][end] = edge
    return graph


def FindAllNodes(graph: dict) -> set:
    # 找到在图中所有的nodes
    all_nodes = set()
    for i in graph:
        all_nodes.add(i)
        for j in graph[i]:
            all_nodes.add(j)
    return all_nodes


def FindIndegreeZero(graph: dict):
    all_nodes = FindAllNodes(graph)
    candidates = []

    # 找到indegree == 0的所有节点
    for cur_node in all_nodes:
        zeroin = True
        for search_node in graph.values():
            if cur_node in search_node:
                zeroin = False
                break
        if zeroin:
            candidates.append(cur_node)
    return candidates


def FindOutdegreeZero(graph: dict):
    all_nodes = FindAllNodes(graph)
    candidates = []

    # 找到outdegree == 0的所有节点
    for cur_node in all_nodes:
        if cur_node not in graph:
            candidates.append(cur_node)
    return candidates


def TopologicalOrdering(graph: dict):
    in_candidates = FindIndegreeZero(graph)
    out_candidates = FindOutdegreeZero(graph)
    res = []
    while len(in_candidates) > 0:
        cur_candidate = in_candidates.pop(0)
        res.append(cur_candidate)
        graph.pop(cur_candidate)
        for i in FindIndegreeZero(graph):
            if i not in in_candidates:
                in_candidates.append(i)
    # 最后再加上outdegree == 0的所有点，这些点一定在拓扑排序的最后。
    res += out_candidates
    if len(graph) != 0:
        return 'No topological ordering'
    else:
        return res


def LongestPath(graph: dict):
    graph1 = graph.copy()
    topo_sort = TopologicalOrdering(graph1)
    values = {topo_sort[0]: 0}
    back_path = {topo_sort[0]: None}
    # 按照拓扑排序依次取出该点的父节点
    for cur_node in topo_sort[1:]:
        for pre_node in graph:
            if cur_node in graph[pre_node]:
                # value的值是父节点储存的再加上两点之间的weight
                cur_value = values[pre_node] + graph[pre_node][cur_node]
                # 如果cur_node不在values字典中或者cur_value比之前存储的大，则添加或替换
                if cur_node not in values or values[cur_node] < cur_value:
                    values[cur_node] = cur_value
                    back_path[cur_node] = pre_node
    final_node = FindOutdegreeZero(graph)[0]
    start_node = FindIndegreeZero(graph)[0]
    max_value = values[final_node]
    print('The value of longest path is', max_value)
    # 从最大点回溯过程
    path = [final_node]
    position = final_node
    while position != start_node:
        position = back_path[position]
        path.insert(0, position)
    print('The path is:', path)


data = open('GraphData.csv', 'r')
graph = {}
title = data.readline()
for i in data:
    graph_line = tuple(map(int, i.strip().split(',')))
    graph = AddGraph(graph, graph_line)


graph1 = graph.copy()
print(TopologicalOrdering(graph1))
LongestPath(graph)


# while 1:
#     try:
#         line = input()
#     except EOFError:
#         break
#     lines.append(line)