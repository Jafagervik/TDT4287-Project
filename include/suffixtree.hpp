#ifndef SuffixTree_H  // Guard
#define SuffixTree_H

#include <stdint.h>

#include <iostream>
#include <string>
#include <string_view>
#include <unordered_map>
#include <utility>
#include <vector>

#include "./filehandling.hpp"
#include "./node.hpp"

uint16_t leaf_end = -1;

class SuffixTree {
   private:
    std::string T;
    Node *last_new_node;
    Node *active_node;

    uint16_t *active_edge;
    uint16_t active_length;
    uint16_t remaining_suffix_count;
    uint16_t *root_end;
    uint16_t *split_end;
    uint16_t size;
    Node *root;

   public:  // public member methods.
    SuffixTree(std::string &T) : T(T) {}
    ~SuffixTree();
    bool traverse(Node *current_node);
    uint16_t max_suffix(const std::string &a);
    uint16_t edge_length(const Node *node) {
        return node->start - *node->end;
    };
    Node *new_node(uint16_t from, uint16_t *to, NodeType is_leaf);
    void extend_tree(uint16_t pos);
    char walk_dfs(Node *current);
    void build_tree();

    std::string::iterator it;

    // TODO: Maybe add some printing
};

#endif