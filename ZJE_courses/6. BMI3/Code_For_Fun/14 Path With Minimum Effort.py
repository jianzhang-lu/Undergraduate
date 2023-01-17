import collections

def minimumEffortPath(heights: list) -> int:
    m = len(heights)
    n = len(heights[0])
    q = collections.deque()
    q.append((0, 0))
    distances = [[float('inf')] * n for _ in range(m)]
    distances[0][0] = 0
    dirs = [[0, 1], [1, 0], [0, -1], [-1, 0]]

    while q:
        i, j = q.popleft()

        for d in dirs:
            x = i + d[0]
            y = j + d[1]

            if 0 <= x < m and 0 <= y < n and distances[x][y] > max(distances[i][j], abs(heights[x][y] - heights[i][j])):
                q.append((x, y))
                distances[x][y] = max(distances[i][j], abs(heights[x][y] - heights[i][j]))

    return distances[-1][-1] if distances[-1][-1] != float('inf') else -1


heights = [[1, 2, 3],
           [3, 8, 4],
           [5, 3, 5]]
print(minimumEffortPath(heights))
print(1<float('inf'))

