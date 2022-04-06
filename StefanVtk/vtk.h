#ifndef VTK_IMG_CONSTRUCT__VTK_H_
#define VTK_IMG_CONSTRUCT__VTK_H_

#include <iostream>
#include <fstream>
#include <vector>

#include "ui.h"

struct Vertex {
  // Mesh
  int material;
  // VTK data
  double temp, enthalpy, conductivity;
  bool state;
};

class Data {
 public:
  std::vector<Vertex> v_;
  size_t dim_x, dim_y, dim_z;
  double scale_x, scale_y, scale_z;

  size_t VectorMapping(size_t i_z, size_t i_y, size_t i_x) const {
    return i_z * dim_x * dim_y + i_y * dim_x + i_x;
  }

  Data(const std::string &vtk_path, const std::string &mesh_path);
};

#endif //VTK_IMG_CONSTRUCT__VTK_H_
