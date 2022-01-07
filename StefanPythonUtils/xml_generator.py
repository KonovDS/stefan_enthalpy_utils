# xml_generator.py by Konov D.S.
# Creates a stefan_enthalpy xml config file
import os


class Material:
    def __init__(self, l_density, l_conductivity, l_capacity, s_density, s_conductivity, s_capacity, t_phase, fusion):
        self.l_density = l_density
        self.l_conductivity = l_conductivity
        self.l_capacity = l_capacity
        self.s_density = s_density
        self.s_conductivity = s_conductivity
        self.s_capacity = s_capacity
        self.t_phase = t_phase
        self.fusion = fusion

    def ret(self):
        return ["TPhase", "densityL", "densityS", "thermalConductivityL", "thermalConductivityS", "specificHeatFusion", "specificHeatCapacityL", "specificHeatCapacityS", ],\
               [self.t_phase, self.l_density, self.s_density, self.l_conductivity, self.s_conductivity, self.fusion, self.l_capacity, self.s_capacity, ]


class Effect:
    types = {
        'on_melting': ('ChangeIndexOnMelting', ('newIndex', )),
        'fixed': ('FixedTemperature', ('temperature', )),
    }

    def __init__(self, effect_type, parameters):
        if effect_type not in self.types:
            print('[ERROR] Incorrect effect "%s"' % effect_type)
            exit(-1)
        if len(parameters) != len(self.types[effect_type][1]):
            print('[ERROR] Not enough parameters for effect "%s"' % effect_type)
            exit(-1)
        self.out = (self.types[effect_type][0], list(self.types[effect_type][1]), list(parameters))


class Boundary:
    types = {
        'const_flux': ('FixedFlux', ('flux', )),
        'const_temp': ('FixedTemperature', ('temperature', )),
        # 'mixed': ('Mixed', ('newIndex', )),
    }
    sides = {
        'up': 1, '+': 1, '1': 1,
        'down': 0, '-': 0, '0': 0,
    }
    axises = {
        'x': 'x',
        'y': 'y',
        'z': 'z',
    }

    def __init__(self, boundary_type, parameters):
        if boundary_type not in self.types:
            print('[ERROR] Incorrect boundary type "%s"' % boundary_type)
            exit(-1)
        if len(parameters) != len(self.types[boundary_type][1]):
            print('[ERROR] Not enough parameters for boundary type "%s"' % boundary_type)
            exit(-1)
        self.out = (self.types[boundary_type][0], list(self.types[boundary_type][1]), list(parameters))


