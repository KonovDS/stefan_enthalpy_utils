import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

Z = np.loadtxt("1.dat")

fig, ax = plt.subplots()

CS = ax.contour(Z, levels=10, cmap="Greys")
print(CS.levels)
exclusionList = [2, 1]
exclude = [item for item in CS.levels if item not in exclusionList]
ax.clabel(CS, exclude, fmt='%1.0f °C', fontsize = 15.0)
CS2 = plt.contourf(Z, levels=80, cmap="RdYlBu_r")
plt.show()