import numpy as np
import subprocess
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

if __name__ == "__main__":
    
    files = os.listdir()
    for i in files:
        if i.split('.')[-1] == 'vtk':
            
            subprocess.call('a.exe ' + i, shell=True)
            
            Z = np.loadtxt(i + ".dat")

            fig, ax = plt.subplots()

            CS = ax.contour(Z, levels=9, cmap="Greys")
            print("\n[NOTICE] Levels for %s:" % i)
            print(CS.levels)
            exclusionList = []
            exclude1 = [item for item in CS.levels if item not in exclusionList]
            exclude = [item for item in exclude1 if item < 0]
            ax.clabel(CS, exclude, fmt='%1.0f °C', fontsize = 15.0)
            CS2 = plt.contourf(Z, levels=80, cmap="RdYlBu_r")
            time = float(int(i.split('.')[0].split('snapshot')[1]) * 50) / 60 / 60 / 24
            labeltext = 'Температурное распределение на краю острова в момент t = %.2f дней' % time
            ax.set_xlabel(labeltext)
            plt.savefig('./out/' + i +'.png')