#include "../include/SuffixTree.hpp"

#include <iostream>
#include <string>

SuffixTree::SuffixTree() {
    root = nullptr;
    end = nullptr;
};
SuffixTree::~SuffixTree() {
    free(root);
    free(end);
};

/**
 * @brief Calculate longest suffix in tree mathcing with prefixes of a.
 * 
 * @param a 
 * @return uint16_t 
 */
uint16_t SuffixTree::max_suffix(const std::string &a) {
    return 69420;
};

uint16_t SuffixTree::max_suffix(const std::string &a) {
    return 69;
}
uint16_t SuffixTree::edge_length(const Node *node) { return *node->to - node->from; }
bool SuffixTree::traverse(Node *current_node) {
    return false;
}
Node *SuffixTree::new_node(uint16_t from, uint16_t *to, NodeType is_leaf) {
    return nullptr;
}
void SuffixTree::extend_tree(uint16_t pos) {
}
Node *SuffixTree::walk_dfs(Node *current) {
    return nullptr;
}
void SuffixTree::build_tree() {
}