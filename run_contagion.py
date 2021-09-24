import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
import typing
from collections import deque
from node import Node

def run_contagion_poisson(n: int, seed: int, z: float, capital_buffer: float, q: float) -> int:
    G = nx.fast_gnp_random_graph(n, z/n, seed=seed, directed=True)
    #G = nx.scale_free_graph(n)
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

    first_fail = np.random.randint(low=0, high=n)
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



def run_contagion_scale_free(n: int, seed: int, z: int, pow: float, capital_buffer: float, q: float) -> int:
    if(z==0):
        return 1
    a = min(1/(2*z), 0.49)
    b = 1 - 2*a
    delta = max(( pow*(1-a) - 2 + a )/(2*a), 0 )
    G = nx.scale_free_graph(n, alpha=a, beta=b, gamma=a, delta_in=delta, delta_out=delta, seed=seed) #this creates parallel edges...
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

    first_fail = np.random.randint(low=0, high=n)
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
