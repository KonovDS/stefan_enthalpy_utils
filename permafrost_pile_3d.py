import stefan_enthalpy_utils.xml_generator as xml
import stefan_enthalpy_utils.data_generator_3d as data
import stefan_enthalpy_utils.mesh_generator_3d as mesh
import stefan_enthalpy_utils.ui as ui
import stefan_enthalpy_utils.vtk_to_data as vtk

import shutil
import os
import subprocess


# -----------------
# - SETUP 2D TASK -
# -----------------

problem_w = 10
problem_h = 20

hx = 0.3
hz = 0.3

tau = 1
steps = 2592000 # 30 days
steps_vtk = 172800 # 2 days

z1 = 14
z2 = 4
z3 = 2

dd = hx * 3

merz_depth = 6
down_temp = -4
up_temp = 30

beton_w = 0.3
beton_l = 14

enable_beton = True

# -----------------
# -               -
# -----------------


def setup_xml():
    t = xml.Task(3, "1.mesh")
    
    up_layer = xml.Material(1000, 2.56, 3150, 1000, 2.73, 2350, 0, 71957)
    middle_layer = xml.Material(1000, 1.51, 3150, 1000, 1.7, 2350, 0, 71957)
    down_layer = xml.Material(1000, 1.51, 2010, 1000, 1.86, 1670, 0, 60437)
    beton = xml.Material(1000, 2.04, 3000, 1000, 2.04, 3000, 100, 0)
    
    t.add_material(0, up_layer)
    t.add_material(1, middle_layer)
    t.add_material(2, down_layer)
    
    t.add_material(3, up_layer)
    t.add_effect(3, xml.Effect('fixed', (str(up_temp), )))
    
    if enable_beton:
        beton = xml.Material(1000, 9.04, 3000, 1000, 9.04, 3000, 100, 0)
        t.add_material(4, beton)
    
    t.set_inistate_pernode("1.dat")

    t.set_time(steps + 1, tau)
    t.set_vtk_period(steps_vtk)

    t.write("1.xml")

def setup_initial_mesh():
    # 0, 0 coordinates - left bottom corner
    m = mesh.Medium3D(problem_w, problem_w, problem_h + dd, hx, hx, hz)

    m.add_shape(2, mesh.Cube(0, 0, 0, problem_w, problem_w, problem_h))
    m.add_shape(1, mesh.Cube(0, 0, z1, problem_w, problem_w, z2))
    m.add_shape(0, mesh.Cube(0, 0, z1 + z2, problem_w, problem_w, z3))
    
    m.add_shape(3, mesh.Cube(0, 0, z1 + z2 + z3, problem_w, problem_w, dd))
    
    if enable_beton:
        m.add_shape(4, mesh.Cube((problem_w - beton_w)/2, (problem_w - beton_w)/2, problem_h - dd - beton_l, beton_w, beton_w, beton_l)) # BETON

    m.write("1.mesh")


def setup_initial_temp():
    d = data.Medium3D(problem_w, problem_w, problem_h + dd, hx, hx, hz)
    
    up_depth = merz_depth + dd
    
    d.add_shape(data.Cube(0, 0, 0, problem_w, problem_w, problem_h + dd, down_temp))  # Многолетняя мерзлота
    d.add_shape(data.CubeGradZ(0, 0, problem_h - dd - merz_depth, problem_w, problem_w, merz_depth, up_temp, down_temp))
    d.add_shape(data.Cube(0, 0, problem_h - dd, problem_w, problem_w, dd, up_temp)) # dd

    if enable_beton:
        d.add_shape(data.Cube((problem_w - beton_w)/2, (problem_w - beton_w)/2, problem_h - dd - beton_l, beton_w, beton_w, beton_l, up_temp)) # BETON


    d.write("1.dat")


def compute():
    ui.notice("Execution of stefan_enthalpy started", show_time=True)
    subprocess.call(".\\stefan_enthalpy.exe 1.xml", shell=True)
    ui.notice("Execution of stefan_enthalpy finished", show_time=True)


if __name__ == "__main__":
    ui.notice("Task started", show_time=True)
    setup_initial_mesh()
    setup_xml()
    setup_initial_temp()
    compute()