# mesh_generator_3d.py by Konov D.S.
# Creates an 3d stefan_enthalpy ascii .mesh file out of arbitrary shapes
import math


class Shape3D:
    # Redefinition of this method in derivative classes may achieve desired form of the shape
    def lies(self, x, y, z):
        return False


def segment(base: float, length: float, value: float):
    if length < 0:
        base += length
        length = -length
    if base <= value <= base + length:
        return True
    else:
        return False


class Cube(Shape3D):
    def __init__(self, x0, y0, z0, w, l, h):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.w = w
        self.l = l
        self.h = h

    def lies(self, x, y, z):
        if segment(self.x0, self.w, x) and segment(self.y0, self.l, y) and segment(self.z0, self.h, z):
            return True
        else:
            return False


class Cylinder(Shape3D):
    def __init__(self, x0, y0, z0, r, h):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.r = r
        self.h = h

    def lies(self, x, y, z):
        if segment(self.z0, self.h, z) and segment(0, self.r, math.sqrt((x - self.x0) ** 2 + (y - self.y0) ** 2)):
            return True
        else:
            return False


class Medium3D:
    shapes = []

    def __init__(self, width, length, height, hx, hy=None, hz=None):
        if (width < 0) or (length < 0) or (height < 0) or (hx < 0) or ((hy is not None) and (hy < 0)) or (
                (hz is not None) and (hz < 0)):
            print('[ERROR] Medium should not receive negative values as arguments')
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

    def add_shape(self, index: int, shape: Shape3D):
        self.shapes.append((index, shape))

    def find(self, x, y, z):
        for shape in reversed(self.shapes):
            if shape[1].lies(x, y, z):
                return shape[0]
        print('[ERROR] Some parts of the medium are left without material')
        print('[NOTICE] You should set shapes to cover all of the medium')
        exit(-1)

    def write(self, path):
        hx = self.w / self.nx
        hy = self.l / self.ny
        hz = self.h / self.nz
        f = open(path, "w")
        f.write("%d %d %d\n" % (self.nx + 1, self.ny + 1, self.nz + 1))
        f.write("%f %f %f\n" % (self.w, self.l, self.h))
        for iz in range(self.nz + 1):
            for iy in range(self.ny + 1):
                for ix in range(self.nx + 1):
                    f.write("%d " % self.find(ix * hx, iy * hy, iz * hz))
                f.write("\n")
        f.close()
        print('[NOTICE] Mesh at "%s" generated successfully' % path)


if __name__ == "__main__":
    m = Medium3D(300, 300, 11, 1, 1, 0.5)
    m.add_shape(1, Cube(0, 0, 0, 300, 300, 11))
    m.add_shape(3, Cube(0, 0, 8.5, 300, 300, 2.5)) 
    m.add_shape(0, Cylinder(150, 150, 0.5, 149, 10))
    m.add_shape(2, Cube(0, 0, 0, 300, 300, 0.5))
    m.write("1.mesh")
