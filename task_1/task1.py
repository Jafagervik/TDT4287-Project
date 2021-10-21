# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from suffixtree import *
import numpy as np
import matplotlib.pyplot as plt

def read_file(filename):
    f = open(filename, 'r')
    lines = []
    while True:
        line = f.readline()
        if not line:
            break
        else:
            lines.append(line)
    f.close()
    return lines

def task_one(lines, r_a_tree):
    result = [0] * 51 # array of fixed size
    count = 0
    for line in lines:
        line = line.strip('\n')
        r = r_a_tree.matchS(line)

        # store length of S after removal of match
        # all S have a length of 50.
        s_remaining_length = 50-r
        result[s_remaining_length]+=1
            # print(str(r) + " for line "+ str(count))

        count += 1

    # visualize task 1.
    fig, ax = plt.subplots()

    ax.set(
        xlabel="Length after match removal",
        ylabel="Occurences",
        title="Task 1: Distribution of DNA Sequences",
    )
    ax.grid()

    newdata = np.squeeze(result)  # Shape is now: (10, 80)
    plt.plot(newdata, color='orange', linewidth= 3)  # plotting by columns
    fig.savefig("task1.png")

    plt.show()
    print("Total number of perfectly matching fragments: " + str(1000000-result[50]))
    return result


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.

    # s should be longer than A

    s = "CAT"
    a = "CAT"
    a_reversed = a[::-1] + "$"# reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert(tree.matchS(s) == 3)



    s = "CAT"
    a = "CA"
    a_reversed = a[::-1] + '$'# reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert(tree.matchS(s) == 0)




    s = "CAT"
    a = "T"
    a_reversed = a[::-1] + '$' # reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert(tree.matchS(s) == 1)



    s = "CAT"
    a = ""
    a_reversed = a[::-1] + '$' # reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert(tree.matchS(s) == 0)


    s = "CAT"
    a = "GG"
    a_reversed = a[::-1] + '$' # reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert(tree.matchS(s) == 0)

    s = ""
    a = "GG"
    a_reversed = a[::-1] + '$' # reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert(tree.matchS(s) == 0)

    s = "A"
    a = "AGCT"
    a_reversed = a[::-1] + '$' # reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert(tree.matchS(s) == 1)
    s = "AG"
    a = "AGCT"
    a_reversed = a[::-1] + '$' # reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert(tree.matchS(s) == 2)

    s = "AGCT"
    a = "AGCT"
    a_reversed = a[::-1] + "$" # reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert (tree.matchS(s) == 4)
    s = "AGC"
    a = "AGCT"
    a_reversed = a[::-1]  + "$"  # reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert (tree.matchS(s) == 3)

    s = "AX"
    a = "AGCT"
    a_reversed = a[::-1]  + "$"  # reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert (tree.matchS(s) == 0)
    s = "AGCTAGCT"
    a = "AGCT"
    a_reversed = a[::-1]  + "$"  # reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert (tree.matchS(s) == 4)

    s = "TGACGTGHTAGATCGATCG"
    a = "GATCGATCGTT"
    a_reversed = a[::-1]  + "$"  # reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert (tree.matchS(s) == 9)

    s = "TGACGTGHTAGATCGATCG"
    a = "GATCG"
    a_reversed = a[::-1] + "$" # reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert (tree.matchS(s) == 5)



    s = "TGACGTGHTAGATCGATCG"
    a = "GATC"
    a_reversed = a[::-1] + "$" # reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert (tree.matchS(s) == 1)

    s = "TGACGTGHTAGATCGATCG"
    a = ""
    a_reversed = a[::-1] + "$" # reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert (tree.matchS(s) == 0)

    s = "T"
    a = "C"
    a_reversed = a[::-1] + "$" # reverse a
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    assert (tree.matchS(s) == 0)

    A = "TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG"
    lines = read_file("./data/s_3_sequence_1M.txt")
    a_reversed = A[::-1] + "$"
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    result = task_one(lines, tree)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
