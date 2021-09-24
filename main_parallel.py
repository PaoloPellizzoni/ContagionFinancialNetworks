import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
import time
from collections import deque
from node import Node
from run_contagion import *
from timeit import default_timer as timer
from multiprocessing import Pool, cpu_count

def main():
    print(f'Starting computations on {cpu_count()} cores')
    rnd_seed = 42
    n = 1000
    q = 1
    percentage_for_systemic = 0.05
    n_iters = 100
    step = 0.5
    interval_z = np.arange(0, 20, step)
    interval_cb = np.arange(0, 0.1, step/100)

    random.seed(rnd_seed)

    count_systemic = np.zeros((len(interval_cb), len(interval_z)))
    avg_failed = np.zeros((len(interval_cb), len(interval_z)))
    avg_failed_coditioned = np.zeros((len(interval_cb), len(interval_z)))

    id2 = 0
    for capital_buffer in interval_cb:
        print("Executing test for cb = ", capital_buffer)
        id = 0
        for z in interval_z:
            print(" Executing test for z = ", z)
            start = timer()
            with Pool() as pool:
                cnt_failed = pool.starmap(run_contagion_poisson, [ (n, random.randint(0, 100000000), z, capital_buffer, q) for _ in range(n_iters) ]  )

            for iter in range(n_iters):
                #cnt_failed = run.run_contagion(n, random.randint(0, 100000000), z, capital_buffer, q)
                avg_failed[id2][id] += cnt_failed[iter]
                if cnt_failed[iter] > percentage_for_systemic * n:
                    count_systemic[id2][id] += 1
                    avg_failed_coditioned[id2][id] += cnt_failed[iter]
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
