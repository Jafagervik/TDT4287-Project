#ifndef SuffixTree_H // Guard
#define SuffixTree_H

#include <iostream>
#include <string>
#include <string_view>
#include <vector>
#include <stdint.h>
#include <utility>

#include "./filehandling.hpp"
#include "./node.hpp"

// I instantly regretted doing this object oriented. we want speed
class SuffixTree
{
public: // public member methods.
    Node *root;
    uint16_t *end; // lenght of string T we're building tree for
    SuffixTree();
    ~SuffixTree();
    uint16_t max_suffix(std::string a);
    void build_tree(std::string s);
};

#endif