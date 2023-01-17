exon = [[1, 5, 5],
        [2, 3, 3],
        [4, 8, 6],
        [6, 12, 10],
        [7, 17, 12],
        [9, 10, 1],
        [11, 15, 7],
        [13, 14, 0],
        [16, 18, 4]]


# 找到给定列表中最大节点值
def Find_Min_Max_Node(exon: list):
    nodes = set()
    for i in exon:
        for j in i[0:2]:
            nodes.add(j)
    return [min(nodes), max(nodes)]


def InitiateGraph(exon: list, graph: dict) -> dict:
    min_node = Find_Min_Max_Node(exon)[0]
    max_node = Find_Min_Max_Node(exon)[1]
    for i in range(min_node, max_node):
        graph[i] = {i+1: 0}
    return graph


def AddGraph(graph: dict, graph_line: tuple) -> dict:
    start, end, edge = graph_line
    if start not in graph:
        graph[start] = {end: edge}
    else:
        graph[start][end] = edge
    return graph


def ExonChaining(exon, graph):
    min_node = Find_Min_Max_Node(exon)[0]  # 1
    max_node = Find_Min_Max_Node(exon)[1]  # 18
    topo_sort = [i for i in range(min_node, max_node)]  # 1~17
    values = [float('-inf') for _ in range(min_node, max_node+1)]
    values[0] = 0
    # 建立回溯字典
    back_path = {min_node: None}
    # 正向寻找，遍历每一个node，将该node的所有子节点value更新
    for node in topo_sort:
        for i in graph[node]:
            new_value = values[node-1] + graph[node][i]
            if new_value > values[i-1]:
                values[i-1] = new_value
                back_path[i] = node
    # 回溯过程
    path = [max_node]  # 18
    cur_node = max_node
    while cur_node != min_node:
        cur_node = back_path[cur_node]
        path.insert(0, cur_node)
    return path


graph = {}
graph = InitiateGraph(exon, graph)
for i in exon:
    graph = AddGraph(graph, tuple(i))
print(ExonChaining(exon, graph))

