#include <string>
#include <utility>
#include <stdint.h>
#include <vector>

enum class NodeType
{
    ROOT = 0,
    INTERNAL = 1,
    LEAF = 2
};

struct Node
{
    NodeType type;
    uint16_t from;
    uint16_t *to;
    uint16_t leaf_index;
    Node * suffix_link;
    std::vector<Node *> children;
    Node *parent;
    // Root constructor
    Node(NodeType t, uint16_t from, uint16_t *to) : type(t), parent(nullptr), suffix_link(nullptr) {
        this->from= from;
        this->to = to;
    }

};