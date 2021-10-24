// StefanToRect by Konov D.S. oct 2021
// Converts from Stefan vtk data and mesh to rect
// TODO: ADD SUPPORT TO STRIDES != 1

#include <vector>
#include <fstream>
#include <string>
#include <iostream>

// Заполнение заголовка VTK
const char *kDefaultHeader1 = "# vtk DataFile Version 3.0\nConverted stefan points\nASCII\n\nDATASET POLYDATA\nPOINTS ";
const char *kDefaultHeader2 = " float\n";
void WriteHeadVTK(std::ofstream &f, int num_of_points) {
  f << kDefaultHeader1 << num_of_points << kDefaultHeader2;
}

struct PointVTK2D {
  double x, z;
};

std::ostream &operator<< (std::ostream &s, const PointVTK2D &p) {
  // Дефолтное значение y для VTK файлов принимаем 0
  return s << p.x << " " << 0 << " " << p.z << "\n";
}

struct Vertex {
  double x, z, temp;
  int material;
};

class Data {
  std::vector<Vertex> v;
 public:
  Data(const std::string &vtk_path, const std::string &mesh_path) {
    std::ifstream vtk, mesh;
    vtk.open(vtk_path);
    if (!vtk.is_open()) {
      std::cout << "[ERROR] Unable to open vtk file \"" << vtk_path << "\"" << std::endl;
      exit(-1);
    }
    mesh.open(mesh_path);
    if (!mesh.is_open()) {
      std::cout << "[ERROR] Unable to open mesh file \"" << mesh_path << "\"" << std::endl;
      exit(-1);
    }
    std::cout << "[NOTICE] Successfully opened files to read" << std::endl;

    // Конфигурация ледового острова и его форма
    int dim_x, dim_z;
    double scale_x, scale_z;
    mesh >> dim_x >> dim_z >> scale_x >> scale_z;
    scale_x /= dim_x;
    scale_z /= dim_z;

    // Двигаемся по vtk до температуры:
    std::string line;
    while(!vtk.eof()) {
      std::getline(vtk, line);
      if(line == "SCALARS T FLOAT")
        break;
    }
    std::cout << "[DEBUG] Found \"" << line << "\". ";
    std::getline(vtk, line);
    std::cout << "Next string is \"" << line << "\"" << std::endl;
    v = std::vector<Vertex>(dim_x * dim_z);

    std::cout << "[DEBUG] Starting reading " << dim_x << "*" << dim_z << " consequent values" << std::endl;
    for (int i_z = 0; i_z < dim_z; i_z++) {
      for (int i_x = 0; i_x < dim_x; i_x++) {
        if (vtk.eof() || mesh.eof()) {
          std::cout << "[ERROR] Unexpected EOF. Exiting" << std::endl;
          vtk.close();
          mesh.close();
          exit(-1);
        }
        v[i_z*dim_x+ i_x].x = scale_x * i_x;
        v[i_z*dim_x + i_x].z = scale_z * i_z;
        vtk >> v[i_z*dim_x + i_x].temp;
        mesh >> v[i_z*dim_x + i_x].material;
      }
    }

    std::getline(vtk, line); // Пропускаем пробельные символы в конце строки
    std::getline(vtk, line); // И читаем следующую строку после данных
    if (line == "SCALARS K FLOAT") {
      std::cout << "[NOTICE] Correctly read VTK file." << std::endl;
    } else {
      std::cout << "[WARNING] Unexpected line \"" << line << "\" at VTK file. Data may be incorrect" << std::endl;
    }
    std::getline(mesh, line); // Пропускаем пробельные символы в конце строки
    std::getline(mesh, line); // Читаем ничего
    std::cout << "[DEBUG] Last line of MESH file \"" << line << "\"" << std::endl;
    vtk.close();
    mesh.close();
  }

  void Output(const std::string &vtk_path, const std::string &temp_path, bool (*f)(const Vertex&)) const {
    std::ofstream out;
    std::vector<PointVTK2D> points;
    points.reserve(v.size());
    out.open(temp_path);
    if (!out.is_open()) {
      std::cout << "[ERROR] Unable to open file \"" << temp_path << "\"" << std::endl;
      exit(-1);
    }

    int num_points = 0;
    for(const auto &i : v) {
      if(f(i)) {
        points.push_back({i.x, i.z});
        out << i.temp << " ";
        num_points++;
      }
    }
    out.close();

    // Далее в файл VTK
    out.open(vtk_path);
    if (!out.is_open()) {
      std::cout << "[ERROR] Unable to open file \"" << vtk_path << "\" to write" << std::endl;
      exit(-1);
    }
    WriteHeadVTK(out, num_points);
    for(const auto &i : points) {
      out << i;
    }
    out.close();
    std::cout << "[NOTICE] Successfully wrote " << num_points << " point data" << std::endl;
  }

  void Offset(double x, double z) {
    for(auto &i : v) {
      i.x += x;
      i.z += z;
    }
  }
};

int main() {
  Data d("s.vtk", "m.mesh");
  d.Offset(0, -10); // Остров находится на донном грунте. Убираем его
  d.Output("ice.vtk", "ice.txt", [](auto v) { return (v.material == 4 || v.material == 1) && v.temp < 0; });
  d.Output("water.vtk", "water.txt", [](auto v) { return (v.material == 4 && v.temp >= 0) || v.material == 0; });
  return 0;
}