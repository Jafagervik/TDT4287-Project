"""File for task 5."""

# 4 <= len(barcode) <= 8

# REPORT: What is the most frequently occurring sequence within each sample?

# All barcodes have the same length

# FIRST WE TRY TO AVOID DUPLICATES AND DIRECTLY MODIFY LIST

import matplotlib.pyplot as plt
import numpy as np
from numba import njit
from tqdm import tqdm
import re

from collections import Counter

BARCODE_LENGTH = 6


def read_file(filename: str = "..\\data\\MultiplexedSamples.txt"):
    with open(filename, "r") as f:
        return f.read().splitlines()


def remove_barcodes(seqs: list[str]):
    for seq in seqs:
        seq = seq[: len(seq) - BARCODE_LENGTH]


# @njit(fastmath=True)
def multi_lcs(seqs: list[str]) -> str:

    # Determine size of the array
    n = len(seqs)

    # Take first word from array
    # as reference
    s = seqs[0]
    l = len(s)
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
                # lines.append(i)

    return res


def identify_barcodes(seqs: list[str]) -> tuple[list[str], list[str]]:
    """Part 1 - identify the
    barcodes (3’ adapters) used and thereby how many samples were multiplexed"""
    # Find 3' adapter through most common subseq
    # Remove these and filler afterwards
    # The remaining suffix is now the barcodes
    barcodes = []

    # have to copy of lines
    # go thrugh sequences
    # find lcs ( this will be adapt seq first )
    # remove lines with adapter completely from list we are iterating over Copy-seqs
    # remove lcs at end from the same lines we're removing entirely from the other list SEQS
    copy_seqs = seqs.copy()

    # Seqs share same length
    # l = len(copy_seqs[0])
    i = 1

    while True:
        if copy_seqs == []:
            # TODO: Find barcode more properly

            # we can now remove barcodes and put into list
            for seq in seqs:
                barcodes.append(seq[-BARCODE_LENGTH:])
                seq = seq[: len(seq) - BARCODE_LENGTH]
            break

        lcs = multi_lcs(copy_seqs)

        if not lcs:
            break

        indexes_to_pop = []
        for line, seq in tqdm(enumerate(copy_seqs)):
            # If end of each sequence contains lcs, remove
            # TODO: go over indexing here
            start_index = seq.find(lcs)
            if start_index != -1:
                # trim end from seqs
                seqs[line] = seq[: start_index + 1]
                # remove line entirely from the list we're iterating over
                indexes_to_pop.append(line)

        copy_seqs = [s for idx, s in enumerate(copy_seqs) if idx not in indexes_to_pop]

    return barcodes, seqs


def num_of_seqs_per_sample(barcodes: list[str]):
    """Part 2 - identify how many sequences that were sequenced from each sample."""
    # naive: return len(seqs)
    # 2. how many lines (seqs) share same barcode

    for key, value in Counter(barcodes).items():
        print(key, value)


def seq_length_dist(seqs: list[str], barcode: str) -> list[int]:
    """Part 3 - identify
    the sequence length distribution within each sample."""
    # most_common_barcode = Counter(barcodes).most_common(1)
    # unique_barcodes = set(barcodes)

    length_dist = []

    for seq in seqs:
        l = len(seq)
        # print(f"{seq[- BARCODE_LENGTH:]} vs {bc}")
        if seq[-BARCODE_LENGTH:] == barcode:
            length_dist.append(l - BARCODE_LENGTH)

    return length_dist


def insertions_per_bc(seqs: list[str], barcode: str) -> list[str]:
    insertions = []
    for seq in seqs:
        l = len(seq)
        insertion = seq[: l - BARCODE_LENGTH]
        if seq[-BARCODE_LENGTH:] == barcode:
            insertions.append(insertion)

    return insertions


def make_distribution(dist: list[str], barcode: str, show: bool = False):
    plt.hist(dist, bins=np.arange(dist.min(), dist.max() + 1), align="left")
    plt.xlabel("Insertion length")
    plt.ylabel("Frequency")
    plt.title(f"Length distribution for barcode {barcode}")
    plt.savefig(f"..\\images\\task5_seq_length_dist_bc{barcode}.png")

    if show:
        plt.show()


if __name__ == "__main__":
    seqs = read_file("../data/MultiplexedSamples.txt")
    barcodes, seqs = identify_barcodes(seqs)

    # Part 1
    print(f"We have {len(set(barcodes))} barcodes")

    # Part 2
    seqs_per_sample = num_of_seqs_per_sample(barcodes)
    print("PART 2")

    # Part 3 - find seqs
    remove_barcodes(seqs)

    for bc in set(barcodes):
        dist = seq_length_dist(seqs, bc)
        # print(f"dist: {dist}")
        make_distribution(np.array(dist), bc)

        insertions_for_bc = insertions_per_bc(seqs, bc)

        most_common = Counter(insertions_for_bc).most_common(1)
        print(f"Most common insertion for barcode {bc} is {most_common}")
