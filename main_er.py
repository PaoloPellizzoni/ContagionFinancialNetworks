import networkx as nx
import numpy as np
from collections import deque
import random
import matplotlib.pyplot as plt
from node import Node
import time
from timeit import default_timer as timer
from mpl_toolkits.mplot3d import Axes3D 

def run_contagion_poisson(n: int, seed: int, z: float, capital_buffer: float, q: float) -> int:
    G = nx.fast_gnp_random_graph(n, z/n, seed=seed, directed=True)
    list_nodes = []

    for i in range(n):
        ia = np.random.standard_normal(1)[0] + 10
        if G.in_degree(i) == 0:
            ia = 0
        ea = ia*4
        list_nodes.append(Node(ia, 0, ea, 0))


    for i in range(n):
        il = 0
        for v in G.neighbors(i):
            il += list_nodes[v].interbank_asset / G.in_degree(v)
        list_nodes[i].interbank_liability = il
        list_nodes[i].deposits = (list_nodes[i].interbank_asset + list_nodes[i].external_assets)*(1 - capital_buffer) - il

    # max degree attack
    max_grade = max(G.degree, key=lambda x: x[1])[1]
    max_grade_nodes_list = [node[0] for node in G.degree if node[1] == max_grade]
    first_fail = max_grade_nodes_list[np.random.randint(low=0, high=len(max_grade_nodes_list))]
    
    # random
    #first_fail = np.random.randint(low=0, high=n)
    
    queue = deque([])
    queue.append(first_fail)
    # first bank to fail
    list_nodes[first_fail].failed = True
    for v in G.successors(first_fail):
        queue.append(v)
        list_nodes[v].failed_pred += 1

    cnt_failed = 1
    while len(queue) > 0:
        u = queue.pop()
        if (list_nodes[u].failed == False):
            tmp = ( list_nodes[u].k() - (1-q)*list_nodes[u].external_assets ) / list_nodes[u].interbank_asset
            frac = list_nodes[u].failed_pred / G.in_degree(u)
            if ( tmp <= frac ):
                list_nodes[u].failed = True
                cnt_failed += 1
                for v in G.successors(u):
                    queue.append(v)
                    list_nodes[v].failed_pred += 1

    return cnt_failed



rnd_seed = 42
n = 1000
q = 1
percentage_for_systemic = 0.05
n_iters = 100
step = 1
interval_z = np.arange(0, 20, step)
interval_cb = np.arange(0, 0.1, step/100)

random.seed(rnd_seed)

count_systemic = np.zeros((int(10/step), int(20/step)))
avg_failed = np.zeros((int(10/step), int(20/step)))
avg_failed_coditioned = np.zeros((int(10/step), int(20/step)))

id2 = 0
for capital_buffer in interval_cb:
    print("Executing test for cb = ", capital_buffer)
    id = 0
    for z in interval_z:
        print(" Executing test for z = ", z)

        start = timer()

        for iter in range(n_iters):
            cnt_failed = run_contagion_poisson(n, random.randint(0, 100000000), z, capital_buffer, q)
            avg_failed[id2][id] += cnt_failed
            if cnt_failed > percentage_for_systemic * n:
                count_systemic[id2][id] += 1
                avg_failed_coditioned[id2][id] += cnt_failed
            pass
        avg_failed[id2][id] /= n_iters
        avg_failed_coditioned[id2][id] /= count_systemic[id2][id]
        id += 1
        end = timer()
        print(f' Elapsed time: {end - start}')
        pass
    id2 += 1
    
    
with open('data/data_er_maxdegreeattack.npy', 'wb') as f:
    np.save(f, count_systemic)
    np.save(f, avg_failed)
    np.save(f, avg_failed_coditioned)


fig = plt.figure()
ax = fig.add_subplot(projection = '3d')
X, Y = np.meshgrid(interval_z, interval_cb)
ax.plot_surface(X, Y, count_systemic)
plt.show()



pass




