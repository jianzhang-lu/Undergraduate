import sys
import networkx as nx
import pandas as pd

def n_connected_components(g: nx.Graph):
    component = 0
    vertices_list = nx.nodes(g)
    visit = [0] * len(vertices_list)
    visit_dict = dict(zip(vertices_list, visit))
    for i in vertices_list:
        if not visit_dict[i]:
            dfs(g, i, visit_dict)
            component += 1
    return component


def dfs(g: nx.Graph, i, visit_dict: dict):
    visit_dict[i] = 1
    for nbr_vertex in nx.all_neighbors(g, i):
        if not visit_dict[nbr_vertex]:
            dfs(g, nbr_vertex, visit_dict)


if __name__ == "__main__":
    g = nx.from_pandas_edgelist(
        pd.read_csv(sys.stdin),
        create_using=nx.Graph()
    )
    print(n_connected_components(g))


## Method 2
# def connectedComponents(graph):
#     visited = []
#     components = []
#     for node in graph:
#         if node not in visited:
#             # dfs
#             component = [node]
#             stack = [node]
#             while stack:
#                 curr_node = stack.pop()
#                 visited.append(curr_node)
#                 neighbors = graph[curr_node]
#                 for neighbor in neighbors:
#                     if neighbor not in component and neighbor not in visited:
#                         component.append(neighbor)
#                         stack.append(neighbor)
#             components.append(component)
#     print(len(components))