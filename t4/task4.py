# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import matplotlib.pyplot as plt
import time
from task_1.suffixtree import SuffixTree

A = 0
T = 1
G = 2
C = 3
adapter_threshold = 60
adapter_suffix_threshold = 25
frequent_key_threshold = 10000

# read file and append each result to a file.
def read_file(filename):
    f = open(filename, 'r')
    lines = []
    longest = 0
    counter = 0
    while True:
        line = f.readline().strip("\n")
        if len(line) > longest:
            longest = len(line)
        if not line:
            break
        else:
            lines.append(line)
        counter+=1
        # change this to 10 000 for faster debugging. (small dataset)
        # if counter == 100000:
        #     break

    f.close()
    return lines, longest


def adapt_seq_continuation(adapt_seq, longest, lines):
    adapt_length = len(adapt_seq)-1
    # initialize two dim array with 0'es
    array = [[0 for x in range(4)] for y in range(longest-len(adapt_seq))]

    for line in lines:
        # search for adapt_seq.
        # add the char after adapt sequence to array[0] etc etc.
        if line.__contains__(adapt_seq):
            char_ptr = 0
            insert_ptr = 0
            end_line = len(line)
            full_seq = False
            # iterates through entire line.
            while char_ptr < end_line:
                # find where a as we know ends.

                # check if current char is adapt length start and ends at same as adapt lenght
                if full_seq == False and line[char_ptr] == adapt_seq[0] and line[char_ptr+adapt_length] == adapt_seq[adapt_length]:
                    # check if this every char also matches adapt sequence prefix so far.
                    adapt_ptr = 0
                    while adapt_ptr <= adapt_length:
                        if line[char_ptr+adapt_ptr] == adapt_seq[adapt_ptr]:
                            # match
                            adapt_ptr += 1
                        else:
                            # not a match break
                            break
                    # everything matched -> adapt sequence present.
                    if adapt_ptr > adapt_length:
                        char_ptr += adapt_ptr-1
                        # flip boolean for reading remainder chars to two dimm statistic array.
                        full_seq = True
                # read remainding char into statistic array
                elif full_seq == True:
                    if line[char_ptr] == 'A':
                        array[insert_ptr][A]+=1

                    elif line[char_ptr] == 'T':
                        array[insert_ptr][T]+=1

                    elif line[char_ptr] == 'G':
                        array[insert_ptr][G]+=1
                    else:
                        array[insert_ptr][C]+=1
                    insert_ptr+=1
                char_ptr+=1
                # add remainder of string to array.
    # read most likely sufix of the adapter prefix from array
    result = get_brute_force_results_array(array, longest-len(adapt_seq), lines, adapter_suffix_threshold)
    return adapt_seq + result

# This functions reads the two dimentional array with results for most likely string combinations.
def get_brute_force_results_array(array, length, lines, percentage_threshold):
    result = ""
    for i in range(0, length):
        total = 0
        current_most_likely_number = 0
        current_most_likely = 'A'
        total += array[i][A]
        current_most_likely_number = array[i][A]

        total+=array[i][T]
        if(array[i][T] > current_most_likely_number):
            current_most_likely_number = array[i][T]
            current_most_likely = 'T'

        total+=array[i][G]
        if(array[i][G] > current_most_likely_number):
            current_most_likely_number = array[i][G]
            current_most_likely =  'G'

        total+=array[i][C]
        if(array[i][C] > current_most_likely_number):
            current_most_likely_number = array[i][C]
            current_most_likely = 'C'

        percentage = 0
        if total != 0:
            percentage = current_most_likely_number/total*100
        # threshold defined on top of file.
        if percentage > percentage_threshold:
            # if current percentage is sufficient append current result to string.
            result = result + current_most_likely
    return result

def task_four_distribution(lines, r_a_tree, longest):
    result = [0] * (longest+1) # array of fixed size
    count = 0
    map = {}
    for line in lines:
        line = line.strip('\n')
        r = r_a_tree.matchS(line)

        # store length of S after removal of match
        # all S have a length of 50.
        s_remaining_length = longest-r
        s = line[:s_remaining_length]
        if not map.__contains__(s):
            map[s] = 1
        else:
            map[s] += 1

        result[s_remaining_length]+=1
            # print(str(r) + " for line "+ str(count))

        count += 1

    # visualize task 1.
    fig, ax = plt.subplots()

    ax.set(
        xlabel="Length after match removal",
        ylabel="Occurences",
        title="Task 4: Distribution of DNA Sequences",
    )
    ax.grid()

    newdata = np.squeeze(result)  # Shape is now: (10, 80)
    plt.plot(newdata, color='orange', linewidth= 3)  # plotting by columns
    fig.savefig("task4.png")

    plt.show()
    #print("Total number of perfectly matching fragments: " + str(len(lines)-result[longest]))
    return map

