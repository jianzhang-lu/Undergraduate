import sys

import networkx as nx
import pandas as pd
from queue import PriorityQueue

def dijkstra_traversal(g: nx.Graph, start: int = 0, end: int = -1):
    vertices_list = sorted(nx.nodes(g))
#   vertices_list: ['A', 'B', 'C', 'D', 'E']

    visit = [0] * len(vertices_list)
    dist_list = [float('inf')] * len(vertices_list)
    dist_list[start] = 0.0

    # previous vertex 结果
    pre_vertex = [-1] * len(vertices_list)

    queue = PriorityQueue()
    queue.put((0.0, start))
    while len(queue.queue) > 0:
        min_dist, cur_vertex = queue.get()
        visit[cur_vertex] = 1

        for nbr_vertex in nx.all_neighbors(g, cur_vertex):
            if not visit[nbr_vertex]:
                edge_weight = g[nbr_vertex][cur_vertex]['weight']
                # new_dist是vertex自身的weight加上edge的weight
                new_dist = edge_weight + dist_list[cur_vertex]
                if new_dist < dist_list[nbr_vertex]:
                    dist_list[nbr_vertex] = new_dist
                    pre_vertex[nbr_vertex] = cur_vertex
                    queue.put((round(new_dist, 1), nbr_vertex))
    res = []
    for i in range(len(vertices_list)):
        res.append((dist_list[i], pre_vertex[i]))
    return res


if __name__ == "__main__":
    g = nx.from_pandas_edgelist(
        pd.read_csv(sys.stdin),
        edge_attr=["weight"],
        create_using=nx.Graph(),
    )
    print(dijkstra_traversal(g, 0, -1))


# graph = {"22": {"23": 10, "15": 12, "12": 13},
#          "23": {"22": 10, "20": 15},
#          "15": {"20": 5, "22": 12, "12": 4, "19": 7, "11": 8},
#          "12": {"15": 4, "11": 7},
#          "20": {"23": 15, "21": 3, "15": 5, "19": 1},
#          "18": {"21": 2, "19": 3, "16": 4},
#          "21": {"18": 2, "20": 3},
#          "19": {"20": 1, "18": 3, "15": 7, "16": 4},
#          "16": {"18": 4, "19": 4, "11": 12, "4": 5},
#          "11": {"16": 12, "15": 8, "10": 8, "12": 7},
#          "4": {"16": 5, "10": 8, "2E": 3},
#          "10": {"4": 8, "2E": 5, "11": 8},
#          "2E": {"4": 3, "10": 5, "2A": 3},
#          "2A": {"2E": 3}}
