import stefan_enthalpy_utils.xml_generator as xml
import stefan_enthalpy_utils.data_generator_3d as data
import stefan_enthalpy_utils.mesh_generator_3d as mesh
import stefan_enthalpy_utils.ui as ui
import stefan_enthalpy_utils.vtk_to_data as vtk

import shutil
import os
import subprocess

# TUNING:

temp_offset = 0  # may fix some problems in stefan_enthalpy
hx = 100
hz = 0.2

x = 2000
y = 2000
z = 300

depth = 5


def setup_xml(up_boundary_temp):
    t = xml.Task(3, "1.mesh")

    # LEGACY
    # water = xml.Material(1000.0, 0.591, 4180.0, 917.0, 2.22, 2100.0, 0.0, 334000.0)
    # up_layer = water

    up_layer = xml.Material(1500.0, 1.51, 1340.0, 1500.0, 1.86, 1113.0, 0.0 + temp_offset, 60437.0)
    # down_layer = xml.Material(1600.0, 1.5, 2100.0, 1600.0, 1.7, 1468.0, 0.0 + temp_offset, 71957.0)
    
    # methane = xml.Material(100.0, 1.86, 100.0, 100.0, 1.86, 100.0, -100.0 + temp_offset, 1e9)
    methane = up_layer
    down_layer = up_layer  # FIX (somehow??)

    t.add_material(0, down_layer)  # Многолетняя мерзлота
    t.add_material(1, up_layer)

    t.add_material(2, up_layer)  # Граница
    t.add_effect(2, xml.Effect('fixed', (str(up_boundary_temp + temp_offset), )))

    t.add_material(3, down_layer)  # Фикс боковушек
    t.add_effect(3, xml.Effect('fixed', (str(0.0 + temp_offset),)))
    
    #t.add_material(4, methane)  # Бомба
    #t.add_effect(4, xml.Effect('fixed', (str(0.0 + temp_offset),)))

    t.set_inistate_pernode("init.dat")

    t.set_time(500001, 500)
    t.set_vtk_period(5000)

    # t.set_vtk_period(325)  # TEST
    t.write("1.xml")


def setup_initial_mesh():
    # 0, 0, 0 coordinates - left bottom corner
    #                 w  h  z  hx
    m = mesh.Medium3D(x, y, z, hx, hx, hz)

    m.add_shape(0, mesh.Cube(0, 0, 0, x, y, z))  # Многолетняя мерзлота
    m.add_shape(1, mesh.Cube(0, 0, z - depth, x, y, depth))
    m.add_shape(2, mesh.Cube(0, 0, z - hz, x, y, hz))

    # Фикс боковушек:
    m.add_shape(3, mesh.Cube(0, 0, 0, hx / 2, hx / 2, z))
    m.add_shape(3, mesh.Cube(x - hx / 2, 0, 0, hx / 2, hx / 2, z))
    m.add_shape(3, mesh.Cube(0, y - hx / 2, 0, hx / 2, hx / 2, z))
    m.add_shape(3, mesh.Cube(x - hx / 2, y - hx / 2, 0, hx / 2, hx / 2, z))
    
    # Бомба
    #m.add_shape(4, mesh.Cube(0.5, 0.5, 12, 1, 1, 2))

    m.write("1.mesh")


def setup_initial_temp():
    d = data.Medium3D(x, y, z, hx, hx, hz)

    d.add_shape(data.Cube(0, 0, 0, x, y, z-depth, -0.1 + temp_offset))  # Многолетняя мерзлота
    d.add_shape(data.CubeGradZ(0, 0, z-depth, x, y, depth, -40 + temp_offset, -0.1 + temp_offset))

    d.write(".\\init.dat")


def compute():
    ui.notice("Execution of stefan_enthalpy started", show_time=True)
    subprocess.call(".\\stefan_enthalpy.exe 1.xml", shell=True)
    ui.notice("Execution of stefan_enthalpy finished", show_time=True)



if __name__ == "__main__":
    ui.notice("Task started", show_time=True)
    setup_initial_mesh()
    setup_xml(20)
    setup_initial_temp()
    compute()