# findpath.py

import mountain
from queue import PriorityQueue

def createMemory(nrow, ncol):
    memory = []
    for i in range(nrow):
        memory.append([0] * ncol)
    return memory

def getMemory(memory, row, col):
    return memory[row][col]

def setMemory(memory, row, col):
    memory[row][col] = 1

def ManhattanDistance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


##  An example of greedy search only considering the distance to the goal:
# def greedy(mountain):
#     queue = PriorityQueue()
#     nrow, ncol = mountain.getDimensions()
#     cur_pos = mountain.getStart()
#     queue.put((0, (cur_pos, [])))
#     memory = createMemory(nrow, ncol)
#     setMemory(memory, cur_pos[0], cur_pos[1])
#     while len(queue.queue) > 0:
#         (move_pos, path) = queue.get()[1]
#         if mountain.isEnd(move_pos):
#             return path + [mountain.getEnd()]
#         neighbors = mountain.getNeighbors(move_pos)
#         for neighbor in neighbors:
#             if not getMemory(memory, neighbor[0], neighbor[1]):
#                 queue.put((ManhattanDistance(neighbor, mountain.getEnd()), (neighbor, path + [move_pos])))

##  An example of greedy search only considering the distance to the goal
# def greedy(mountain, heuristic = 1, future = 3):
#     nrow, ncol = mountain.getDimensions()
#     # memory用来记忆走过的路线，防止重复(走过的为0)
#     memory = createMemory(nrow, ncol)
#     mountain_queue = PriorityQueue()
#     start_position = mountain.getStart()
#     # 在队列中添加第一个元素
#     mountain_queue.put((0, start_position))
#     # 创建即将输出的path
#     path = []
#     while len(mountain_queue.queue) > 0:
#         cur_position = mountain_queue.get()[1]
#         setMemory(memory, cur_position[0], cur_position[1])
#         print(cur_position)
#         path.append(cur_position)
#         # 判断结束的语句
#         if mountain.isEnd(cur_position):
#             return path
#         neighboors = mountain.getNeighbors(cur_position)
#         for neighboor in neighboors:
#             if getMemory(memory, neighboor[0], neighboor[1]) == 0:
#                 cur_distance = ManhattanDistance(neighboor, mountain.getEnd())
#                 mountain_queue.put((cur_distance, neighboor))

## A-star algorithm
def greedy(mountain):
    # 定义队列，迄今为止的代价记录，parent信息。
    frontier = PriorityQueue()
    cost_so_far = {}
    parent = {}

    start_position = mountain.getStart()
    end_position = mountain.getEnd()
    frontier.put((0, start_position))
    parent[start_position] = None
    cost_so_far[start_position] = 0

    while len(frontier.queue) > 0:
        cur_position = frontier.get()[1]
        # 如果搜索到end了，就意味着一定有一条从start到end的通路
        if cur_position == end_position:
            break
        neighbors = mountain.getNeighbors(cur_position)
        for neighbor in neighbors:
            # neighbor的代价等于cur_position记录的代价加上cur到neighbor的代价
            new_cost = cost_so_far[cur_position] + mountain.timeBetween(cur_position, neighbor)
            # 两种情况：如果neighbor不在cost字典中，证明还没搜寻到这里。
            # 或者此时的neighbor代价比刚得到的要高（比如本题中一个1.5和三个0.5的代价不一样）
            if neighbor not in cost_so_far or cost_so_far[neighbor] > new_cost:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + ManhattanDistance(neighbor, end_position)
                frontier.put((priority, neighbor))
                parent[neighbor] = cur_position
    # 拿到了parent，接下来从end开始回溯到start
    path = [end_position]
    position = end_position
    while position != start_position:
        position = parent[position]
        path.insert(0, position)
    return path
