#include <stdint.h>

#include <algorithm>
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

using matrix = std::vector<std::vector<uint16_t>>;

auto edit_distance(const std::string &S, const std::string &P);
void backtrack(matrix &M);
bool allow_mismatch(const float &mismatch_percentage);