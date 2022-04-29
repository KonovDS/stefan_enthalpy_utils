# data_generator_3d.py by Konov D.S.
# Creates an 2d stefan_enthalpy binary _temperature.data file out of arbitrary shapes
# Version 0.3
import numpy as np
import sys
import struct
import math
import stefan_enthalpy_utils.ui as ui


class Shape2D:
    # Redefinition of this method in derivative classes may achieve desired form of the shape
    def lies(self, x, y):
        return False

    def temp(self, x, y):
        return float(0)


def segment(base: float, length: float, value: float):
    if length < 0:
        base += length
        length = -length
    if base <= value <= base + length:
        return True
    else:
        return False


class Rect(Shape2D):
    def __init__(self, x0, y0, w, h, cube_temp):
        self.x0 = x0
        self.y0 = y0
        self.w = w
        self.h = h
        self.cube_temp = cube_temp

    def lies(self, x, y):
        if segment(self.x0, self.w, x) and segment(self.y0, self.h, y):
            return True
        else:
            return False

    def temp(self, x, y):
        return float(self.cube_temp)


class RectGradZ(Shape2D):
    def __init__(self, x0, y0, w, h, temp_up, temp_down):
        self.x0 = x0
        self.y0 = y0
        self.w = w
        self.h = h
        self.temp_up = temp_up
        self.temp_down = temp_down

    def lies(self, x, y):
        if segment(self.x0, self.w, x) and segment(self.y0, self.h, y):
            return True
        else:
            return False

    def temp(self, x, y):
        return float(self.temp_down + (self.temp_up - self.temp_down) * (y - self.y0) / self.h)


class Medium2D:
    shapes = []

    def __init__(self, width, height, hx, hy=None):
        if (width < 0) or (height < 0) or (hx < 0) or ((hy is not None) and (hy < 0)):
            ui.error("Medium should not receive negative values as arguments")
            exit(-2)
        self.w = width
        self.h = height
        if hy is None:
            hy = hx
        self.nx = int(math.ceil(self.w / hx))
        self.ny = int(math.ceil(self.h / hy))

    def add_shape(self, shape: Shape2D):
        self.shapes.append(shape)

    def find(self, x, y):
        for shape in reversed(self.shapes):
            if shape.lies(x, y):
                return shape.temp(x, y)
        ui.error("Some parts of the medium are left without temperature data")
        exit(-1)

    def temp_list(self):
        ret = []
        hx = self.w / self.nx
        hy = self.h / self.ny
        for iy in range(self.ny + 1):
            for ix in range(self.nx + 1):
                ret.append(float(self.find(ix * hx, iy * hy)))
        return ret

    def write(self, path):
        ret = self.temp_list()
        f = open(path, "wb")
        f.write(struct.pack("<%ud" % len(ret), *ret))
        f.close()
        ui.notice("Data at \"%s\" generated successfully" % path)
