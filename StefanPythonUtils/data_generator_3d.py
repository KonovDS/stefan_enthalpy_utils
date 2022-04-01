# data_generator_3d.py by Konov D.S.
# Creates an 3d stefan_enthalpy binary _temperature.data file out of arbitrary shapes
# Version 0.1
import numpy as np
import sys
import struct
import math
import stefan_enthalpy_utils.ui as ui


class Shape3D:
    # Redefinition of this method in derivative classes may achieve desired form of the shape
    def lies(self, x, y, z):
        return False

    def temp(self, x, y, z):
        return float(0)


def segment(base: float, length: float, value: float):
    if length < 0:
        base += length
        length = -length
    if base <= value <= base + length:
        return True
    else:
        return False


class Cube(Shape3D):
    def __init__(self, x0, y0, z0, w, l, h, cube_temp):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.w = w
        self.l = l
        self.h = h
        self.cube_temp = cube_temp

    def lies(self, x, y, z):
        if segment(self.x0, self.w, x) and segment(self.y0, self.l, y) and segment(self.z0, self.h, z):
            return True
        else:
            return False

    def temp(self, x, y, z):
        return float(self.cube_temp)


class CubeGradZ(Shape3D):
    def __init__(self, x0, y0, z0, w, l, h, temp_up, temp_down):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.w = w
        self.l = l
        self.h = h
        self.temp_up = temp_up
        self.temp_down = temp_down

    def lies(self, x, y, z):
        if segment(self.x0, self.w, x) and segment(self.y0, self.l, y) and segment(self.z0, self.h, z):
            return True
        else:
            return False

    def temp(self, x, y, z):
        return float(self.temp_down + (self.temp_up - self.temp_down) * (z - self.z0) / self.h)


class Medium3D:
    shapes = []

    def __init__(self, width, length, height, hx, hy=None, hz=None):
        if (width < 0) or (length < 0) or (height < 0) or (hx < 0) or ((hy is not None) and (hy < 0)) or (
                (hz is not None) and (hz < 0)):
            ui.error("Medium should not receive negative values as arguments")
            exit(-2)
        self.w = width
        self.h = height
        self.l = length
        if hz is None:
            hz = hx
        if hy is None:
            hy = hx
        self.nx = int(math.ceil(self.w / hx))
        self.ny = int(math.ceil(self.l / hy))
        self.nz = int(math.ceil(self.h / hz))

    def add_shape(self, shape: Shape3D):
        self.shapes.append(shape)

    def find(self, x, y, z):
        for shape in reversed(self.shapes):
            if shape.lies(x, y, z):
                return shape.temp(x, y, z)
        ui.error("Some parts of the medium are left without temperature data")
        exit(-1)

    def temp_list(self):
        ret = []
        hx = self.w / self.nx
        hy = self.l / self.ny
        hz = self.h / self.nz
        for iz in range(self.nz + 1):
            for iy in range(self.ny + 1):
                for ix in range(self.nx + 1):
                    ret.append(float(self.find(ix * hx, iy * hy, iz * hz)))
        return ret

    def write(self, path):
        ret = self.temp_list()
        f = open(path, "wb")
        f.write(struct.pack("<%ud" % len(ret), *ret))
        f.close()
        ui.notice("Data at \"%s\" generated successfully" % path)
