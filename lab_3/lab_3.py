from graph import *
import time
import matplotlib.pyplot as plt
import pandas as pd

def floyd_warshall(graph):
    start_time = time.time()
    V = len(graph.edges)
    g = graph.weights.copy()
    for k in range(V):
        for i in range(V):
            for j in range(V):
                if i != j:
                    g[i][j] = min(g[i][j], g[i][k] + g[k][j])
                else:
                    g[i][j] = 0
    return g, time.time()-start_time
def dijkstra(graph, start):
    g = graph.weights
    distances = [float("inf") for _ in range(len(g))]
    visited = [False for _ in range(len(g))]
    distances[start] = 0
    while True:
        shortest_distance = float("inf")
        shortest_index = -1
        for i in range(len(g)):
            if distances[i] < shortest_distance and not visited[i]:
                shortest_distance = distances[i]
                shortest_index = i
        if shortest_index == -1:
            return distances
        for i in range(len(g[shortest_index])):
            if g[shortest_index][i] != 0 and distances[i] > distances[shortest_index] + g[shortest_index][i]:
                distances[i] = distances[shortest_index] + g[shortest_index][i]
        visited[shortest_index] = True
    return distances
def dijkstra_all(graph):
    start_time = time.time()
    for i in range(len(graph.edges)):
        dijkstra(graph, i)
    return time.time()-start_time
def mesure_time(start_n, end_n, step_n, p, min_weight, max_weight, alg:str):
    time_mesured = []
    if alg == 'floyd_warshall':
        for i in range(start_n, end_n, step_n):
            G = generate_graph(i, p, min_weight, max_weight)
            time_mesured.append(floyd_warshall(G)[-1])
    elif alg == 'dijkstra':
        for i in range(start_n, end_n, step_n):
            G = generate_graph(i, p, min_weight, max_weight)
            time_mesured.append(dijkstra_all(G))
    return time_mesured

times_floyd_warshall_p_1 = mesure_time(10, 100, 1, 1, 10, 500, 'floyd_warshall')
times_dijkstra_p_1 = mesure_time(10, 100, 1, 1, 10, 500, 'dijkstra')
times_floyd_warshall_p_05 = mesure_time(10, 100, 1, 0.5, 10, 500, 'floyd_warshall')
times_dijkstra_p_05 = mesure_time(10, 100, 1, 0.5, 10, 500, 'dijkstra')
nums = []
for i in range(10, 100):
    nums.append(i)
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax1.set_title('probability of vertice existing = 1')
ax2 = fig.add_subplot(122)
ax2.set_title('probability of vertice existing = 0.5')
ax1.plot(times_floyd_warshall_p_1, nums, label='floyd_warshall')
ax1.plot(times_dijkstra_p_1, nums, label='dijkstra')
ax1.set_xlabel('time')
ax1.set_ylabel('number of edges')
ax2.plot(times_floyd_warshall_p_05, nums, label='floyd_warshall')
ax2.plot(times_dijkstra_p_05, nums, label='dijkstra')
ax2.set_xlabel('time')
ax2.set_ylabel('number of edges')
ax1.legend()
ax2.legend()
plt.show()
data_p_1 = pd.DataFrame({'Floyd Warshall for p = 1':times_floyd_warshall_p_1,
                        'Dijkstra for p = 1':times_dijkstra_p_1})
data_p_05 = pd.DataFrame({'Floyd Warshall for p = 0.5':times_floyd_warshall_p_05,
                        'Dijkstra for p = 0.5':times_dijkstra_p_05})
data_p_1.to_csv('time_p_1.csv')
data_p_05.to_csv('time_p_0.5.csv')