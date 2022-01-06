# mesh_generator_2d.py by Konov D.S.
# Creates an 2d stefan_enthalpy ascii .mesh file out of arbitrary shapes
import math
import stefan_enthalpy_utils.ui as ui


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
            ui.error("Medium should not receive negative values as arguments")
        self.w = width
        self.h = height
        if hy is None:
            hy = hx
        self.nx = int(math.ceil(self.w / hx))
        self.ny = int(math.ceil(self.h / hy))

    def add_shape(self, index: int, shape: Shape):
        self.shapes.append((index, shape))

    def find(self, x, y):
        for shape in reversed(self.shapes):
            if shape[1].lies(x, y):
                return shape[0]
        ui.error("Some parts of the medium are left without material")

    def write(self, path):
        hx = self.w / self.nx
        hy = self.h / self.ny
        f = open(path, "w")
        f.write("%d %d\n" % (self.nx + 1, self.ny + 1))
        f.write("%f %f\n" % (self.w, self.h))
        ui.start_progress(self.ny + 1)
        for iy in range(self.ny + 1):
            ui.increase_progress()
            for ix in range(self.nx + 1):
                f.write("%d " % self.find(ix * hx, iy * hy))
            f.write("\n")
        f.close()
        ui.notice("Mesh at \"%s\" generated successfully" % path)


if __name__ == "__main__":

    # 0, 0 coordinates - left bottom corner
    #              w   h   hx
    u = 10.0
    t = 0.05 * 3
    m = Medium(300.05, 10.05 + u, 0.05)
    
    m.add_shape(3, Rect(0, 0, 300.05, u))
    m.add_shape(0, Rect(0, u + 0, 300.05, 10.05)) #Вода
    m.add_shape(5, Rect(0, u, 0.025, 10.05)) #Вода граница
    m.add_shape(5, Rect(300.025, u, 0.05, 10.05)) #Вода граница
    m.add_shape(2, Rect(0, u + 8.0025, 300.05, 100)) #Воздух
    m.add_shape(3, Rect(0, u + 0, 300.05, t - 0.05)) #Донный грунт
    m.add_shape(1, Rect(t, u + 8.0025, 300.05 - 2*t, 2.0025 - t + 0.05)) #Лед. При плавлении - воздух.
    m.add_shape(4, Rect(t, u + t - 0.05, 300.05 - 2*t, 8.0025 - t + 0.05))
    m.write("./mesh.mesh")
