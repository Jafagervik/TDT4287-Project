"""Task 3 in project"""

import matplotlib.pyplot as plt
import numpy as np
from numba import njit, prange
from tqdm import tqdm


A = "TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG"


def read_file(filename: str = "..\\data\\s_3_sequence_1M.txt"):
    with open(filename, "r") as f:
        return f.readlines()


# ======= TASK 2 =======


@njit(fastmath=True, parallel=True)
def string_compare(
    a_prefix: str, B: str, allow_ins_del: bool = False
) -> tuple[bool, bool]:
    """
    Hamming distance between two strings.

    returns a tuple if it belongs to 0.10 or 0.25 mismatch array
    """
    # TODO: implement insertion deletion
    if a_prefix == B:
        return (True, True)

    if not a_prefix or not B:
        return (False, False)
    # Both strings have same value
    l = len(a_prefix)
    same_char_at_index = 0
    for i in prange(l):
        if a_prefix[i] == B[i]:
            same_char_at_index += 1

    match = same_char_at_index / l
    return (match >= (1.0 - 0.1), match >= (1.0 - 0.25))


def mismatch(seqs: list[str], allow_ins_del: bool = False) -> list[str]:
    allowed_seqs_10 = []
    allowed_seqs_25 = []

    for line in tqdm(seqs):
        line = line.rstrip()  # Remove trailing newline
        l = len(line)
        suffix_10_found = False
        suffix_25_found = False
        for i in range(l):
            # Match prefix of a with suffix of s or "line" in this instance
            suffix_prefix_10, suffix_prefix_25 = string_compare(A[: l - i], line[i:])

            if suffix_prefix_10 and not suffix_10_found:
                allowed_seqs_10.append(
                    # Add the suffix which is allowed, all sequences have same length anyways
                    line[i:]
                )
                suffix_10_found = True

            if suffix_prefix_25 and not suffix_25_found:
                allowed_seqs_25.append(line[i:])

                suffix_25_found = True

            if suffix_10_found and suffix_25_found:
                # We've now found suffix/prefix match for both 10 and 25%
                # go to next sequence
                break

    return np.array(allowed_seqs_10), np.array(allowed_seqs_25)


# ======= TASK 3 =======


@njit(fastmath=True, parallell=True)
def seq_error_sequence(seqs: list[str]):
    """
    Array of indexes where sequence error occurs
    @param seqs: List of sequences
    """
    # At which indexes do we find these errors
    index_errors = []
    for seq in seqs:
        l = len(seq)

        # We only need to look for the length l since we only look at
        # prefixes of A that have matched
        for i in prange(l):
            if A[i] != seq[i]:
                index_errors.append(i)

    return np.array(index_errors)


@njit(fastmath=True, parallel=True)
def rate_of_seq_error(seqs: list[str]) -> float:
    """
    @param seqs: allowed sequences which passes even though there can be errors
    """
    sequence_error_count = 0
    n = len(seqs)
    for seq in prange(n):
        # len of current sequence
        l = len(seqs[seq])
        # string sequence s and does not match with prefix of A
        if A[:l] != seqs[seq]:
            sequence_error_count += 1
            # Found error, go to next sequence

    return float(sequence_error_count / l)


# ======= DISTRIBUTIONS AND PLOTTING =======


@njit(fastmath=True)
def make_bins(size: int):
    return np.array([i for i in range(size + 1)])


def make_distribution_task2(array, percentage: int, filename: str, show: bool = False):
    assert len(array) > 0, "No empty arrays allowed"

    array_lengths = np.vectorize(len)(array)

    max_size = np.amax(len(max(array, key=len)))
    bins = make_bins(max_size + 1)
    plt.xlabel("Sequence lengts")
    plt.ylabel("Frequency of lengths")
    plt.title(
        f"Histogram of sequence length from allowed sequcenes Mismatch allowed: {percentage}%"
    )
    plt.hist(array_lengths, bins)

    plt.savefig(f"..\\images\\{filename}.png")

    if show:
        plt.show()


def make_distribution(
    seq_errors,
    percentage: int,
    show: bool = False,
):
    plt.xlabel("Index in string")
    plt.ylabel("Frequency of errors")

    plt.title("Histogram of where error occurs for sequence")
    plt.hist(
        seq_errors, bins=np.arange(seq_errors.min(), seq_errors.max() + 1), align="left"
    )

    plt.savefig(f"..\\images\\sequence_error_rate_mismatch{percentage}.png")

    if show:
        plt.show()


if __name__ == "__main__":

    print("Reading file...")
    content = read_file()
    print("Read file...")

    # First of we allow 10% mismatch
    case10, case25 = mismatch(content)

    print("Making distributions for task 2...")
    make_distribution_task2(case10, 10, "distrib_length_10pc")
    make_distribution_task2(case25, 25, "distrib_length_25pc")

    print("Starting Task 3...")
    index_errors_10 = seq_error_sequence(case10)
    rate_seq_error_10 = rate_of_seq_error(case10)
    print(
        "Number of accepted sequences with 10% mismatch with errors:",
        round(rate_seq_error_10, 2) * 100,
        "percent",
    )

    print(r"Making distributions for 10% allowed mismatch...")
    make_distribution(index_errors_10, 10)

    # 25 PERCENT
    index_errors_25 = seq_error_sequence(case25)
    rate_seq_error_25 = rate_of_seq_error(case25)
    print(
        "Number of accepted sequences with 25% mismatch with errors:",
        round(rate_seq_error_25, 2) * 100,
        "percent",
    )

    print(r"Making distributions for 25% allowed mismatch...")
    make_distribution(index_errors_25, 25)

    print("Finished making distributions...")
