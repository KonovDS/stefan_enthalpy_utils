# vtk_to_data_2d.py by Konov D.S.
# Creates an 2d stefan_enthalpy binary _temperature.data file out of vtk output file

import struct


def enlarge(temperature, stride, size):
    if stride == [1, 1]:
        return temperature
    ret = []
    size[0] = int(size[0] / stride[0])
    size[1] = int(size[1] / stride[1])
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
        print("[ERROR] %d temperature floats couldn't be read correctly. Exiting.")
        exit(-1)
    t = f.readline()
    if t != "SCALARS K FLOAT\n":
        print("[NOTICE] Not all floats were read. Size or stride may be wrong.")
    return temperature


def write(path, temperature):
    f = open(path, "wb")
    f.write(struct.pack("<%ud" % len(temperature), *temperature))
    f.close()
    print('[NOTICE] Mesh at "%s" generated successfully' % path)


def vtk_to_data(inp, out, stride, size):
    temp = read(inp, size[0] * size[1] / (stride[0] * stride[1]))
    temp = enlarge(temp, stride, size)
    write(out, temp)


def main():
    filename = "start_temp.vtk"
    output = "vtk_out.data"
    stride = [2, 2]
    size = [6002, 402]

    temperature = read(filename, size[0] * size[1] / (stride[0] * stride[1]))
    temperature = enlarge(temperature, stride, size)
    write(output, temperature)


if __name__ == "__main__":
    main()
