"""Task 3 in project"""

import matplotlib.pyplot as plt
import numpy as np
from numba import njit
from tqdm import tqdm

from helpers import read_file, A


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


def seq_error_sequence(seqs: list[str]):
    """
    @param seq: String sequence in S
    """
    # At which indexes do we find these errors
    index_errors = []
    for seq in seqs:
        l = len(seq)

        # We only need to look for the length l since we only look at
        # prefixes of A that have matched
        for i in range(l):
            if A[i] != seq[i]:
                index_errors.append(i)

    return np.array(index_errors)


def seq_error_per_nucleotide(seqs: list[str], nucleotide: str):
    """
    @param seqs: allowed sequences which passes even though there can be errors
    @param nucleotide: A, C, T or G
    """
    index_errors_per_nuc = []
    for seq in seqs:
        l = len(seq)

        # Both strings are now of equal length
        for i in range(l):
            # The char in A we are looking at now need
            if A[i] != seq[i] and A[i] != nucleotide:
                index_errors_per_nuc.append(i)

    return np.array(index_errors_per_nuc)


@njit(fastmath=True)
def make_bins(size: int):
    return np.array([i for i in range(size + 1)])


def make_distribution(
    seq_errors, nuc: str = None, has_nuc: bool = False, show: bool = False
):
    plt.hist(
        seq_errors, bins=np.arange(seq_errors.min(), seq_errors.max() + 1), align="left"
    )
    plt.savefig(
        f"..\\images\\sequence_error_rate_{nuc}.png"
    ) if has_nuc else plt.savefig(f"..\\images\\sequence_error_rate.png")
    if show:
        plt.show()


if __name__ == "__main__":
    print("Reading file...")
    content = read_file()
    print("Read file...")

    print("Starting Algorithm")
    # First of we allow 10% mismatch
    mismatches = mismatch(content, 0.1)
    # Make differne
    index_errors = seq_error_sequence(mismatches)
    index_errors_a = seq_error_per_nucleotide(mismatches, "A")
    index_errors_t = seq_error_per_nucleotide(mismatches, "T")
    index_errors_c = seq_error_per_nucleotide(mismatches, "C")
    index_errors_g = seq_error_per_nucleotide(mismatches, "G")
    print("Finished Algorithm")

    print("Making distributions...")
    make_distribution(index_errors, show=True)
    make_distribution(index_errors_a, "A", has_nuc=True)
    make_distribution(index_errors_t, "T", has_nuc=True)
    make_distribution(index_errors_c, "C", has_nuc=True)
    make_distribution(index_errors_g, "G", has_nuc=True)


## TEST
"""
mismatch(0.0. )
mismatch(0.10)
mismatch(0.25)
"""
