#include <iostream>
#include <fstream>
#include <string>
#include <string_view>
#include <vector>
#include <stdint.h>
#include <unordered_map>

std::vector<std::string> read_file(const std::string &filename);
void write_file(const std::string &filename, std::vector<uint16_t> seqs);
