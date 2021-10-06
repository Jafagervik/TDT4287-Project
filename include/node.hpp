#include <stdint.h>

#include <string>
#include <utility>
#include <vector>

enum class NodeType {
    ROOT = 0,
    INTERNAL = 1,
    LEAF = 2
};

struct Node {
    NodeType type;
    std::pair<uint16_t, uint16_t> label;
    uint16_t from;
    uint16_t *to;
    uint16_t leaf_index;
    Node *suffix_link;
    std::vector<Node *> children;
    Node *parent;
    Node(NodeType t, uint16_t from, uint16_t *to) : type(t), label(from, *to), parent(nullptr) {}
    // Root constructor
    Node(NodeType t, uint16_t from, uint16_t *to) : type(t), parent(nullptr), suffix_link(nullptr) {
        this->from = from;
        this->to = to;
    }
};