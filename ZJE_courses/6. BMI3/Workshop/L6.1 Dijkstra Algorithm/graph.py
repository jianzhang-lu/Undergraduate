# Vertex使用字典connectedTo来记录与其相连的顶点，以及每一条边的权重
class Vertex:
    # 初始化id(通常是一个字符串)，以及字典connectedTo
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}

    # addNeighbor方法添加一个顶点到另一个顶点的连接
    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    # getConnections方法返回邻接表中的所有顶点，由connectedTo来表示
    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    # 返回当前顶点到以参数传入的顶点之间的边的权重
    def getWeight(self, nbr):
        return self.connectedTo[nbr]

class Graph:
    def __init__(self):
        # verList: {'A': A(vertex), 'B': B(vertex)...}
        self.verList = {}
        self.numVertices = 0

    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.verList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.verList:
            return self.verList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.verList

    # f: from (vertex_id), t: to (vertex_id).
    def addEdge(self, f, t, cost=0):
        if f not in self.verList:
            nv = self.addVertex(f)
        if t not in self.verList:
            nv = self.addVertex(t)
        self.verList[f].addNeighbor(self.verList[t], cost)

    def getVertices(self):
        return self.verList.keys()

    # 重点：可以直接遍历图中所有顶点
    def __iter__(self):
        return iter(self.verList.values())
