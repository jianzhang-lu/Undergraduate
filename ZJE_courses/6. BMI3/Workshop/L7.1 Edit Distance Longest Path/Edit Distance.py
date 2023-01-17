def EditDistance(s1: str, s2: str) -> int:
    matrix = [[0 for _ in range(len(s1)+1)] for __ in range(len(s2)+1)]
    # 将矩阵中第一行和第一列填补上
    for i in range(len(matrix[0])):
        matrix[0][i] = i
    for j in range(len(matrix)):
        matrix[j][0] = j

    # 开始dynamic programming
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if s1[i-1] == s2[j-1]:
                diag_weight = 0
            else:
                diag_weight = 1
            matrix[j][i] = min(matrix[j-1][i]+1, matrix[j][i-1]+1, matrix[j-1][i-1]+diag_weight)
    return matrix[len(s2)][len(s1)]


print(EditDistance('CTCATGTACCATAAT', 'ACTTATACGATAATC'))


