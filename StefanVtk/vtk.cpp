#include "vtk.h"

#include <iostream>
#include <fstream>

Data::Data(const std::string &vtk_path, const std::string &mesh_path) {
  std::ifstream vtk, mesh;
  vtk.open(vtk_path);
  if (!vtk.is_open()) {
    ui::Error("Unable to open vtk file \"" + vtk_path + "\"");
    exit(-1);
  }
  mesh.open(mesh_path);
  if (!mesh.is_open()) {
    ui::Error("Unable to open mesh file \"" + mesh_path + "\"");
    exit(-1);
  }
  ui::Notice("Successfully opened files to read");

  mesh >> dim_x >> dim_y >> dim_z >> scale_x >> scale_y >> scale_z;
  scale_x /= double(dim_x - 1);
  scale_y /= double(dim_y - 1);
  scale_z /= double(dim_z - 1);

  std::string line;
  // Двигаемся по vtk до температуры:
  while(!vtk.eof()) {
    std::getline(vtk, line);
    if(line == "DATASET STRUCTURED_POINTS")
      break;
  }
  int dim_x2, dim_y2, dim_z2;
  vtk >> line >> dim_x2 >> dim_y2 >> dim_z2;
  if (dim_x != dim_x2 || dim_y != dim_y2 || dim_z != dim_z2) {
    ui::Error("Dimensions of VTK and mesh are different");
  }

  while(!vtk.eof()) {
    std::getline(vtk, line);
    if(line == "SCALARS E FLOAT")
      break;
  }
  std::getline(vtk, line);

  try {
    v_ = std::vector<Vertex>(dim_x * dim_y * dim_z);
  } catch(...) {
    ui::Error("Could not allocate " + std::to_string(dim_x * dim_y * dim_z) + " data points");
    exit(-1);
  }

  ui::Notice("Reading enthalpy data...");
  //ui::ProgressBar p(dim_z);
  for (int i_z = 0; i_z < dim_z; i_z++) {
    for (int i_y = 0; i_y < dim_y; i_y++) {
      for (int i_x = 0; i_x < dim_x; i_x++) {
        if (vtk.eof() || mesh.eof()) {
          ui::Error("Unexpected EOF. Exiting");
          vtk.close();
          mesh.close();
          exit(-1);
        }
        auto i = VectorMapping(i_z, i_y, i_x);
        vtk >> v_[i].enthalpy;
        mesh >> v_[i].material;
      }
    }
    //p.Increase();
  }
  //p.Finish();

  while(!vtk.eof()) {
    std::getline(vtk, line);
    if(line == "SCALARS T FLOAT")
      break;
  }
  std::getline(vtk, line);

  ui::Notice("Reading temperature data...");
  //p.Restart(dim_z);
  for (int i_z = 0; i_z < dim_z; i_z++) {
    for (int i_y = 0; i_y < dim_y; i_y++) {
      for (int i_x = 0; i_x < dim_x; i_x++) {
        if (vtk.eof() || mesh.eof()) {
          ui::Error("Unexpected EOF. Exiting");
          vtk.close();
          mesh.close();
          exit(-1);
        }
        auto i = VectorMapping(i_z, i_y, i_x);
        vtk >> v_[i].temp;
      }
    }
    //p.Increase();
  }
  //p.Finish();

  while(!vtk.eof()) {
    std::getline(vtk, line);
    if(line == "SCALARS K FLOAT")
      break;
  }
  std::getline(vtk, line);

  ui::Notice("Reading conductivity data...");
  //p.Restart(dim_z);
  for (int i_z = 0; i_z < dim_z; i_z++) {
    for (int i_y = 0; i_y < dim_y; i_y++) {
      for (int i_x = 0; i_x < dim_x; i_x++) {
        if (vtk.eof() || mesh.eof()) {
          ui::Error("Unexpected EOF. Exiting");
          vtk.close();
          mesh.close();
          exit(-1);
        }
        auto i = VectorMapping(i_z, i_y, i_x);
        vtk >> v_[i].conductivity;
      }
    }
    //p.Increase();
  }
  //p.Finish();

  while(!vtk.eof()) {
    std::getline(vtk, line);
    if(line == "SCALARS state FLOAT")
      break;
  }
  std::getline(vtk, line);

  ui::Notice("Reading state data...");
  //p.Restart(dim_z);
  for (int i_z = 0; i_z < dim_z; i_z++) {
    for (int i_y = 0; i_y < dim_y; i_y++) {
      for (int i_x = 0; i_x < dim_x; i_x++) {
        if (vtk.eof() || mesh.eof()) {
          std::cout << "[ERROR] Unexpected EOF. Exiting" << std::endl;
          vtk.close();
          mesh.close();
          exit(-1);
        }
        auto i = VectorMapping(i_z, i_y, i_x);
        vtk >> v_[i].state;
      }
    }
    //p.Increase();
  }
  //p.Finish();

  std::getline(mesh, line); // Пропускаем пробельные символы в конце строки
  std::getline(mesh, line); // Читаем ничего
  ui::Debug("Last line of mesh file \"" + line + "\"");
  mesh.close();

  std::getline(vtk, line); // Пропускаем пробельные символы в конце строки
  std::getline(vtk, line); // Читаем ничего
  ui::Debug("Last line of VTK file \"" + line + "\"");
  vtk.close();
}