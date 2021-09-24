import networkx as nx
import numpy as np
from collections import deque
import random
import matplotlib.pyplot as plt
from node import Node
from run_contagion import *
import time
from timeit import default_timer as timer

def main():
    rnd_seed = 42
    n = 1000
    p = 0.005
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

    fig = plt.figure()
    ax = fig.add_subplot(projection = '3d')
    X, Y = np.meshgrid(interval_z, interval_cb)
    ax.plot_surface(X, Y, count_systemic)
    plt.show()

    with open('data/data.npy', 'wb') as f:
        np.save(f, count_systemic)
        np.save(f, avg_failed)
        np.save(f, avg_failed_coditioned)


    pass





if __name__ == '__main__':
    main()
