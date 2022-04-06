cmake_minimum_required(VERSION 3.20)
project(vtk_img_construct)

set(CMAKE_CXX_STANDARD 17)

add_executable(vtk_img_construct main.cpp vtk.cpp vtk.h ui.h ui.cpp out.cpp out.h)
