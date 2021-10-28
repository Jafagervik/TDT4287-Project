"""File for task 5."""

# 4 <= len(barcode) <= 8

# REPORT: What is the most frequently occurring sequence within each sample?

# All barcodes have the same length

import matplotlib.pyplot as plt
import numpy as np

from helpers import read_file, A


class LCS:
    """Struct for representing an lcs."""

    def __init__(self, label: str, idxs: int, idxe: int, line: int = -1):
        self.line_nr = line  # which line (index) this LCS is in
        self.label = label
        self.start_index = idxs
        self.end_index = idxe


def strip_strings(seqs: list[str], cutoff: int):
    """Trim down seqs."""
    for seq in seqs:
        seq = seq[:cutoff]


def multi_lcs(seqs: list[str]) -> LCS:

    # Determine size of the array
    n = len(seqs)

    # Take first word from array
    # as reference
    s = seqs[0]
    l = len(s)
    idxs = -1
    idxe = -1
    res = ""

    for i in range(l):
        for j in range(i + 1, l + 1):

            # generating all possible substrings
            # of our reference string arr[0] i.e s
            stem = s[i:j]
            k = 1
            for k in range(1, n):

                # Check if the generated stem is
                # common to all words
                if stem not in seqs[k]:
                    break

            # If current substring is present in
            # all strings and its length is greater
            # than current result
            if k + 1 == n and len(res) < len(stem):
                res = stem
                idxs = i
                idxe = j

    print(f"LCS: {res}")
    print(f"Starting at index {idxs} and ending at {idxe}")
    return LCS(res, idxs, idxe)


def identify_barcodes(seqs: list[str]) -> list[str]:
    """Part 1 - identify the
    barcodes (3’ adapters) used and thereby how many samples were multiplexed"""
    # Find 3' adapter through most common subseq
    # Remove these and filler afterwards
    # The remaining suffix is now the barcodes
    barcodes = []

    # Seqs share same length
    seq_length = len(seqs[0])

    while True:

        lcs = multi_lcs(seqs)

        # ROUGH ESTIMATE
        if lcs.start_index <= int(seq_length / 4):
            # We've now found all the 3' adapters and the barcodes we were interested in
            break

        # From the information of the task we know that the length is in range [4,8]
        # Barcodes should now also be at the end since we've removed 3' adapters and fillers
        if 4 <= len(lcs.label) <= 8 and lcs.end_index == seq_length - 1:
            barcodes.append(lcs.label)

        # Remove the lcs found to repeat the process, should remove 3' adapters and fillers before barcode
        strip_strings(seqs, lcs.start_index)

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


if __name__ == "__maim__":
    seqs = read_file("../data/MultiplexedSamples.txt")[:1000]
    barcodes = identify_barcodes(seqs)
    print(f"We have {len(barcodes)} barcodes.")
    seqs_per_sample = num_of_seqs_per_sample(seqs, barcodes)
