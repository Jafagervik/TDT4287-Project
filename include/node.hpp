#include <stdint.h>

#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

static uint16_t leaf_end = -1;

enum class NodeType {
    ROOT = 0,
    INTERNAL = 1,
    LEAF = 2
};

struct Node {
    NodeType type;

    uint16_t start;
    uint16_t *end;
    Node *suffix_link;
    uint16_t suffix_index;
    std::unordered_map<char, Node *>
        children;
    Node *parent;

};