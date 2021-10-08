import networkx as nx
import numpy as np
from collections import deque
import random
import typing
import matplotlib.pyplot as plt
from node import Node
import time
from timeit import default_timer as timer

def runcont(n: int, seed: int, z: int, capital_buffer: float, q: float, targetcl):
    if(z==0):
        return 1


    G1 = nx.barabasi_albert_graph(n, int(z), seed=seed)
    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    for e in G1.edges():
        (a, b) = e
        if np.random.randint(low=0, high=2) == 0:
            G.add_edge(a, b)
        else:
            G.add_edge(b, a)


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

    # select nodes with outdegree = target
    cl_nodes_list = [node for node in G.nodes if (abs(nx.clustering(G, node) - targetcl) < 0.5) ]
    if(len(cl_nodes_list) == 0):
        return 0
    first_fail = cl_nodes_list[np.random.randint(low=0, high=len(cl_nodes_list))]
    
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
p = 0.005
q = 1
percentage_for_systemic = 0.05
n_iters = 100
capital_buffer = 0.04
z = 3
step = 1
interval_clt = np.arange(0, 10, step)
random.seed(rnd_seed)

count_systemic = np.zeros( int(10/step) )
avg_failed = np.zeros( int(10/step) )
avg_failed_coditioned = np.zeros( int(10/step) )

id = 0
for clt in interval_clt:
    print(" Executing test for tz = ", clt/10)

    start = timer()

    for iter in range(n_iters):
        cnt_failed = runcont(n, random.randint(0, 100000000), z, capital_buffer, q, clt/10)
        avg_failed[id] += cnt_failed
        if cnt_failed > percentage_for_systemic * n:
            count_systemic[id] += 1
            avg_failed_coditioned[id] += cnt_failed
        pass
    avg_failed[id] /= n_iters
    avg_failed_coditioned[id] /= count_systemic[id]
    id += 1
    end = timer()
    print(f' Elapsed time: {end - start}')
    pass

plt.plot(interval_clt, count_systemic)
plt.show()

with open('data/data_cntsyst_vs_clusteringattack.npy', 'wb') as f:
    np.save(f, count_systemic)
    np.save(f, avg_failed)
    np.save(f, avg_failed_coditioned)


pass