def brute_force_t4(lines, longest):
    # test case for troubleshooting:
    # lines = []
    # lines.append("CCCTAG")
    # lines.append("CCCTAG")
    # lines.append("CCCTAG")
    # lines.append("GGGTAG")
    # lines.append("AAATAG")
    # lines.append("GGGTAG")
    # lines.append("AAATAG")
    # lines.append("GGGTAG")
    # lines.append("AAATAG")
    # lines.append("TTTAGC")
    # lines.append("TAGCA")
    # longest = 6
    # two dim array with longest * 4.
    array = [[0 for x in range(4)] for y in range(longest)]
    # reads each line into two dim array which notes what nucleotide is at the index.
    # note that the array is filles up from the end. This means that only the longest strings (lenght of array width) will use A[0].
    # e.g :
    # long string:      A G C T A G
    # short string:           T A G
    #                   G C T T A G
    # array:
    # index             0 1 2 3 4 5
    #  A counter        1 0 0 0 3 0
    #  T counter        0 0 1 3 0 0
    #  G counter        1 1 0 0 0 3
    #  C counter        0 1 1 0 0 0

    # most likely for
    # each index:       ? ? ? T A G
    # unkown values do not have high enough percentage of all hits. Defined in adapt_thresholds on top of file.

    for sequence in lines:
        seq_length = len(sequence)
        for i in range(0, seq_length):
                if sequence[i] == 'A':
                    array[longest-seq_length+i][A] += 1

                elif sequence[i] == 'T':
                    array[longest-seq_length+i][T] += 1

                elif sequence[i] == 'G':
                    array[longest-seq_length+i][G] += 1

                else:
                    array[longest-seq_length+i][C] += 1

    adapt_seq_prefix = get_brute_force_results_array(array, longest, lines, adapter_threshold)
    adapt_seq = adapt_seq_continuation(adapt_seq_prefix, longest, lines)
    return adapt_seq

def remove_adapters_get_distribution():
    pass
def print_hi(name):
    read_file_start_time = time.time()
    lines, longest = read_file("../data/tdt4287-unknown-adapter.txt")
    read_file_end_time = time.time()

    calc_adapt_seq_start_time = time.time()
    adapt_seq = brute_force_t4(lines, longest)
    calc_adapt_seq_end_time = time.time()
    # build tree
    radpt_tree = None
    a_reversed = adapt_seq[::-1] + "$"
    match_fragments_start_time = time.time()
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    map = task_four_distribution(lines, tree, longest)
    match_fragments_end_time = time.time()

    get_frequent_seq_start_time = time.time()
    higly_frequent_keys = dict(sorted(map.items(), key=lambda item: item[1], reverse=True))
    counter = 0
    print("Highly frequent sequences:")
    for key in higly_frequent_keys.keys():
        value = higly_frequent_keys[key]
        print(key + " is occuring " + str(value) + " times.")
        counter += 1
        if value < frequent_key_threshold:
            break
    get_frequent_seq_end_time = time.time()
    print("Frequent key threshold: "+ str(frequent_key_threshold))
    print("\nAdapter threshold: "+ str(adapter_threshold) + "%")
    print("Adater suffix threshold: " + str(adapter_suffix_threshold)+"%")
    print("Most likely adapt sequence: " + adapt_seq)
    print("Unique sequences: " + str(len(map)))

    print("\nTime used in seconds:")
    print("Read file time:                " + str(read_file_end_time-read_file_start_time))
    print("Calculate adapt sequence time: " + str(calc_adapt_seq_end_time-calc_adapt_seq_start_time))
    print("Match fragments time:          " + str(match_fragments_end_time-match_fragments_start_time))
    print("Get frequent keys time:        " + str(get_frequent_seq_end_time-get_frequent_seq_start_time))




if __name__ == '__main__':
    print_hi('YO')
