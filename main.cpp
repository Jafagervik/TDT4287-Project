#include <iostream>
#include <vector>
#include "./include/SuffixTree.hpp"
#include <stdint.h>
#include <string>

std::vector<std::uint16_t> suffix_lengths;
//map[suffix_lengths[i]]++;
// read to file
// visualize in python



// Test functionality main.
int main(){
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

