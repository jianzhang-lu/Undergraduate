import numpy as np

def LocalAlignment(s1, s2):
    # Indel: -1; Mismatch: -1; match: +1
    matrix = [[0 for _ in range(len(s1)+1)] for __ in range(len(s2)+1)]

    # 建立回溯字典
    back_dict = {(0, 0): None}

    # 开始dynamic programming
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if s1[i-1] == s2[j-1]:
                diag_weight = 1
            else:
                diag_weight = -1
            possible_values = [matrix[j-1][i]-1, matrix[j][i-1]-1, matrix[j-1][i-1]+diag_weight, 0]
            matrix[j][i] = max(possible_values)
            max_index = possible_values.index(max(possible_values))
            # 分情况计入回溯结果
            if max_index == 0:
                max_pre_pos = tuple([j-1, i])
            elif max_index == 1:
                max_pre_pos = tuple([j, i-1])
            elif max_index == 2:
                max_pre_pos = tuple([j-1, i-1])
            else:
                max_pre_pos = None
            back_dict[(j, i)] = max_pre_pos

    # 回溯过程: 首先找到values中最大的数
    np_matrix = np.array(matrix)
    local_value = np_matrix.max()
    max_index = np.unravel_index(np_matrix.argmax(), np_matrix.shape)

    path = [max_index]
    cur_pos = max_index
    # 回溯到第一个0的下一位
    while matrix[cur_pos[0]][cur_pos[1]] > 0:
        cur_pos = back_dict[cur_pos]
        path.insert(0, cur_pos)
    print(path)

    # 根据回溯后的path输出比对后的两条序列
    path1 = [i[1] for i in path]  # 行
    path2 = [i[0] for i in path]  # 列

    # res1是行 res2是列
    res1, res2 = [], []
    for i in range(1, len(path1)):
        if path1[i] == path1[i-1]:
            res1.append('-')
        else:
            res1.append(s1[path1[i]-1])

    for i in range(1, len(path2)):
        if path2[i] == path2[i-1]:
            res2.append('-')
        else:
            res2.append(s2[path2[i]-1])
    print(''.join(res1))
    print(''.join(res2))

    return local_value


str1 = 'GCCCAGTCTATGTCAGGGGGCACGAGCATGCACA'  # 34
str2 = 'GCCGCCGTCGTTTTCAGCAGTTATGTTCAGAT'  # 32
print(LocalAlignment(str1, str2))

