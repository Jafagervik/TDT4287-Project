from numba import njit
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from helpers import read_file, A


def string_compare(
    A: str, B: str, mismatch_percentage: float, allow_ins_del: bool = False
):
    """
    Hamming distance between two strings.
    """
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


def mismatch(
    content, mismatch_percentage: float, allow_ins_del: bool = False
) -> list[str]:
    allowed_seqs = []

    # FIXME: Handle exception better
    for line in tqdm(content):
        line = line.rstrip()  # Remove trailing newline
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


def make_distribution(array, filename: str, show: bool = False):
    try:
        max_size = np.amax(array)
        bins = make_bins(max_size)
    except ValueError as ve:
        print(f"Error {ve}: No empty arrays allowed")
    else:
        plt.hist(array, bins)
        plt.savefig(f"..\\images\\{filename}.png")

    if show:
        plt.show()


if __name__ == "__main__":
    print("Reading file...")
    content = read_file()
    print("Read file...")

    print("Starting Algorithm for 0, 10 and 25% mismatch")
    case1 = mismatch(content, 0.0)
    case2 = mismatch(content, 0.1)
    case3 = mismatch(content, 0.25)
    print("Finished Algorithm")

    print("Starting Algorithm for 0, 10 and 25% mismatch with ins/dels")
    case1_modification = mismatch(content, 0.0, True)
    case2_modification = mismatch(content, 0.1, True)
    case3_modification = mismatch(content, 0.25, True)
    print("Finished Algorithm")

    print("Making distributions...")
    make_distribution(case1, "distrib_length_0pc")
    make_distribution(case2, "distrib_length_10pc")
    make_distribution(case3, "distrib_length_25pc")

    make_distribution(case1_modification, "distrib_length_0pc_mod")
    make_distribution(case2_modification, "distrib_length_10pc_mod")
    make_distribution(case3_modification, "distrib_length_25pc_mod")
    print("Finished executing tasks...")
