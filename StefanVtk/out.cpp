#include "out.h"

// Заполнение заголовка VTK
inline void WriteHeadVTK(std::ofstream &f,
                         size_t x, size_t y, size_t z,
                         double scale_x, double scale_y, double scale_z,
                         const std::string &data_name,
                         const std::string &description) {
  f << "# vtk DataFile Version 3.0\n";
  f << description << "\n";
  f << "ASCII\n";
  f << "\n";
  f << "DATASET STRUCTURED_POINTS\n";
  f << "DIMENSIONS " << x << " " << y << " " << z << "\n";
  f << "ORIGIN 0 0 0\n";
  f << "SPACING " << scale_x << " " << scale_y << " " << scale_z << "\n";
  f << "\n";
  f << "POINT_DATA " << x * y * z << "\n";
  f << "SCALARS " << data_name << " FLOAT\n";
  f << "LOOKUP_TABLE default\n";
}

void VtkOut3D(const Data &d,
              const std::string &path,
              double (*f)(const Vertex&, size_t i_x, size_t i_y, size_t i_z),
              const std::string &data_name,
              const std::string &description) {
  std::ofstream out;
  out.open(path);
  if (!out.is_open()) {
    std::cout << "[ERROR] Unable to open file \"" << path << "\"" << std::endl;
    exit(-1);
  }

  WriteHeadVTK(out, d.dim_x, d.dim_y, d.dim_z, d.scale_x, d.scale_y, d.scale_z, data_name, description);

  for (int i_z = 0; i_z < d.dim_z; i_z++) {
    for (int i_y = 0; i_y < d.dim_y; i_y++) {
      for (int i_x = 0; i_x < d.dim_x; i_x++) {
        auto i = d.VectorMapping(i_z, i_y, i_x);
        out << f(d.v_[i], i_x, i_y, i_z) << "\n";
      }
    }
  }

  out.close();
}

void PltOut2D(const Data &d,
              const std::string &path,
              double (*f)(const Vertex&, size_t i_x, size_t i_y, size_t i_z),
              size_t x,
              size_t y) {
  std::ofstream out;
  out.open(path);
  if (!out.is_open()) {
    std::cout << "[ERROR] Unable to open file \"" << path << "\"" << std::endl;
    exit(-1);
  }

  for (int i_z = 0; i_z < d.dim_z; i_z++) {
    for (int i_y = 0; i_y < d.dim_y; i_y++) {
      for (int i_x = 0; i_x < d.dim_x; i_x++) {
        if((i_x == x || x == 0) && (i_y == y || y == 0)) {
          auto i = d.VectorMapping(i_z, i_y, i_x);
          out << f(d.v_[i], i_x, i_y, i_z) << " ";
        }
      }
    }
    out << "\n";
  }

  out.close();
}
