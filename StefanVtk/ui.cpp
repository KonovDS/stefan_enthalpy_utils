#include "ui.h"

#include <iostream>

namespace ui {

void ProgressBar::Update() {
  out_ << "[";
  int new_pos = int(scale * pos);
  for (int i = 0; i < symbol_len; i++) {
    if (i < new_pos) {
      out_ << "=";
    } else if (i == new_pos) {
      out_ << ">";
    } else {
      out_ << " ";
    }
  }
  out_ << "] (" << pos << " / " << total_len << ") \r";
  out_.flush();
}

ProgressBar::ProgressBar(int total,
                         int actual_length,
                         std::ostream &out) :
                         out_(out)
                         {
  total_len = total;
  symbol_len = actual_length;
  pos = 0;
  finished = false;
  scale = double(symbol_len) / total_len;
  Update();
}

void ProgressBar::Restart(int total, int actual_length) {
  if (!finished) {
    if (pos < total_len) {
      Finish();
    }
  }
  total_len = total;
  symbol_len = actual_length;
  pos = 0;
  finished = false;
  scale = double(symbol_len) / total_len;
  Update();
}

void ProgressBar::Increase(int val) {
  pos += val;
  Update();
  if (pos == total_len)
    Finish();
}

void ProgressBar::Finish() {
  finished = true;
  out_ << "\n";
}

ProgressBar::~ProgressBar() {
  if (!finished) {
    if (pos < total_len) {
      Finish();
    }
  }
}

void Error(const std::string &text, std::ostream &out) {
  out << "[ERROR]  " << text << std::endl;
}

void Notice(const std::string &text, std::ostream &out) {
  out << "[NOTICE] " << text << std::endl;
}

void Debug(const std::string &text, std::ostream &out) {
  out << "[DEBUG]  " << text << std::endl;
}

} // namespace ui

