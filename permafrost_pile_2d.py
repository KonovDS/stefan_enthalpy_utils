import stefan_enthalpy_utils.xml_generator as xml
import stefan_enthalpy_utils.data_generator_2d as data
import stefan_enthalpy_utils.mesh_generator_2d as mesh
import stefan_enthalpy_utils.ui as ui
import stefan_enthalpy_utils.vtk_to_data_2d as vtk

import shutil
import os
import subprocess


# -----------------
# - SETUP 2D TASK -
# -----------------

problem_w = 10
problem_h = 20

hx = 0.02
hz = 0.02 # ALSO CHANGE IN VTK TO DATA!

tau = 50
steps = 51840 # 30 days
steps_vtk = 17280 # 10 days
months = 12
up = [20,   15,   6,  -7,   -26,  -37, -37, -32.9, -19, -4, 8, 17]

z1 = 14
z2 = 4
z3 = 2

dd = hx * 3

merz_depth = 6
down_temp = -4

beton_w = 0.3
beton_l = 14

enable_beton = True

# -----------------
# -               -
# -----------------


def setup_xml(up_temp):
    t = xml.Task(2, "1.mesh")
    
    up_layer = xml.Material(1000, 2.56, 3150, 1000, 2.73, 2350, 0, 71957)
    middle_layer = xml.Material(1000, 1.51, 3150, 1000, 1.7, 2350, 0, 71957)
    down_layer = xml.Material(1000, 1.51, 2010, 1000, 1.86, 1670, 0, 60437)
    
    if enable_beton:
        beton = xml.Material(1000, 9.04, 3000, 1000, 9.04, 3000, 100, 0)
    
    t.add_material(0, up_layer)
    t.add_material(1, middle_layer)
    t.add_material(2, down_layer)
    
    t.add_material(3, up_layer)
    t.add_effect(3, xml.Effect('fixed', (str(up_temp), )))
    
    if enable_beton:
        t.add_material(4, beton)
    
    t.add_boundary("x", "up", xml.Boundary("const_flux", (0, )))
    t.add_boundary("x", "down", xml.Boundary("const_flux", (0, )))
    t.add_boundary("y", "up", xml.Boundary("const_flux", (0, )))
    t.add_boundary("y", "down", xml.Boundary("const_flux", (0, )))
    t.add_boundary("z", "up", xml.Boundary("const_flux", (0, )))
    t.add_boundary("z", "down", xml.Boundary("const_flux", (0, )))

    t.set_inistate_pernode("init.dat")

    t.set_time(steps + 1, tau)
    t.set_vtk_period(steps_vtk)

    t.write("1.xml")

def setup_initial_mesh():
    # 0, 0 coordinates - left bottom corner
    m = mesh.Medium2D(problem_w, problem_h + dd, hx, hz)

    m.add_shape(2, mesh.Rect(0, 0, problem_w, problem_h))
    m.add_shape(1, mesh.Rect(0, z1, problem_w, z2))
    m.add_shape(0, mesh.Rect(0, z1 + z2, problem_w, z3))
    
    m.add_shape(3, mesh.Rect(0, z1 + z2 + z3, problem_w, dd))
    
    if enable_beton:
        m.add_shape(4, mesh.Rect((problem_w - beton_w)/2, problem_h - dd - beton_l, beton_w, beton_l))

    m.write("1.mesh")


def setup_initial_temp(up_temp):
    d = data.Medium2D(problem_w, problem_h + dd, hx, hz)
    
    up_depth = merz_depth + dd
    
    d.add_shape(data.Rect(0, 0, problem_w, problem_h + dd, down_temp))  # Многолетняя мерзлота
    d.add_shape(data.RectGradZ(0, problem_h - dd - merz_depth, problem_w, merz_depth, up_temp, down_temp))
    d.add_shape(data.Rect(0, problem_h - dd, problem_w, dd, up_temp)) # dd

    if enable_beton:
        d.add_shape(data.Rect((problem_w - beton_w)/2, problem_h - dd - beton_l, beton_w, beton_l, up_temp)) # BETON

    d.write("init.dat")

def compute(res_name):
    ui.notice("Execution of stefan_enthalpy started", show_time=True)
    subprocess.call(".\\stefan_enthalpy.exe 1.xml", shell=True)
    ui.notice("Execution of stefan_enthalpy finished", show_time=True)
    os.mkdir(".\\res\\" + res_name)
    for f in os.listdir(".\\out"):
        os.rename(".\\out\\" + f, ".\\res\\" + res_name + "\\" + f)

if __name__ == "__main__":
    ui.notice("Task started", show_time=True)
    name = "compute"
    
    setup_initial_mesh()
    setup_xml(up[0])
    setup_initial_temp(up[0])
    compute(name + '_' + str(0))
    
    os.remove("init.dat")
    ui.notice("Computations of " + '0' + " finished.")
    
    for i in range(1, months):
        ui.notice("Using i=" + str(i-1) + " data to compute.")
        shutil.copy('./res/' + name + '_' + str(i-1) + '/s' + str(steps) + '.vtk', './init.vtk')
        vtk.vtk_to_data("init.vtk", "init.dat", [1, 1], (501, 1004))
        setup_xml(up[i])
        compute(name + '_' + str(i))
        os.remove("init.vtk")
        os.remove("init.dat")
        ui.notice("Computations of " + str(i) + " finished.")
    
    compute()