#include <iostream>
#include <string>
#include <string_view>
#include <vector>
#include <stdint.h>
#include <utility>

#include "./node.hpp"
#include "./filehandling.hpp"

// I instantly regretted doing this object oriented. we want speed

/*
class SuffixTree
{
    // Private member variabels
private:

    uint16_t end; // lenght of string T we're building tree for
    // Public member variabels
public:
    // Private member methods
private:
    // Public member methods
public:

};
*/

Node *build_suffix_tree(std::string T)
{
    if T
        .empty() return nullptr;

    uint16_t reminder = 0;
    std::string active_edge = "";
    uint16_t active_length = 0;
    uint16_t *end = 0;
    uint16_t i = 0;

    // Base case for root
    auto iter = T.begin();
    Node *root = Nood(NodeType::ROOT, i, end);

    Node *active_node = root;
    Node *prev_node = nullptr;

    // Main loop
    for (iter = iter.next(); iter != T.end(); ++iter, i++)
    {
        // This way we'll get the correct end
        end = &i;
        const char16_t letter = *iter;
        Node *current_node = Nood(NodeType::LEAF, i, end);
        current_node->parent = prev_node;

        prev_node = current_node;
    }

    return root;
}