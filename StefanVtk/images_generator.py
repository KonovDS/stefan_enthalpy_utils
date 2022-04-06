import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

for x in os.listdir():
    if x.split(".")[-1] == "vtkd":
        Z = np.loadtxt(x)

        fig = plt.figure(figsize=(3, 7))
        ax = fig.add_subplot()

        CS = ax.contour(Z, levels=10, cmap="Greys")
        print(CS.levels)
        exclusionList = [1.5, 3, 4.5, 6, 7.5, 9, 10.5]
        exclude = [item for item in CS.levels if item not in exclusionList]
        ax.clabel(CS, exclude, fmt='%1.0f °C', fontsize = 15.0)
        CS2 = plt.contourf(Z, levels=80, cmap="RdYlBu_r")
        time = float(x.split("s")[-1].split(".")[0]) * 50 / 60 / 60 / 24
        ax.set_xlabel('Temperature distribution at day = ' + str(time))
        plt.savefig('./' + x.split(".")[0] +'.png')