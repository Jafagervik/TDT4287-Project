#include <stdint.h>

#include <iostream>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

#include "./filehandling.hpp"
#include "./node.hpp"

// I instantly regretted doing this object oriented. we want speed

class SuffixTree {
    // Private member variabels
   private:
    Node *root;     // root of the tree
    uint16_t *end;  // lenght of string T we're building tree for

    // Public member variabels
   public:
    // Private member methods
    // std::vector<uint16_t> suffixes; suffixes::max();
    uint16_t max_suffix;

   private:
    // Public member methods
   public:
    SuffixTree(std::string T) {}
    Node *build_suffix_tree();
};
