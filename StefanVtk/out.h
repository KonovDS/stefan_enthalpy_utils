#ifndef VTK_IMG_CONSTRUCT__OUT_H_
#define VTK_IMG_CONSTRUCT__OUT_H_

#include <string>

#include "vtk.h"

void VtkOut3D(const Data &d,
              const std::string &path,
              double (*f)(const Vertex&, size_t i_x, size_t i_y, size_t i_z),
              const std::string &data_name = std::string("data"),
              const std::string &description = std::string("converted stefan points"));

void PltOut2D(const Data &d,
              const std::string &path,
              double (*f)(const Vertex&, size_t i_x, size_t i_y, size_t i_z),
              size_t x,
              size_t y = 0);

#endif //VTK_IMG_CONSTRUCT__OUT_H_
