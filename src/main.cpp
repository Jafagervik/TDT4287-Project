#include <stdint.h>

#include <iostream>
#include <string>
#include <vector>

#include "./include/SuffixTree.hpp"

static constexpr auto a = "TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG";

std::vector<std::uint16_t> suffix_lengths;

// Test functionality main.
int main() {
    std::cout << "Hello world!\n";
    // read file
    std::string s = "catcgcat";
    // for each line build tree
    SuffixTree myTree;
    myTree.build_tree(s);

    // update vector from tree:
    // free end of suffixTree.
    // repeat.
    return 0;
}