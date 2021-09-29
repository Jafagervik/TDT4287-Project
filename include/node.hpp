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
    std::pair<uint16_t, uint16_t> label;
    uint16_t leafindex;
    std::vector<Node *> children;
    Node *parent;
    Node(NodeType t, uint16_t from, uint16_t to) : type(t), label(from, to), parent(nullptr) {}
};