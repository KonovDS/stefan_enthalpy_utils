import stefan_enthalpy_utils.xml_generator as xml
import stefan_enthalpy_utils.vtk_to_data_2d as vtk
import stefan_enthalpy_utils.mesh_generator_2d as mesh
import stefan_enthalpy_utils.ui as ui

import os
import subprocess


def setup_initial_xml(water_temp, air_temp, ground_temp, ice_temp, smooth):
    t = xml.Task(2, "1.mesh")
    water = xml.Material(1000.0, 0.591, 4180.0, 917.0, 2.22, 2100.0, 0.0, 334000.0)
    air = xml.Material(1.6, 0.022, 1007.0, 1.6, 0.022, 1007.0, -200.0, 1e9)
    ground = xml.Material(2500.0, 0.8, 750.0, 2500.0, 0.8, 750.0, 1000.0, 1e9)

    t.add_material(0, water)  # лед
    t.add_material(1, water)  # вода
    t.add_material(4, water)  # лед при плавлении вода
    t.add_material(2, ground)
    t.add_material(3, air)

    # Smoothing
    for i in range(5, 5 + smooth):
        t.add_material(i, water)
        temp = air_temp + (i - 4) * (water_temp - air_temp) / (smooth + 1)
        t.add_effect(i, xml.Effect('fixed', (str(temp), )))
        t.add_inistate_submesh(i, temp)

    t.add_effect(1, xml.Effect('fixed', (water_temp,)))
    # t.add_effect(2, xml.Effect('fixed', (ground_temp,)))
    t.add_effect(3, xml.Effect('fixed', (air_temp,)))

    t.add_effect(4, xml.Effect('on_melting', (3,)))

    t.add_boundary("x", "up", xml.Boundary("const_flux", (0,)))
    t.add_boundary("x", "down", xml.Boundary("const_flux", (0,)))
    t.add_boundary("y", "up", xml.Boundary("const_flux", (0,)))
    t.add_boundary("y", "down", xml.Boundary("const_flux", (0,)))

    t.add_inistate_submesh(0, ice_temp)  # ice
    t.add_inistate_submesh(4, ice_temp)  # ice при плавлении воздух
    t.add_inistate_submesh(1, water_temp)  # water
    t.add_inistate_submesh(2, ground_temp)  # ground
    t.add_inistate_submesh(3, air_temp)  # air

    t.set_time(260001, 50)
    t.set_vtk_period(32500)
    t.write("1.xml")


def setup_initial_mesh(smooth):
    # 0, 0 coordinates - left bottom corner
    #               w    h   hx
    m = mesh.Medium(302, 16, 0.05)

    m.add_shape(2, mesh.Rect(0, 0, 302, 5.5))  # ground
    m.add_shape(1, mesh.Rect(0, 5.5, 302, 10))  # water

    # Smoothing
    delta = 1.0 / smooth
    for i in range(5, 5 + smooth):
        m.add_shape(i, mesh.Rect(0, 13.5 - (i-4) / smooth, 302, delta))

    m.add_shape(3, mesh.Rect(0, 13.5, 302, 2.5))  # air
    m.add_shape(0, mesh.Rect(1, 5.5, 300, 8))  # ice
    m.add_shape(4, mesh.Rect(1, 13.5, 300, 2))  # ice при плавлении воздух

    m.write("1.mesh")


def compute(res_name):
    ui.notice("Execution of stefan_enthalpy started", show_time=True)
    subprocess.call(".\\stefan_enthalpy.exe 1.xml", shell=True)
    ui.notice("Execution of stefan_enthalpy finished", show_time=True)
    os.mkdir(".\\results\\" + res_name)
    for f in os.listdir(".\\bin\\out"):
        os.rename(".\\out\\" + f, ".\\results\\" + res_name + "\\" + f)


def setup_xml(water_temp, air_temp, ground_temp, ice_temp, smooth):
    print("TODO")


if __name__ == "__main__":
    ui.notice("Task started", show_time=True)
    setup_initial_mesh(5)
    setup_initial_xml(4, -30, 5, -10, 5)
    compute("test")