class Task:
    

    def __init__(self, dim, mesh_path):
        self.dim = dim
        self.mesh_path = mesh_path
        self.vtk = None
        self.time = None
        self.materials = []
        self.effects = []
        self.boundaries = []
        self.initial_temps_submesh = []
        self.initial_temps_pernode_path = ""

    def add_material(self, index, material: Material):
        if index in [x for x in self.materials if x[0] == index]:
            print('[ERROR] Multiple materials can not have the same index')
            exit(-1)
        self.materials.append((index, material))

    def add_effect(self, index, effect: Effect):
        self.effects.append((index, effect))

    def add_boundary(self, axis, side, boundary: Boundary):
        if axis not in Boundary.axises or side not in Boundary.sides:
            print('[ERROR] Incorrect boundary "%s", "%d"' % axis, side)
            exit(-1)
        side_num = Boundary.sides[side]
        self.boundaries.append((axis, side_num, boundary, ))

    vtk_default = {
        'writeEnthalpy': 'true',
        'writeTemperature': 'true',
        'writeThermalElasticity': 'true',
        'writeState': 'true'
    }

    def set_vtk_period(self, frames, stride='1 1 1', out_path='out/s<step>.vtk'):
        self.vtk = (frames, stride, out_path)

    def set_time(self, total, step):
        self.time = (total, step)

    def set_inistate_pernode(self, path):
        self.initial_temps_pernode_path = path

    def add_inistate_submesh(self, index, temperature):
        self.initial_temps_submesh.append((index, temperature, ))

    def write(self, path):
        f = open(path, "w")
        f.write('<?xml version="1.0" encoding="UTF-8" ?>' + "\n")
        count = 0

        def open_tag(tag_name, attributes=(), values=(), close=False):
            nonlocal count
            nonlocal f
            if len(attributes) != len(values):
                print('[ERROR] Internal error during "%s"' % tag_name)
                exit(-1)
            s = ''
            for i in range(0, count):
                s += "  "
            s += '<%s' % tag_name
            for i in range(0, len(attributes)):
                s += ' ' + str(attributes[i]) + ' = "' + str(values[i]) + '"'
            if close:
                s += '/'
            s += ">\n"
            f.write(s)
            if not close:
                count += 1

        def close_tag(tag_name):
            nonlocal count
            nonlocal f
            count -= 1
            s = ''
            for i in range(0, count):
                s += "  "
            f.write(s + '</%s>' % tag_name + "\n")

        # Sorting of the materials and inistates:
        self.initial_temps_submesh.sort(key=lambda tup: tup[0])
        self.materials.sort(key=lambda tup: tup[0])
        # Start of xml tree

        open_tag("Settings", ("dimsCount", ), ("%d" % self.dim, ))
        open_tag("Mesh", ("meshFile", ), ("%s" % self.mesh_path, ))
        open_tag("MediumParams")
        for x in self.materials:
            a, b = x[1].ret()
            a.insert(0, "index")
            b.insert(0, "%s" % x[0])
            open_tag("Submesh", a, b)
            for y in self.effects:
                if y[0] == x[0]:
                    open_tag("Effects")
                    for z in self.effects:
                        if z[0] == x[0]:
                            open_tag(z[1].out[0], z[1].out[1], z[1].out[2], True)
                    close_tag("Effects")
                    break
            close_tag("Submesh")
        open_tag("Boundaries")
        for x in self.boundaries:
            name, a, b = x[2].out
            a.insert(0, "axis")
            a.insert(1, "side")
            b.insert(0, x[0])
            b.insert(1, x[1])
            open_tag(name, a, b, True)
        close_tag("Boundaries")
        close_tag("MediumParams")
        close_tag("Mesh")
        open_tag("Snapshot")
        open_tag("Period", ("frames", ), ("%d" % self.vtk[0], ), True)
        a = ["fileName", "stride"]
        b = [self.vtk[2], self.vtk[1]]
        for x in self.vtk_default:
            a.append(x)
            b.append(self.vtk_default[x])
        open_tag("Data", a, b, True)
        close_tag("Snapshot")
        open_tag("Task", ("numberOfSteps", "timeStep", ), (self.time[0], self.time[1], ))
        open_tag("IniState")
        if self.initial_temps_pernode_path == "":
            open_tag("PerSubmesh")
            for x in self.initial_temps_submesh:
                open_tag("Submesh", ("index", "temperature", ), ("%d" % x[0], "%f" % x[1], ), True)
            close_tag("PerSubmesh")
        else:
            open_tag("PerNode", ("fileName", ), ("%s" % self.initial_temps_pernode_path, ), True)
        close_tag("IniState")
        close_tag("Task")
        close_tag("Settings")
        f.close()
        print('[NOTICE] XML config at "%s" generated successfully' % path)


if __name__ == "__main__":
    t = Task(3, "1.mesh")
    water = Material(1000.0, 0.591, 4180.0, 917.0, 2.22, 2100.0, 0.0, 334000.0)
    air = Material(1.6, 0.022, 1007.0, 1.6, 0.022, 1007.0, -200.0, 1e9)
    ground = Material(2500.0, 0.8, 750.0, 2500.0, 0.8, 750.0, 1000.0, 1e9)

    t.add_material(0, water)
    t.add_material(1, water)
    t.add_material(2, ground)
    t.add_material(3, air)

    t.add_effect(1, Effect('fixed', ('3',)))
    t.add_effect(2, Effect('fixed', ('5',)))
    t.add_effect(3, Effect('fixed', ('-40',)))
    
    t.add_boundary("x", "up", Boundary("const_temp", (3, )))
    t.add_boundary("x", "down", Boundary("const_temp", (3, )))
    t.add_boundary("y", "up", Boundary("const_temp", (3, )))
    t.add_boundary("y", "down", Boundary("const_temp", (3, )))
    t.add_boundary("z", "up", Boundary("const_temp", (-40, )))
    t.add_boundary("z", "down", Boundary("const_flux", (0, )))

    t.add_inistate_submesh(0, -10)
    t.add_inistate_submesh(1, 3)
    t.add_inistate_submesh(2, 5)
    t.add_inistate_submesh(3, -40)
    
    t.set_time(518401, 5)
    t.set_vtk_period(20736)
    t.write("1.xml")