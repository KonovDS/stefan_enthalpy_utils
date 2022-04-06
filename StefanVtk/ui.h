#ifndef IMPLICITSTEFANPROBLEMMPI__UI_H_
#define IMPLICITSTEFANPROBLEMMPI__UI_H_

#include <iostream>

namespace ui {

class ProgressBar {
  std::ostream &out_;
  int total_len, pos, symbol_len;
  double scale;
  bool finished;
  void Update();
 public:
  void Restart(int total, int actual_length = 50);
  ProgressBar(int total, int actual_length = 50, std::ostream &out = std::cout);
  void Increase(int val = 1);
  void Finish();
  ~ProgressBar();
};

// Displays [ERROR] Message
void Error(const std::string &text, std::ostream &out = std::cout);
// Displays [NOTICE] Message
void Notice(const std::string &text, std::ostream &out = std::cout);
// Displays [DEBUG] Message
void Debug(const std::string &text, std::ostream &out = std::cout);

} // namespace ui

#endif //IMPLICITSTEFANPROBLEMMPI__UI_H_
