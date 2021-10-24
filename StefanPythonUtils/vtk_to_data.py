# vtk_to_data.py by Konov D.S.
# Provides an interface convert vtk files
import numpy as np
import sys
import argparse
import struct


def create_parser():
    parser = argparse.ArgumentParser(description='Converting .vtk files into ASCII temperature data.')
    parser.add_argument('filename', metavar='filename.vtk', nargs=1, help='a file to convert.')
    parser.add_argument('-s', '--stride', nargs=3, default=[1, 1, 1], type=int, metavar=('Sn', 'Sm', 'Sl'), help='stride to enlarge vtk to temperature data')
    parser.add_argument('-d', '--dimensions', nargs=3, default=[0, 0, 0], type=int, metavar=('N', 'M', 'L'), help='dimensions of the vtk file')
    parser.add_argument('-o', '--output', default='out.data', help='output file name')
    return parser


def enlarge_3d(temperature, stride, size):
    if stride == [1, 1, 1]:
        return temperature
    else:
        print('[WARNING] Stride functionality untested')
    ret = []
    size[0] = int(size[0] / stride[0])
    size[1] = int(size[1] / stride[1])
    size[2] = int(size[2] / stride[2])
    for k in range(size[2]):
        for z in range(stride[2]):
            for i in range(size[1]):
                for y in range(stride[1]):
                    for j in range(size[0]):
                        for x in range(stride[0]):
                            ret.append(temperature[i*size[0] + j])
    return ret


def read(path, n):
    n = int(n)
    temperature = []
    f = open(path, "r")
    t = f.readline()
    while t != "SCALARS T FLOAT\n":
        t = f.readline()
    t = f.readline()
    try:
        for x in range(n):
            temperature.append(float(f.readline()))
    except ValueError:
        print("[ERROR] Temperature floats couldn't be read correctly. Exiting.")
        exit(-1)
    t = f.readline()
    if t != "SCALARS K FLOAT\n":
        print("[NOTICE] Not all floats were read. Size or stride may be wrong.")
    return temperature


def write(path, temperature):
    f = open(path, "wb")
    f.write(struct.pack("<%ud" % len(temperature), *temperature))
    f.close()


def convert_to_ascii(path, stride, dims, out_path):
    temperature = read(path, dims[0] * dims[1] * dims[2] / (stride[0] * stride[1] * stride[2]))
    temperature = enlarge_3d(temperature, stride, dims)
    write(out_path, temperature)


if __name__ == "__main__":
    parser = create_parser()
    namespace = parser.parse_args()
    print('[NOTICE] Starting conversion from VTK at "%s" with following parameters' % namespace.filename[0])
    print(namespace)
    if 0 in namespace.dimensions:
        print('[ERROR] Incorrect dimensions')
    else:
        convert_to_ascii(namespace.filename[0], namespace.stride, namespace.dimensions, namespace.output)
        print('[NOTICE] Successfully generated "%s"' % namespace.output)