import subprocess
import os

if __name__ == "__main__":
    files = os.listdir()
    for i in files:
        if i.split('.')[-1] == 'vtk':
            subprocess.call('a.exe ' + i + ' m.mesh ' + i.split('.')[0].split('t')[-1], shell=True)