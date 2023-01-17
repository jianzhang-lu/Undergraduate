import re
import copy
from collections import deque
import json
from random import shuffle, seed
import time
import sys
from copy import deepcopy
from queue import PriorityQueue


sys.setrecursionlimit(0x100000)

class Maze:
    # Initializes the Maze object by reading the maze from a string
    def __init__(self, lines):
        self.__wallChar = '%'
        self.__startChar = 'P'
        self.__objectiveChar = '.'
        self.start = None
        self.objective = None
        # lines = list(filter(lambda x: not re.match(r'^\s*$', x), lines))
        lines = [list(line.strip('\n')) for line in lines]

        self.rows = len(lines)
        self.cols = len(lines[0])
        self.mazeRaw = lines

        if (len(self.mazeRaw) != self.rows) or (len(self.mazeRaw[0]) != self.cols):
            print("Maze dimensions incorrect")
            raise SystemExit
            return

        for row in range(len(self.mazeRaw)):
            for col in range(len(self.mazeRaw[0])):
                if self.mazeRaw[row][col] == self.__startChar:
                    self.start = (row, col)
                elif self.mazeRaw[row][col] == self.__objectiveChar:
                    self.objective = (row, col)

    # Returns True if the given position is the location of a wall
    def isWall(self, row, col):
        return self.mazeRaw[row][col] == self.__wallChar

    # Returns True if the given position is the location of an objective
    def isObjective(self, row, col):
        return (row, col) == self.objective

    # Returns the start position as a tuple of (row, column)
    def getStart(self):
        return self.start

    def setStart(self, start):
        self.start = start

    # Returns the dimensions of the maze as a (row, column) tuple
    def getDimensions(self):
        return (self.rows, self.cols)

    # Returns the list of objective positions of the maze
    def getObjectives(self):
        return copy.deepcopy(self.objective)

    def setObjectives(self, objectives):
        self.objective = objectives

    # Check if the agent can move into a specific row and column
    def isValidMove(self, row, col):
        return row >= 0 and row < self.rows and col >= 0 and col < self.cols and not self.isWall(row, col)

    # Returns list of neighboing squares that can be moved to from the given row,col
    def getNeighbors(self, row, col):
        possibleNeighbors = [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1)
        ]
        neighbors = []
        for r, c in possibleNeighbors:
            if self.isValidMove(r, c):
                neighbors.append((r, c))
        return neighbors


lines = []
while 1:
    line = input()
    if line == '':
        break
    lines.append(line)

maze = Maze(lines)
def ManhattanDistance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def GreedyMaze(maze: Maze):
    queue = PriorityQueue()
    end_pos = maze.getObjectives()
    cur_pos = maze.getStart()
    queue.put((ManhattanDistance(cur_pos, end_pos), cur_pos))
    # 建立回溯字典
    parent = {cur_pos: None}

    # 防止重走
    visit = set()
    while len(queue.queue) > 0:
        cur_pos = queue.get()[1]
        visit.add(cur_pos)
        if maze.isObjective(cur_pos[0], cur_pos[1]):
            break
        else:
            for neighbor in maze.getNeighbors(cur_pos[0], cur_pos[1]):
                if neighbor not in visit:
                    queue.put((ManhattanDistance(neighbor, end_pos), neighbor))
                    parent[neighbor] = cur_pos
                    visit.add(neighbor)
    return parent


# 回溯过程
parent = GreedyMaze(maze)

path = [maze.getObjectives()]
position = maze.getObjectives()

while position != maze.getStart():
    position = parent[position]
    path.insert(0, position)

path1 = []
for i in path:
    path1.append(list(i))
res = {'steps': len(path1)-1,
       'path': path1[1:]}
print(json.dumps(res))


# lines = []
# while 1:
#     try:
#         line = input()
#     except EOFError:
#         break
#     lines.append(line)


