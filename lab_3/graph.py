import random
class Graph(object):
    def __init__(self, n):
        self.matrix = []
        for i in range(n): 
            self.matrix.append([0 for i in range(n)])
        self.size = n
        self.edges = []
        for i in range(1, n+1): 
            self.edges.append(i)
class Undirected_graph(object):
    def __init__(self, n, vertices:list):
        A = Graph(n)
        self.matrix = A.matrix
        self.size = A.size
        self.edges = A.edges
        for i in range(self.size):
            for j in range(self.size):
                if (vertices[i][j] != 0)&(vertices[i][j] != 1):
                    raise Exception("Adjacency matrix can only contain ones and zeroes")
        for i in range(self.size):
            for j in range(self.size):
                A.matrix[i][j] = vertices[i][j]
    def add_edge(self, edge):
        self.edges.append(edge)
        for i in range(self.size):
            self.matrix[i].append(0)
        self.size+=1
        self.matrix.append([0]*self.size)
    def delete_edge(self, edge):
        if (edge > max(self.edges)) or (edge < min(self.edges)):
            raise Exception("This edge is not in the graph.")
        else:
            if edge in self.edges:
                ind = self.edges.index(edge)
                self.edges.remove(edge)
                for i in range(self.size):
                    self.matrix[i].remove(self.matrix[i][ind])
                del(self.matrix[ind])
                self.size-=1
            else:
                raise Exception("This edge is not in the graph.")
    def add_vertice(self, edge1, edge2):
        if (edge1 > max(self.edges)) or (edge1 < min(self.edges)) or (edge2 > max(self.edges)) or (edge2 < min(self.edges)):
            raise Exception("At least one of the edges is not in the graph.")
        else:
            if (edge1 in self.edges)&(edge2 in self.edges):
                self.matrix[edge1-1][edge2-1] = 1
                self.matrix[edge2-1][edge1-1] = 1
            else:
                raise Exception("At least one of the edges is not in the graph.")
    def delete_vertice(self, edge1, edge2):
        if (edge1 > max(self.edges)) or (edge1 < min(self.edges)) or (edge2 > max(self.edges)) or (edge2 < min(self.edges)):
            raise Exception("At least one of the edges is not in the graph.")
        else:
            if (edge1 in self.edges)&(edge2 in self.edges):
                self.matrix[edge1-1][edge2-1] = 0
                self.matrix[edge2-1][edge1-1] = 0
            else:
                raise Exception("At least one of the edges is not in the graph.")
class Undirected_weighted_graph(object):
    def __init__(self, n, vertices:list, weights:list):
        A = Undirected_graph(n, vertices)
        self.matrix = A.matrix
        self.size = A.size
        self.edges = A.edges
        self.weights = weights
        for i in range(self.size):
            for j in range(self.size):
                if (self.matrix[i][j] == 1)&(self.weights[i][j] == float('inf')):
                    raise Exception("Each vertece has to have a weight, that can not be -1. Please, choose a different value.")
                elif (self.matrix[i][j] == 0)&(self.weights[i][j] != float('inf')):
                    raise Exception("This vertece does not exist but has a weight. Please, change the weight value to -1.")
    def add_edge(self, edge):
        self.edges.append(edge)
        for i in range(self.size):
            self.matrix[i].append(0)
            self.weights[i].append(float('inf'))
        self.size+=1
        self.matrix.append([0]*self.size)
        self.weights.append([float('inf')]*self.size)
    def delete_edge(self, edge):
        if (edge > max(self.edges)) or (edge < min(self.edges)):
            raise Exception("This edge is not in the graph.")
        else:
            if edge in self.edges:
                ind = self.edges.index(edge)
                self.edges.remove(edge)
                for i in range(self.size):
                    del self.matrix[i][ind]
                    del self.weights[i][ind]
                del self.matrix[ind]
                del self.weights[ind]
                self.size-=1
            else:
                raise Exception("This edge is not in the graph.")
    def add_vertice(self, edge1, edge2, weight):
        if (edge1 > max(self.edges)) or (edge1 < min(self.edges)) or (edge2 > max(self.edges)) or (edge2 < min(self.edges)):
            raise Exception("At least one of the edges is not in the graph.")
        else:
            if (edge1 in self.edges)&(edge2 in self.edges):
                self.matrix[edge1-1][edge2-1] = 1
                self.matrix[edge2-1][edge1-1] = 1
                self.weights[edge1-1][edge2-1] = weight
                self.weights[edge2-1][edge1-1] = weight
            else:
                raise Exception("At least one of the edges is not in the graph.")
    def delete_vertice(self, edge1, edge2):
        if (edge1 > max(self.edges)) or (edge1 < min(self.edges)) or (edge2 > max(self.edges)) or (edge2 < min(self.edges)):
            raise Exception("At least one of the edges is not in the graph.")
        else:
            if (edge1 in self.edges)&(edge2 in self.edges):
                self.matrix[edge1-1][edge2-1] = 0
                self.matrix[edge2-1][edge1-1] = 0
                self.weights[edge1-1][edge2-1] = float('inf')
                self.weights[edge2-1][edge1-1] = float('inf')
            else:
                raise Exception("At least one of the edges is not in the graph.")
def convert_graph(graph, weighted:bool):
    if type(graph.matrix) == list:
        vertices = {}
        for i in range(graph.size):
            vertices["{key}".format(key = (i+1))] = [graph.edges[i] for i, x in enumerate(graph.matrix[i]) if x == 1]
        graph.matrix = vertices
        if weighted == True:
            weights = {}
            for i in range(graph.size):
                weights["{key}".format(key = (i+1))] = graph.weights[i]
            graph.weights = weights
    elif type(graph.matrix) == dict:
        vertices = [] 
        for i in range(graph.size):
            lst = []
            for j in range(graph.size):
                lst.append(int(graph.edges[i] in graph.matrix["{key}".format(key = (j+1))]))
            vertices.append(lst)
        graph.matrix = vertices
        if weighted == True:
            weights = []
            for i in range(graph.size):
                weights.append(graph.weights["{key}".format(key = (i+1))])
            graph.weights = weights
    return vertices
def generate_graph(n, p, min_weight, max_weight):
    matrix = []
    weights = []
    for i in range(n):
        matrix.append([0.5] * n)
        weights.append([0.5] * n)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 0.5:
                if i != j:
                    matrix[i][j] = matrix[j][i] = random.choices([0, 1], weights=(1-p, p))[0]
                else:
                    matrix[i][j] = 0
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                weights[i][j] = weights[j][i] = random.uniform(min_weight, max_weight)
            else:
                weights[i][j] = float('inf')
    graph = Undirected_weighted_graph(n, matrix, weights)
    return graph