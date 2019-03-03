
import math

class Vertex:
    def __init__(self, vert_id):
        self.vert_id = vert_id
        self.connectedTo={}
    
    def addNeighbor(self,vert_id,weight=0):
        self.connectedTo[vert_id]=weight
    
    def __str__(self):
        return str(self.vert_id)+' connectedTo: '+str([x for x in self.connectedTo.keys()])
 
    def getConnections(self):
        return self.connectedTo.keys()
 
    def getName(self):
        return self.vert_id
    
    def getWeight(self,vert_id):
        return self.connectedTo[vert_id]

class Graph:
    def __init__(self):
        self.vertList={}
        self.numVertices=0
 
    def addVertex(self,vert_id):
        self.numVertices=self.numVertices+1
        newVertex=Vertex(vert_id)
        self.vertList[vert_id]=newVertex
 
    def getVertex(self, vert_id):
        if vert_id in self.vertList:
            return self.vertList[vert_id]
        else:
            return None
 
    def __contains__(self, n):
        return n in self.vertList
 
    def addEdge(self, vert_id, overt_id, cost=0):
        if vert_id in self.vertList and overt_id in self.vertList:
            self.vertList[vert_id].addNeighbor(overt_id,cost)
            self.vertList[overt_id].addNeighbor(vert_id,cost)
 
    def getVertices(self):
        return self.vertList.keys()
 
    def __iter__(self):
        return iter(self.vertList.values())


def build_from_file(filevert_id='input.txt'):
    g = Graph()
    points = {}
    edge_datas = []
    with open(filevert_id,'r') as f:
        vertices,edges = [int(d) for d in f.readline().strip().split(' ')]
        f.readline()
        for i in range(vertices):
            line = f.readline().strip().split(' ')
            line = [d for d in line if d.strip()]
            points[int(line[0])] = (int(line[1]), int(line[-1]))
        f.readline()
        for i in range(edges):
            line = f.readline().strip().split(' ')
            edge_datas.append((int(line[0]), int(line[-1])))
        f.readline()
        line = f.readline().strip().split(' ')
        info = (int(line[0]), int(line[-1]))
    dist = lambda x,y,m,n:math.sqrt((x - m) ** 2 + (y - n) ** 2)
    for vert_id in points.keys():
        g.addVertex(vert_id)
    for vert,overt in edge_datas:
        g.addEdge(vert, overt, dist(points[vert][0], points[vert][1],
                        points[overt][0], points[overt][1]))
    return g, info


if __name__ == '__main__':
    
    g, info = build_from_file()

    for v in g:
        print(v)