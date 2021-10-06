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

uint16_t SuffixTree::edge_length(const Node *node) { return *node->to - node->from; }

/**
 * @brief We use Skip/Count for this one
 * 
 * @param current_node 
 * @return true if active_length >= length
 * @return false otherwise 
 */
bool SuffixTree::traverse(Node *current_node) {
    uint16_t length = edge_length(current_node);
    if (active_length >= length) {
        active_edge += length;
        active_length -= length;
        active_node = current_node;
        return true;
    }
    return false;
}

/**
 * @brief Add a new node to thbe suffix tree.
 * 
 * @param from 
 * @param to 
 * @param is_leaf 
 * @return Node* 
 */
Node *SuffixTree::new_node(uint16_t from, uint16_t *to, NodeType is_leaf) {
    Node *node = new Node(from, to, NodeType::LEAF);

    node->suffix_link = root;
    node->from = from;
    node->to = to;

    node->suffix_index = -1;
    return node;
}

/**
 * @brief The Big Ukkonen, https://www.youtube.com/watch?v=ByuMPBfyR5g&t=0s
 * 
 * @param pos 
 */
void SuffixTree::extend_tree(uint16_t pos) {
    leaf_end = pos;

    remaining_suffix_count += 1;

    last_new_node = nullptr;

    while (remaining_suffix_count > 0) {
        if (active_length == 0)
            active_edge = pos;

        // TODO: instead of vector, store in unordered_map
        if (!active_node->children[T[active_edge]]) {
            active_node->children[T[active_edge]] = new_node(pos, pos, NodeType::LEAF);
            if (last_new_node) {
                last_new_node->suffix_link = active_node;
                last_new_node = nullptr;
            }
        } else {
            Node *next = active_node->children[T[active_edge]];
            if (traverse(next))
                continue;
            if (T[next->from + active_length] == T[pos]) {
                if (last_new_node && active_node != root) {
                    last_new_node->suffix_link = active_node;
                    last_new_node = nullptr;
                }
                active_length += 1;
                break;
            }
            split_end = next->from + active_length - 1;
            Node *split = new Node(pos, pos, NodeType::LEAF);
            split->children[T[pos]] = new_node(pos, pos, NodeType::LEAF);
            next->from += active_length;
            split->children[T[next->from]] = next;

            if (last_new_node) {
                last_new_node->suffix_link = split;
            }
            last_new_node = split;
        }
        remaining_suffix_count -= 1;
        if (active_node == root && active_length) {
            active_length -= 1;
            active_edge = pos - remaining_suffix_count + 1;
        } else if (active_node != root)
            active_node = active_node->suffix_link;
    }
}

/**
 * @brief walk down the tree in a dfs manner one node at a time
 * 
 * @param current 
 * @return Node* 
 */
Node *SuffixTree::walk_dfs(Node *current) {
    // TODO: See what to do instead of yielding
    uint16_t start = current->from;
    uint16_t end = *current->to;

    for (uint16_t i = start; i < end + 1; ++i) {
        T[i];
    }

    for (Node *node : current->children) {
        walk_dfs(node);
    }
}

/**
 * @brief Build the tree initially
 * 
 */
void SuffixTree::build_tree() {
    size = T.size();

    *root_end = -1;
    root = new_node(-1, root_end, NodeType::INTERNAL);
    active_node = root;
    for (int i = 0; i < T.size(); ++i)
        extend_tree(i);
}