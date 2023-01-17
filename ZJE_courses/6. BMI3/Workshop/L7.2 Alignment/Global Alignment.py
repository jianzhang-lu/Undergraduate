def GlobalAlignment(s1, s2):
    # Indel: -1; Mismatch: -1; match: +1
    matrix = [[0 for _ in range(len(s1)+1)] for __ in range(len(s2)+1)]
    # 将矩阵中第一行和第一列填补上
    for i in range(len(matrix[0])):
        matrix[0][i] = -i
    for j in range(len(matrix)):
        matrix[j][0] = -j

    # 建立回溯字典
    back_dict = {(0, 0): None}

    # 开始dynamic programming
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if s1[i-1] == s2[j-1]:
                diag_weight = 1
            else:
                diag_weight = -1
            possible_values = [matrix[j-1][i]-1, matrix[j][i-1]-1, matrix[j-1][i-1]+diag_weight]
            matrix[j][i] = max(possible_values)
            max_index = possible_values.index(max(possible_values))
            # 分情况计入回溯结果
            if max_index == 0:
                max_pre_pos = tuple([j-1, i])
            elif max_index == 1:
                max_pre_pos = tuple([j, i-1])
            else:
                max_pre_pos = tuple([j-1, i-1])
            back_dict[(j, i)] = max_pre_pos

    # 回溯过程
    path = [(len(s2), len(s1))]
    cur_pos = (len(s2), len(s1))
    while cur_pos != (0, 0):
        cur_pos = back_dict[cur_pos]
        path.insert(0, cur_pos)

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

    return matrix[len(s2)][len(s1)]


str1 = 'GCCCAGTCTATGTCAGGGGGCACGAGCATGCACA'  # 34
str2 = 'GCCGCCGTCGTTTTCAGCAGTTATGTTCAGAT'  # 32
print(GlobalAlignment(str1, str2))
