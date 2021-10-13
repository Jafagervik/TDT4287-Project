import logging
import numba
from numba import njit
import numpy as np
import matplotlib.pyplot as plt

A = "TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG"


@njit(parallel=True, fastmath=True)
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

    return same_char_at_index / max_len >= (1 - mismatch_percentage)


def read_file(filename: str = ".\\data\\s_3_sequence_1M.txt"):
    with open(filename, "r") as f:
        return f.readlines()


@njit(parallel=True, fastmath=True)
def mismatch(content, mismatch_percentage: float):
    # np_content = np.array(content)
    # num_of_sequences = 0
    allowed_seqs = []

    # FIXME: Handle exception better
    for line in content:
        for i in range(len(line)):
            suffix_prefix = string_compare(
                A[: len(line) - i], line[i:], mismatch_percentage
            )
            if suffix_prefix:
                # num_of_sequences += 1
                allowed_seqs.append(line)
                # We break since we're only interested in longest suffix
                break

    return allowed_seqs


@njit(fastmath=True)
def make_bins(size: int):
    return np.array([i for i in range(size + 1)])


def make_distribution(array):
    max_size = np.amax(array)
    bins = make_bins(max_size)
    plt.hist(array, bins)
    plt.show()


if __name__ == "__main__":
    content = read_file()
    case1 = mismatch(content, 0.0)
    make_distribution(case1)

## TEST
"""
mismatch(0.0. )
mismatch(0.10)
mismatch(0.25)
"""