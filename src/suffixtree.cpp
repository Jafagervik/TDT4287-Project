#include "../include/SuffixTree.hpp"

#include <iostream>
#include <string>

SuffixTree::~SuffixTree() {
    delete last_new_node;
    delete active_edge;
    delete active_node;
    delete root;
    delete root_end;
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

uint16_t SuffixTree::edge_length(const Node *node) { return *node->end - node->start; }

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
        *active_edge += length;
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
Node *SuffixTree::new_node(uint16_t from, uint16_t *to = nullptr, NodeType leaf = NodeType::LEAF) {
    // TODO: maybe insert parent here?
    Node *node = new Node();

    node->suffix_link = root;
    node->start = from;
    node->end = to;

    node->suffix_index = -1;
    return node;
}

/**
 * @brief The Big Ukkonen, https://www.youtube.com/watch?v=ByuMPBfyR5g&t=0s
 * 
 * @param pos 
 */
void SuffixTree::extend_tree(uint16_t pos) {
    // Setting global static variable
    leaf_end = pos;

    remaining_suffix_count += 1;

    last_new_node = nullptr;

    while (remaining_suffix_count > 0) {
        if (active_length == 0)
            *active_edge = pos;

        // TODO: instead of vector, store in unordered_map
        if (active_node->children[T[*active_edge]]) {
            active_node->children[T[*active_edge]] = new_node(pos, (uint16_t *)pos, NodeType::LEAF);
            if (last_new_node != nullptr) {
                last_new_node->suffix_link = active_node;
                last_new_node = nullptr;
            }
        } else {
            Node *next = active_node->children[T[*active_edge]];
            if (walk_dfs(next))
                continue;
            if (T[next->start + active_length] == T[pos]) {
                if (last_new_node && active_node != root) {
                    last_new_node->suffix_link = active_node;
                    last_new_node = nullptr;
                }
                active_length += 1;
                break;
            }
            *split_end = next->start + active_length - 1;
            Node *split = new_node(next->start, next->end);
            active_node->children[T[pos]] = split;
            next->start += active_length;
            split->children[T[next->start]] = next;

            if (last_new_node != nullptr) {
                last_new_node->suffix_link = split;
            }
            last_new_node = split;
        }
        remaining_suffix_count -= 1;
        if (active_node == root && active_length > 0) {
            active_length -= 1;
            *active_edge = pos - remaining_suffix_count + 1;
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

char SuffixTree::walk_dfs(Node *current) {
    // TODO: See what to do instead of yielding

    uint16_t start = current->start;
    uint16_t end = *current->end;

    it = T.substr(start, end - start).begin();
    // Check if we even have a valid char to walk through
    if (*it) {
        // save the char on this node to return
        char nuc = *it;
        // Traverse to next nucleotide
        it = next(it);
        return nuc;
    }

    for (const auto &[nucleotide, node] : current->children) {
        if (node)
            walk_dfs(current);
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
    // First active node is root
    active_node = root;
    for (int i = 0; i < T.size(); ++i)
        extend_tree(i);
}