# mountain.py

"""
This file contains the Mountain class, which reads in a mountain file and creates
a representation of the mountain that is exposed through a simple interface.
"""
import re
import copy

class Mountain:
    # Initializes the Maze object by reading the maze from a file
    def __init__(self, filename):
        self.__filename = filename
        with open(filename) as f:
            lines = f.readlines()
        self.__Z = list(map(lambda y: list(map(float, y.strip().split(','))), lines))
        self.__shape = (len(self.__Z), len(self.__Z[0]))
        self.rows = len(self.__Z)
        self.cols = len(self.__Z[0])
        self.__start = (1,1)
        self.__stop = (len(self.__Z)-2, len(self.__Z[0])-2)

    def getStart(self):
        return self.__start 

    def getEnd(self):
        return self.__stop 

    def isEnd(self, pos):
        return pos == self.getEnd()

    def getDimensions(self):
        return self.__shape

    def verticalDistance(self, prev:tuple, next:tuple):
        return self.__Z[next[0]][next[1]] - self.__Z[prev[0]][prev[1]]

    def timeBetween(self, prev:tuple, next:tuple):
        vert = abs(self.verticalDistance(prev, next))
        return (vert ** 2 if vert > 1 else vert)

    def isValidMove(self, prev:tuple, next:tuple):
        row, col = next[0], next[1]
        if abs(next[0] - prev[0]) + abs(next[1] - prev[1]) > 1:
        	return False
        return row > 0 and row < self.rows -1 and col > 0 and col < self.cols -1

    def getNeighbors(self, prev:tuple):
        row, col = prev[0], prev[1]
        possibleNeighbors = [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1)
        ]
        neighbors = []
        for n in possibleNeighbors:
            if self.isValidMove(prev, n):
                neighbors.append(n)
        return neighbors        

    def isValidPath(self, path:list):
        for i in range(len(path)-1):
            if not self.isValidMove(path[i], path[i+1]):
                return False
        else:
            return True

    def calculatePath(self, path:list):
        if len(path) == 0:
            raise ValueError("No path found")
        if path[-1] != self.__stop:
            raise ValueError("The path does not reach the goal")
        result = len(path) * 0.1
        for i in range(len(path)-1):
            if not self.isValidMove(path[i], path[i+1]):
                raise ValueError("The path is not a valid solution")
            result += self.timeBetween(path[i], path[i+1])
        return result

    def plotContour(self, level=20, ax=None):
        import numpy as np
        import matplotlib.pyplot as plt
        lin_x = np.linspace(0,1,self.__shape[0],endpoint=False)
        lin_y = np.linspace(0,1,self.__shape[1],endpoint=False)
        flag = False
        if not ax:
            fig,ax= plt.subplots()
            flag = True
        ax.contour(lin_x, lin_y, np.array(self.__Z), level)
        ax.scatter(lin_x[self.__start[0]], lin_y[self.__start[1]],c="red",zorder=100)
        ax.scatter(lin_x[self.__stop[0]], lin_y[self.__stop[1]], c="blue",zorder=100)
        if flag:
            return fig, ax 
        else:
            return ax 


    def plot3D(self, ax=None):
        import numpy as np
        import matplotlib.pyplot as plt
        lin_x = np.linspace(0,1,self.__shape[0],endpoint=False)
        lin_y = np.linspace(0,1,self.__shape[1],endpoint=False)
        x,y = np.meshgrid(lin_x,lin_y)
        flag = False
        if not ax:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")
            flag = True
        ax.plot_surface(x,y,np.array(self.__Z),cmap='terrain')
        ax.scatter3D(lin_x[self.__start[0]], lin_y[self.__start[1]], self.__Z[self.__start[0]][self.__start[1]],c="red",zorder=100)
        ax.scatter3D(lin_x[self.__stop[0]], lin_y[self.__stop[1]], self.__Z[self.__stop[0]][self.__stop[1]],c="blue",zorder=100)
        ax.set_axis_off()
        if flag:
            return fig, ax 
        else:
            return ax 

    def plotPath(self, ax, path):
        import numpy as np
        import matplotlib.pyplot as plt
        lin_x = np.linspace(0,1,self.__shape[0],endpoint=False)
        lin_y = np.linspace(0,1,self.__shape[1],endpoint=False)
        xline = list(map(lambda x: lin_x[x[0]], path))
        yline = list(map(lambda x: lin_y[x[1]], path))
        ax.plot(xline, yline, c = 'red', zorder=100)

    def plot3DPath(self, ax, path):
        import numpy as np
        import matplotlib.pyplot as plt
        lin_x = np.linspace(0,1,self.__shape[0],endpoint=False)
        lin_y = np.linspace(0,1,self.__shape[1],endpoint=False)
        zline = np.array(list(map(lambda x: self.__Z[x[0]][x[1]], path)) )
        xline = list(map(lambda x: lin_x[x[0]], path))
        yline = list(map(lambda x: lin_y[x[1]], path))
        ax.scatter3D(xline, yline, zline, c='red',zorder=100)


