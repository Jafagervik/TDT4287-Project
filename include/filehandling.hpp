#include <stdint.h>

#include <fstream>
#include <iostream>
#include <string>
#include <string_view>
#include <unordered_map>
#include <vector>

std::vector<std::string> read_file(const std::string &filename);
std::unordered_map<uint16_t, uint16_t> vec_to_dict(std::vector<uint16_t> seqs);

void write_dists_to_file(const std::string &filename, std::vector<uint16_t> seqs);
