import logging
import numba
from numba import njit
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

A = "TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG"


def string_compare(
    A: str, B: str, mismatch_percentage: float, allow_ins_del: bool = False
):
    # TODO: implement insertion deletion
    if A == B:
        return True

    if not A or not B:
        return False

    max_len = max(len(A), len(B))
    min_len = min(len(A), len(B))
    same_char_at_index = 0
    for i in range(min_len):
        if A[i] == B[i]:
            same_char_at_index += 1

    a = same_char_at_index / max_len
    return a >= (1.0 - mismatch_percentage)


def read_file(filename: str = ".\\data\\s_3_sequence_1M.txt"):
    with open(filename, "r") as f:
        return f.readlines()


def mismatch(content, mismatch_percentage: float):
    allowed_seqs = []

    # FIXME: Handle exception better
    for line in tqdm(content):
        line = line.rstrip()
        l = len(line)
        for i in range(l):
            # Match prefix of a with suffix of s or "line" in this instance
            suffix_prefix = string_compare(A[: l - i], line[i:], mismatch_percentage)
            print(suffix_prefix)
            if suffix_prefix:
                allowed_seqs.append(
                    line
                )  # If one suff / pre match we add the entire line
                # We break since we're only interested in longest suffix
                break

    return allowed_seqs


@njit(fastmath=True)
def make_bins(size: int):
    return np.array([i for i in range(size + 1)])


def make_distribution(array):
    try:
        max_size = np.amax(array)
        bins = make_bins(max_size)
    except ValueError as ve:
        print(f"Error {ve}: No empty arrays allowed")
    else:
        plt.hist(array, bins)
        plt.show()


if __name__ == "__main__":
    print("Reading file...")
    content = read_file()
    print("Read file...")

    print("Starting Algorithm")
    case1 = mismatch(content, 0.0)
    print("Finished Algorithm")

    print("Making distribution...")
    make_distribution(case1)

## TEST
"""
mismatch(0.0. )
mismatch(0.10)
mismatch(0.25)
"""