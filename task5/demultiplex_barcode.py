"""File for task 5."""

# 4 <= len(barcode) <= 8

# REPORT: What is the most frequently occurring sequence within each sample?

"""
Sequence: ATCG
ATCG
 TCGA
  CGAT

Sample becomes: ATCGAT

"""

import matplotlib.pyplot as plt
import numpy as np

from suffix_tree import Tree

from helpers import read_file, A


def make_suffix_tree(lines: list[str]):
    """Creates a suffix tree of all sequences in file."""

    seqs = {}

    for idx, line in enumerate(lines):
        seqs[idx] = line

    tree = Tree(seqs)
    return tree


def identify_barcodes(tree: Tree) -> list[str]:
    """Part 1 - identify the
    barcodes (3’ adapters) used and thereby how many samples were multiplexed"""
    # set up suffix tree
    # look for occuring patterns
    # Find common suffixes, and add these to list of barcodes
    barcodes = []

    # TODO: set up traversing to find barcode
    # From the information of the task we know that the length is in range [4,8]
    if 4 <= len(barcode) <= 8:
        barcode.append("yes")
    return barcodes


def num_of_seqs_per_sample(seqs: list[str], barcodes: list[str]):
    """Part 2 - identify how many sequences that were sequenced from each sample."""
    # naive: return len(seqs)
    # actual: return nun of barcodes found in the tree
    pass


def seq_length_dist():
    """Part 3 - identify
    the sequence length distribution within each sample."""
    # Look through each
    pass


def make_distribution(seqs: list[str], show: bool = False):
    plt.hist(seqs, bins=np.arange(seqs.min(), seqs.max() + 1), align="left")
    plt.savefig(f"..\\images\\task5_seq_length_dist.png")

    if show:
        plt.show()


def main():
    print("Hello World")


if __name__ == "__maim__":
    seqs = read_file("../data/MultiplexedSamples.txt")
    tree = make_suffix_tree(seqs)
    barcodes = identify_barcodes(tree)
    seqs_per_sample = num_of_seqs_per_sample(seqs, barcodes)

    main()
