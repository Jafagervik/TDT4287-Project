import numba
from numba import njit
import numpy as np
import matplotlib.pyplot as plt

from .visualize import *

A = "TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG"


@njit(parallel=True, fastmath=True)
def knut_morris_plot(T: str, P: str) -> tuple(list[int], int):
    """Substring search algorithm O(m+n)

    TODO: find way to implement mismatches
    """

    # longest prefix sufffix

    m = len(T)
    n = len(P)
    lps = [0] * n
    j = 0

    compute_lcs_array(P, n, lps)
    i = 0
    while i < n:
        if P[j] == T[i]:
            i += 1
            j += 1
            # If we're at end
            if j == n:
                if (i - j) == 0:
                    print(f"Found pattern at index {str(i-j)}")
                    return True
                j = lps[j - 1]

        elif i < m and P[j] != T[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return False


@njit(parallel=True, fastmath=True)
def compute_lcs_array(P: str, n: int, lps: list[int]):
    # length of the previous longest prefix suffix
    l = 0
    lps[0] = 0
    i = 1

    while i < n:
        if P[i] == P[l]:
            l += 1
            lps[i] = l
            i += 1
        else:
            if l:
                l = lps[l - 1]
            else:
                lps[i] = 0
                i += 1


@njit(parallel=True, fastmath=True)
def string_compare(A: str, B: str, mismatch_percentage: float):
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


def read_seq3(filename: str):
    with open(filename, "r") as f:
        yield from f.readlines()


@njit(parallel=True, fastmath=True)
def mismatch(mismatch_percentage: float):
    num_of_sequences = 0
    allowed_seqs = np.array([])

    gen = read_seq3(".\\data\\s_3_sequence_1M.txt")

    # FIXME: Handle exception better
    while gen:
        for i in range(len(gen)):
            suffix_prefix = string_compare(A[: len(gen) - i], gen[i:])
            if suffix_prefix:
                num_of_sequences += 1
                allowed_seqs.append(gen)
                # We break since we're only interested in longest suffix
                break

        gen = next(gen)

    return allowed_seqs


def make_distribution(array):
    max_size = np.amax(array)
    bins = np.array([i for i in range(max_size + 1)])
    plt.hist(array, bins)
    plt.show()


## TEST
"""
mismatch(0.0)
mismatch(0.10)
mismatch(0.25)
"""