import numpy as np
import matplotlib.pyplot as plt

'''
# capital buffer at 4%
step = 0.2
range = np.arange(0, 10, step)

with open('data_4%.npy', 'rb') as f:
    count_systemic = np.load(f)
    avg_failed = np.load(f)
    avg_failed_coditioned = np.load(f)

plt.scatter(range, avg_failed_coditioned)
plt.show()
plt.scatter(range, avg_failed)
plt.show()
#'''

#'''
# image 6
step = 0.5
interval_z = np.arange(0, 20, step)
interval_cb = np.arange(0, 0.1, step/100)

with open('data_compl_s05_it100.npy', 'rb') as f:
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
#'''
