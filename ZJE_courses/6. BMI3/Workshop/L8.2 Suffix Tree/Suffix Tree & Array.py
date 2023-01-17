def SuffixTree(string):
    new_string = string + '$'
    suffices = []
    for i in range(len(new_string)):
        suffices.append(new_string[i:])
    # 根节点设成0, 字典形式: {0:{1: T, 2: C, 3: G, 4: A}}
    tree = {0: {}}
    # 添加节点，新的节点从1开始命名
    new_node = 1
    for suffix in suffices:
        # 每次重新遍历一个suffix都要从0开始
        current_node = 0
        for base in suffix:
            current_edges = tree[current_node]
            if base not in list(current_edges.values()):
                # 此时需要建立新的node
                tree[current_node][new_node] = base
                tree[new_node] = {}
                current_node = new_node
                new_node += 1
            else:
                for key in current_edges:
                    if current_edges[key] == base:
                        current_node = key
    return tree


# 类似BFS算法
# 指定root，从root的所有子节点出发压缩suffix tree。对于每个节点来说，压缩到第一次遇到分叉就停止
# 返回所有遇到分叉前的节点 (如果root = 0 返回[3, 11, 18])
# 在这些节点之上的所有节点已经压缩完毕
def SuffixArrayHelper(suffixtree, root):
    res_root = []
    subnodes = suffixtree[root]  # {1: 'C', 10: 'A', 18: 'G', 25: 'T', 38: '$'}
    for node in list(subnodes.keys()):  # [1, 10, 18, 25, 38]
        combine = suffixtree[root][node]  # combine = 'C'
        # 移除节点
        suffixtree[root].pop(node)
        cur_node = node  # cur_node = 1
        while len(suffixtree[cur_node]) == 1:
            next = suffixtree[cur_node]  # next = {2: 'A'}, next = {3: 'G'}
            suffixtree.pop(cur_node)
            combine += list(next.values())[0]  # combine = CA, combine = CAG
            cur_node = list(next.keys())[0]  # cur_node = 2, cur_node = 3
        # 压缩suffix tree 添加节点
        suffixtree[root][cur_node] = combine

        # 如果此时的节点有子节点 意味着还有分叉 需要返回该节点
        # 如果没有节点 则意味着这条路已经全部压缩完毕
        if len(suffixtree[cur_node]) != 0:
            res_root.append(cur_node)
    return suffixtree, res_root


def SuffixArray(suffixtree: dict):
    suffixtree, roots = SuffixArrayHelper(suffixtree, 0)  # [3, 11, 18]
    while len(roots) > 0:
        root = roots.pop(0)
        suffixtree, temp_roots = SuffixArrayHelper(suffixtree, root)
        roots += temp_roots
    return suffixtree


# 输出suffix array所有的边
def OutputSuffixArray(suffixArray: dict) -> list:
    res = []
    for node in suffixArray:
        for subnode in suffixArray[node]:
            res.append(suffixArray[node][subnode])
    return sorted(res)


tree = SuffixTree('CAGTCAGG')
print(tree)
print()

array = SuffixArray(tree)
print(array)
print()

print(OutputSuffixArray(array))


# DFS算法
def merge_leaf(old_tree):
    # new_tree = {0:{}}
    res = []
    # new_next_node_to_add = None
    stack = [0]
    prev_edges = {i:'' for i in range(len(old_tree))}
    while stack:
        curr_node = stack.pop()
        children = list(old_tree[curr_node].keys())
        if len(children) > 1:
            new_next_node_to_add = curr_node
        for child in children:
            stack.append(child)
            if not old_tree[child] or len(old_tree[child]) > 1:  # test if we should end the edge
                res.append(prev_edges[curr_node] + old_tree[curr_node][child])
                # new_tree[new_next_node_to_add][child] = prev_edges[curr_node] + old_tree[curr_node][child]
            else:  # if we in middle of edge
                prev_edges[child] = prev_edges[curr_node] + old_tree[curr_node][child]
    print(prev_edges)
    return res


# print(merge_leaf(tree))