#include <iostream>

#include "ui.h"
#include "vtk.h"
#include "out.h"

int main() {
  std::vector<std::string> vtks = {
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s00000.vtk",
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s32500.vtk",
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s65000.vtk",
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s97500.vtk",
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s130000.vtk",
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s162500.vtk",
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s195000.vtk",
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s227500.vtk",
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s260000.vtk",
      };
  std::vector<std::string> vtkds = {
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s00000.vtkd",
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s32500.vtkd",
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s65000.vtkd",
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s97500.vtkd",
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s130000.vtkd",
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s162500.vtkd",
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s195000.vtkd",
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s227500.vtkd",
      "E:\\comp_phys\\merz\\compute\\nn_3d_1\\results\\test\\s260000.vtkd",
      };
  std::string mesh_path = "E:\\comp_phys\\merz\\compute\\nn_3d_1\\1.mesh";

  for (int i = 0; i < vtks.size(); i++) {
    Data d(vtks[i], mesh_path);
    PltOut2D(d, vtkds[i], [](auto x, auto i_x, auto i_y, auto i_z) {
      return x.temp;
      }, 2);
  }

  /*
  VtkOut3D(d, out_path, [](auto x, auto i_x, auto i_y, auto i_z) {
    if (x.material == 4) {
      return double(2);
    }
    if (x.material == 3) {
      if (i_z > 200) {
        return double(1);
      }
    }
    return double(int(x.state));
  });
*/

  return 0;
}
