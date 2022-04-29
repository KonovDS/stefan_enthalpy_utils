import stefan_enthalpy_utils.xml_generator as xml
import stefan_enthalpy_utils.data_generator_2d as data
import stefan_enthalpy_utils.mesh_generator_2d as mesh
import stefan_enthalpy_utils.ui as ui
import stefan_enthalpy_utils.vtk_to_data as vtk

import shutil
import os
import subprocess


# -----------------
# - SETUP 2D TASK -
# -----------------

problem_w = 2
problem_h = 10

h = 0.05

tau = 50
steps = 1000
steps_vtk = 100

up_depth = 5

down_temp = 0.1
up_temp = -40

border_temp = 20

# -----------------
# -               -
# -----------------


def setup_xml(up_boundary_temp):
    t = xml.Task(2, "1.mesh")
    
    up_layer = xml.Material(1500.0, 1.51, 1340.0, 1500.0, 1.86, 1113.0, 0.0, 60437.0)
    down_layer = xml.Material(1600.0, 1.5, 2100.0, 1600.0, 1.7, 1468.0, 0.0, 71957.0)

    t.add_material(0, down_layer)  
    t.add_material(1, up_layer)
    t.add_material(2, up_layer)  # Граница
    t.add_effect(2, xml.Effect('fixed', (str(up_boundary_temp), )))

    t.set_inistate_pernode("1.dat")

    t.set_time(steps, tau)
    t.set_vtk_period(steps_vtk)

    t.write("1.xml")


def setup_initial_mesh():
    # 0, 0 coordinates - left bottom corner
    m = mesh.Medium2D(problem_w, problem_h, h)

    m.add_shape(0, mesh.Rect(0, 0, problem_w, problem_h))
    m.add_shape(1, mesh.Rect(0, problem_h - up_depth, problem_w, up_depth))
    m.add_shape(2, mesh.Rect(0, problem_h - h, problem_w, h))

    m.write("1.mesh")


def setup_initial_temp():
    d = data.Medium2D(problem_w, problem_h, h)

    d.add_shape(data.Rect(0, 0, problem_w, problem_h - up_depth, down_temp))  # Многолетняя мерзлота
    d.add_shape(data.RectGradZ(0, problem_h - up_depth, problem_w, up_depth, up_temp, down_temp))

    d.write("1.dat")


def compute():
    ui.notice("Execution of stefan_enthalpy started", show_time=True)
    subprocess.call(".\\stefan_enthalpy.exe 1.xml", shell=True)
    ui.notice("Execution of stefan_enthalpy finished", show_time=True)



if __name__ == "__main__":
    ui.notice("Task started", show_time=True)
    setup_initial_mesh()
    setup_xml(border_temp)
    setup_initial_temp()
    compute()