m = [['G', 'T', 'G', 'G', 'T', 'C', 'T', 'T', 'T', 'G'],
     ['C', 'T', 'T', 'A', 'C', 'T', 'T', 'T', 'A', 'G'],
     ['C', 'A', 'A', 'C', 'C', 'G', 'G', 'A', 'T', 'T'],
     ['C', 'C', 'C', 'G', 'T', 'G', 'A', 'T', 'T', 'A'],
     ['G', 'A', 'G', 'A', 'C', 'T', 'T', 'G', 'G', 'A'],
     ['G', 'G', 'C', 'C', 'A', 'A', 'T', 'G', 'T', 'T'],
     ['G', 'C', 'T', 'T', 'G', 'A', 'A', 'T', 'T', 'A'],
     ['C', 'C', 'A', 'T', 'A', 'A', 'A', 'C', 'A', 'T'],
     ['A', 'G', 'A', 'C', 'A', 'C', 'A', 'C', 'C', 'T'],
     ['T', 'C', 'G', 'A', 'C', 'A', 'G', 'T', 'T', 'A']]


# Find all neighbors of the current position
def getNeighbors(cur_row, cur_col, n_row, n_col) -> list:
    directions = [[cur_row, cur_col-1],
                  [cur_row, cur_col+1],
                  [cur_row-1, cur_col],
                  [cur_row+1, cur_col]]
    neighbors = []
    for row, col in directions:
        if 0 <= row < n_row and 0 <= col < n_col:
            neighbors.append([row, col])
    return neighbors


# Judge whether the current string is the final string
def isFinal(m: list, path: list, s: str) -> bool:
    cur_s = ''
    for i in path:
        row, col = i
        sub_s = m[row][col]
        cur_s += sub_s
    return cur_s == s


# 对所有第一个位置符合的点 作为start 进行DFS
# Path记录了当前走过的路径 count记录有多少路径是符合条件的
def dfs(m: list, s: str, start: list, path: list, count: int) -> int:
    n_row = len(m)
    n_col = len(m[0])
    if isFinal(m, path, s):
        count += 1
        return count

    for neighbor in getNeighbors(start[0], start[1], n_row, n_col):
        if neighbor not in path and m[neighbor[0]][neighbor[1]] == s[len(path)]:
            path.append(neighbor)
            count = dfs(m, s, neighbor, path, count)
            path.pop()
    return count


def findSeqOccurance(m: list, s: str) -> int:
    """
    @arg m: a matrix containing nucleotide characters
    @arg s: the sequence to be searched
    Exapmle:
        findSeqOccurance(m, "GTTCCA") # returns 7
        findSeqOccurance(m, "CATAGACA") # returns 2
        findSeqOccurance(m, "GTCAGATCA") # returns 9
    """
    count = 0
    for row in range(len(m)):
        for col in range(len(m[0])):
            if m[row][col] == s[0]:
                start = [row, col]
                count += dfs(m, s, start, [start], 0)
    return count


print(findSeqOccurance(m, "GTCAGATCA"))