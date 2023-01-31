import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the dimensions of the box
l = 2
b = 3
h = 4

# Create a 3D numpy array to represent the box
box = np.zeros((l, b, h))

# Plot the 3D representation of the box
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.voxels(box, edgecolor='k', facecolor='#565859', linewidth=0)

# Modify the x and y dimensions to create an asymmetric box
ax.set_xlim(0, 2)
ax.set_ylim(0, 2.5)

# Remove axis markings
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

# Remove the top bar
ax.set_frame_on(False)

plt.show()
