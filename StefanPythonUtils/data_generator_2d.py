# data_generator_2d.py by Konov D.S.
# Creates an 2d stefan_enthalpy binary _temperature.data file out of arbitrary shapes
# Version 0.2
import math
import struct


class Shape:
    # Redefinition of this method in derivative classes may achieve desired form of the shape
    def lies(self, x, y):
        return False


class Rect(Shape):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def lies(self, x, y):

        def segment(base: float, length: float, value: float):
            if length < 0:
                base += length
                length = -length
            if base <= value <= base + length:
                return True
            else:
                return False

        if segment(self.x, self.w, x) and segment(self.y, self.h, y):
            return True
        else:
            return False


class Circle(Shape):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def lies(self, x, y):
        dx = x - self.x
        dy = y - self.y
        if dx * dx + dy * dy <= self.r * self.r:
            return True
        else:
            return False


class Medium:
    shapes = []

    def __init__(self, width, height, hx, hy=None):
        if (width < 0) or (height < 0) or (hx < 0) or ((hy is not None) and (hy < 0)):
            print('[ERROR] Medium should not receive negative values as arguments')
            exit(-2)
        self.w = width
        self.h = height
        if hy is None:
            hy = hx
        self.nx = int(math.ceil(self.w / hx))
        self.ny = int(math.ceil(self.h / hy))

    def add_shape(self, temp: float, shape: Shape):
        self.shapes.append((temp, shape))

    def find(self, x, y):
        for shape in reversed(self.shapes):
            if shape[1].lies(x, y):
                return shape[0]
        print('[ERROR] Some parts of the medium are left without material. Exiting')
        print('[NOTICE] You should set shapes to cover all of the medium')
        exit(-1)

    def write(self, path):
        hx = self.w / self.nx
        hy = self.h / self.ny
        temperature = []
        for iy in range(self.ny + 1):
            for ix in range(self.nx + 1):
                temperature.append(self.find(ix * hx, iy * hy))
        f = open(path, "wb")
        f.write(struct.pack("<%ud" % len(temperature), *temperature))		
        f.close()
        print('[NOTICE] Mesh at "%s" generated successfully' % path)


if __name__ == "__main__":
    #          w   h   hx
    m = Medium(300.0, 10.0, 0.05)
    #    Temperature   	  x  y  w      h
    m.add_shape(-40, Rect(0, 0, 300.0, 10.0))
    m.write("./my_temperature.data")
