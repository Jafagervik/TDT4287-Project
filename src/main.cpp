#include <cstdlib>
#include <iostream>

#include "./include/SuffixTree.hpp"

static constexpr auto a = "TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG";

std::vector<std::uint16_t> suffix_lengths;

int main(int argc, char* argv[]) {
    SuffixTree tree;
    // Must be called with 1 and only 1 parameter.
    if (argc != 2) {
        std::cout << "usage: suffixtree inputstring" << std::endl;
        exit(1);
    } else {
        tree.construct(argv[1]);
        std::cout << tree.log_tree() << std::endl;
    }
}