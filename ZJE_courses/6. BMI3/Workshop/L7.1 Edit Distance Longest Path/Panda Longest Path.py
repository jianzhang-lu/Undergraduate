import pandas as pd
graph = pd.read_csv('GraphData.csv')

# source = 1, sink = 72
def LongestPath(source: int, sink: int, graph: pd.DataFrame):
    # 建立每个点的初始value (负无穷)
    values = [float('-inf')] * sink
    values[source-1] = 0

    # 建立回溯字典
    path_back = {source: None}
    for i in range(source+1, sink+1):
        # 找到此节点的所有子节点
        pre_nodes = list(graph.loc[graph['end'] == i, 'origin'])
        temp_values = []
        for pre_node in pre_nodes:
            # 找到pre节点到该节点的weight
            judge = (graph['end'] == i) & (graph['origin'] == pre_node)
            weight = int(graph.loc[judge, 'weight'])  # df格式转化成int
            temp_values.append(values[pre_node-1] + weight)
        # 将得到的最大值填入到values列表中
        values[i-1] = max(temp_values)
        # 通过temp_values中的最大值找到对应的父节点
        max_index = temp_values.index(values[i-1])
        path_back[i] = pre_nodes[max_index]
    print('The value of the longest path in this alignment graph is',
          values[sink-1])

    # 回溯过程
    path = [sink]
    position = sink  # 72
    while position != source:
        position = path_back[position]
        path.insert(0, position)
    print('The path is:', path)


LongestPath(1, 72, graph)




