from os import read
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

from numba import njit


def read_distribution(filename: str):
    """Read a distribution from a file
    inp: >>> 1 4\n2 5\0
    out: >>> dict{"1": 4, "2": 5}
    """
    lengths, counts = np.loadtxt(filename, delimiter=" ", unpack=True)
    return lengths, counts


@njit(parallel=True)
def get_avg(lengths, counts):
    number_of_seqs = len(lengths)
    return (
        np.sum(lengths[i] * counts[i] for i in range(number_of_seqs)) / number_of_seqs
    )


def line_plot(filename: str):
    xs, ys = read_distribution(filename)

    fig, ax = plt.subplots()
    ax.plot(xs, ys)

    ax.set(
        xlabel="DNA Sequences",
        ylabel="Occurences",
        title="Distribution of DNA Sequences",
    )

    ax.grid()

    fig.savefig("task1.png")
    plt.show()


def histogram(filename: str, mean: int, bins: int = 10):
    xs, _ = read_distribution(filename)

    # example data
    mu = mean  # mean of distribution
    sigma = 10  # TODO: calculate sta deviation
    # x = mu + sigma * np.random.randn(437)

    fig, ax = plt.subplots()

    # Histogram
    n, bins, patches = ax.hist(xs, bins, density=True)

    # add a 'best fit' line
    y = (1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(
        -0.5 * (1 / sigma * (bins - mu)) ** 2
    )
    ax.plot(bins, y, "--")
    ax.set_xlabel("Sequence lengths")
    ax.set_ylabel("Probability density")
    ax.set_title(r"Histogram of DNA Sequences: $\mu={mu}$, $\sigma={sigma}$")

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.show()


def main():
    print("----- E N T R Y P O I N T -----")

    print("Task 1: Distributions")
    line_plot("\\data\\s_3_sequence_1M.txt")

    """
    print("Task 2: Distributions")
    line_plot("s_3_sequence_1M.txt")

    print("Task 3: Distributions")
    line_plot("s_3_sequence_1M.txt")

    print("Task 4: Distributions")
    line_plot("s_3_sequence_1M.txt")

    print("Task 5: Distributions")
    line_plot("s_3_sequence_1M.txt")
    """


if __name__ == "__main__":
    main()