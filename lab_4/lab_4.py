from graph import * 
import time
import matplotlib.pyplot as plt
class Unionfind:
    def __init__(self):
        self.R = {}
        self.List = {}
        self.Next = {}
        self.Size = {}
        self.Internal_names = {}
        self.External_names = {}
    def Make_set(self, n, int_name, ext_name):
        self.R.update({n:int_name})
        self.List.update({int_name:n})
        self.Next.update({n:0})
        self.Internal_names.update({ext_name:int_name})
        self.External_names.update({int_name:ext_name})
        self.Size.update({int_name:1})
    def Find(self, x):
        for key, val in self.R.items():
            if key == x:
                return self.External_names[self.R[key]]
        return False
    def Union(self, x, y):
        if x == y:
            return False
        int_x = self.Internal_names[x]
        int_y = self.Internal_names[y]
        if self.Size[int_x] >= self.Size[int_y]:
            for key, val in self.R.items():
                if (self.Next[key] == 0)&(val == int_x):
                    self.Next[key] = self.List[int_y]
                if self.R[key] == str(int_y):
                    self.R[key] = str(int_x)
            del self.Internal_names[y]
            del self.External_names[int_y]
            self.Size[int_x]+=self.Size[int_y]
            del self.Size[int_y]
            del self.List[int_y]
        else:
            for key, val in self.R.items():
                if (self.Next[key] == 0)&(val == int_y):
                    self.Next[key] = self.List[int_x]
                if self.R[key] == str(int_x):
                    self.R[key] = str(int_y)
            del self.Internal_names[x]
            del self.External_names[int_x]
            self.Size[int_y]+=self.Size[int_x]
            del self.Size[int_x]
            del self.List[int_x]

def create_new_matrix(graph):
    matrix = []
    if type(graph.matrix) == dict:
        convert_graph(graph, True)
    for i in range(graph.size):
        for j in range(graph.size):
            if graph.weights[i][j] != -1:
                matrix.append([i+1, j+1, graph.weights[i][j]])
    return matrix

def Kruskals(graph):
    data = create_new_matrix(graph)
    data.sort(key=lambda x: x[2])
    result = []
    un_fi = Unionfind()
    for i in graph.edges:
        un_fi.Make_set(i, i, i)
    start_time = time.time()
    for u, v, w in data:
        if (u in un_fi.External_names)&(v in un_fi.External_names):
            if un_fi.Find(u) != un_fi.Find(v):
                un_fi.Union(un_fi.External_names[u], un_fi.External_names[v])
                result.append((u, v, w))
    return result, time.time()-start_time


def mesure_time(start_n, end_n, step_n, p, min_weight, max_weight):
    time_mesured = []
    for i in range(start_n, end_n, step_n):
        G = generate_graph(i, p, min_weight, max_weight)
        time_mesured.append(Kruskals(G)[-1])
    return time_mesured
times = mesure_time(100, 1000, 10, 1, 10, 500)
nums = []
for i in range(100, 1000, 10):
    nums.append(i)
print(times)
plt.plot(times, nums)
plt.show()
