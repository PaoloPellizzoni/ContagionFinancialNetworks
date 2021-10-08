import numpy as np
import matplotlib.pyplot as plt


'''
# plot 3D
step = 1
interval_z = np.arange(0, 20, step)
interval_cb = np.arange(0, 0.1, step/100)

with open('out/data_scalefree_ab_maxdegree_firstfail.npy', 'rb') as f:
    count_systemic = np.load(f)
    avg_failed = np.load(f)
    avg_failed_coditioned = np.load(f)

fig = plt.figure()
ax = fig.add_subplot(projection = '3d')
X, Y = np.meshgrid(interval_z, interval_cb)
ax.plot_surface(X, Y, count_systemic)
ax.set_xlabel("Average degree")
ax.set_ylabel("Capital buffer (%)")
plt.show()

fig, ax = plt.subplots()

c = ax.pcolormesh(X, Y, count_systemic, cmap='plasma')
ax.set_xlabel("Average degree")
ax.set_ylabel("Capital buffer (%)")
plt.show()
#'''

#'''
# plot cnt_sys vs centralities
step = 1
interval_z = np.arange(0, 10, step)

with open('out/data_cntsyst_vs_degreeattack.npy', 'rb') as f:
    count_systemic = np.load(f)
    avg_failed = np.load(f)
    avg_failed_coditioned = np.load(f)

fig = plt.figure()
ax = fig.add_subplot()
ax.plot(interval_z, count_systemic)
ax.set_ylabel("Systemic failures")
ax.set_xlabel("Degree of first failed bank")
plt.show()

