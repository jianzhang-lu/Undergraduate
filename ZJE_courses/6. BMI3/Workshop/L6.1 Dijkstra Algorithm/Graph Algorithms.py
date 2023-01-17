from queue import PriorityQueue
import graph
import pandas as pd

# Dijkstra’s algorithm
## 建立undirected graph
graph1 = graph.Graph()
graph1.addEdge('A', 'B', 6)
graph1.addEdge('B', 'A', 6)
graph1.addEdge('A', 'D', 1)
graph1.addEdge('D', 'A', 1)
graph1.addEdge('B', 'D', 2)
graph1.addEdge('D', 'B', 2)
graph1.addEdge('B', 'E', 2)
graph1.addEdge('E', 'B', 2)
graph1.addEdge('B', 'C', 5)
graph1.addEdge('C', 'B', 5)
graph1.addEdge('D', 'E', 1)
graph1.addEdge('E', 'D', 1)
graph1.addEdge('E', 'C', 5)
graph1.addEdge('C', 'E', 5)
for i in graph1:
    print(i)

# def dijkstra(graph, n_vertices, start):
#     # vertices_list: ['A', 'B', 'C', 'D', 'E']
#     vertices_list = list(graph.getVertices())
#     # 0: not visited, 1: visited
#     visit = [0] * n_vertices
#     visit_dict = dict(zip(vertices_list, visit))
#
#     # dist_list_result (距离的结果)
#     dist_list = [float('inf')] * n_vertices
#     dist_list[vertices_list.index(start)] = 0
#     dist_result = dict(zip(vertices_list, dist_list))
#
#     # previous vertex 结果
#     pre_vertex = [None] * n_vertices
#     pre_result = dict(zip(vertices_list, pre_vertex))
#
#     queue = PriorityQueue()
#     queue.put((0, start))
#     while len(queue.queue) > 0:
#         # cur_vertex_id = 'A' or 'B' or 'C'...
#         min_dist, cur_vertex_id = queue.get()
#         visit_dict[cur_vertex_id] = 1
#
#         vertex = graph.verList[cur_vertex_id]
#         for nbr_vertex in vertex.getConnections():
#             if not visit_dict[nbr_vertex.id]:
#                 weight = vertex.getWeight(nbr_vertex)
#                 # new_dist是vertex自身的weight加上edge的weight
#                 new_dist = weight + dist_result[vertex.id]
#                 if new_dist < dist_result[nbr_vertex.id]:
#                     dist_result[nbr_vertex.id] = new_dist
#                     pre_result[nbr_vertex.id] = vertex.id
#                     queue.put((new_dist, nbr_vertex.id))
#     # 建立表格
#     pd_vertex = list(dist_result.keys())
#     pd_dist = list(dist_result.values())
#     pd_pre = list(pre_result.values())
#     result = {'Vertex': pd_vertex,
#               'Dist': pd_dist,
#               'Previous': pd_pre}
#     result = pd.DataFrame(result)
#     return result
#
#
# print(dijkstra(graph1, graph1.numVertices, 'A'))
#
# # Return how many connected components are in a given graph.
# # 并且返回分组情况
# ## 建立disconnected graph.
# graph2 = graph.Graph()
# graph2.addEdge('C', 'Q', 1)
# graph2.addEdge('A', 'B', 1)
# graph2.addEdge('B', 'J', 1)
# graph2.addEdge('J', 'A', 1)
# graph2.addEdge('J', 'E', 1)
# graph2.addEdge('E', 'F', 1)
# graph2.addEdge('F', 'G', 1)
# graph2.addEdge('F', 'I', 1)
# graph2.addEdge('I', 'J', 1)
# graph2.addEdge('I', 'D', 1)
# graph2.addEdge('D', 'H', 1)
# graph2.addEdge('H', 'I', 1)
#
# # group代表分组信息的字典, group_info表示目前的组(从1开始计数)
# # 一次dfs可以找到一条完整通路。
# def dfs(graph, visit_dict, start, group, group_info):
#     visit_dict[start] = 1
#     group[start] = group_info
#     vertex = graph.verList[start]
#     # 如果此时的vertex没有neighbor了，循环不会进行，大dfs结束(此时一条通路已找到)
#     for nbr_vertex in vertex.getConnections():
#         if not visit_dict[nbr_vertex.id]:
#             dfs(graph, visit_dict, nbr_vertex.id, group, group_info)
#
# def findComponents(graph, n_vertices):
#     group_info = 1
#     vertices_list = list(graph.getVertices())
#     component_group = [None] * n_vertices
#     component_result = dict(zip(vertices_list, component_group))
#     visit = [0] * n_vertices
#     visit_dict = dict(zip(vertices_list, visit))
#
#     for i in vertices_list:
#         if not visit_dict[i]:
#             dfs(graph, visit_dict, i, component_result, group_info)
#             # 找到一条通路，分组信息加1，开始其他通路寻找。
#             group_info += 1
#     # 处理分组信息
#     final_result = {}
#     for i in component_result.values():
#         if i not in final_result:
#             final_result[i] = 1
#         else:
#             final_result[i] += 1
#     return final_result
#
#
# print(findComponents(graph2, graph2.numVertices))