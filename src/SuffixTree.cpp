#include "../include/SuffixTree.hpp"
#include <string>
#include <iostream>

SuffixTree::SuffixTree(){
    root = nullptr;
    end = nullptr;
};
SuffixTree::~SuffixTree(){
    free(end);
};
uint16_t SuffixTree::max_suffix(std::string a) {
    // calculate longest suffix in tree mathcing with prefixes of a.
    return 10;
};


void SuffixTree::build_tree(std::string s) {
    s = s + "$"; // Add terminating dollar sign to algorithm.
    uint16_t *end = new uint16_t;
    *end = -1; // increased to 0 at the start of first iteration.
    // init variables for Ukkonen algorithm
    {
        Node n = Node(NodeType::ROOT,0, 0);
        root = &n;
    }
    uint16_t remainder = 0;
    Node * active_node = root;
    Node * active_edge = nullptr;
    uint16_t active_length = 0; // remainder on active_edge


    // iterates over all the characters in string s.
    for (int i = 0; i < s.length(); i++){

        // increase remainder & end value.
        remainder++;
        end++;

        Node * last_created_int_node = nullptr;


        while (remainder > 0){
            // dependant on active edge value
            // if active edge == nullptr just add as below
            // else we have to split edge.

            if(active_edge == nullptr){
                Node n = Node(NodeType::LEAF, i, end);
                n.parent = active_node;
                active_node->children.push_back(&n);
                if(active_node == root){
                    remainder--; // after adding a new edge/node decrease the remainder.
                }
                else{
                    // follow suffix link to new active node,
                    // if no suffix link set active node to root
                }
            }
        }
        // check if current char is already a children of active Node
        //for (Node *n : active_node->children){
        //        children_node = n;
        }
        // if an active children was found update active edge
    }
//    uint16_t *end = new uint16_t;
//    // remember to free end
//    *end = 7;
//    Node n = Node(NodeType::ROOT, 0, end);
//    root = &n;
//    *end = 8;
//    std::cout << *(root->to);
};