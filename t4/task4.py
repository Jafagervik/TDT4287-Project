# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import matplotlib.pyplot as plt
import time
from suffixtree import SuffixTree


# nucleotide number reprentation for Array access.
A = 0
T = 1
G = 2
C = 3

# thresholds for the heuristic propability adapter sequence matching.
adapter_threshold = 60
adapter_suffix_threshold = 40
adapter_unique_threshold = 60
adapter_unique_suffix_threshold = 40

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
        counter += 1
        # change this to 10 000 for faster debugging. (small dataset)
        # if counter == 10000:
        #     break

    f.close()
    return lines, longest


def adapt_seq_continuation(adapt_seq, longest, lines, suff_threshold):
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
    result = get_brute_force_results_array(array, longest-len(adapt_seq), lines, suff_threshold, loopBehind=False)
    return adapt_seq + result

# this prints indice and estimated char and its percentage for the index.
def print_char_results(char_results):
    i = 0
    length = len(char_results)
    index_str = ""
    char_str = ""
    perc_str = ""
    full_string = ""
    while i < length:
        c = char_results[i][0]
        p = round(char_results[i][1], 1)
        index_str = index_str + "{:>5}".format(str(i))
        perc_str = perc_str  + "{:>5}".format(p)
        char_str = char_str  + "{:>5}".format(str(c))
        i += 1
        if i % 25 == 0:
            full_string = full_string + index_str +"\n" + char_str + "\n" + perc_str + "\n\n"
            index_str = ""
            perc_str = ""
            char_str = ""

    full_string = full_string + index_str +"\n" + char_str + "\n" + perc_str + "\n\n"

    print(full_string)


# This functions reads the two dimentional array with results for most likely string combinations.
def get_brute_force_results_array(array, length, lines, percentage_threshold, loopBehind):
    result = ""
    char_result = []
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
        #print("For index: " + str(i) + " most likely is " + current_most_likely + " with a percentage of " + str(percentage))
        char_result.append((current_most_likely, percentage))

    # iteration front or from start, with threshold and stop at first below threshold.
    if(loopBehind == True):
        # loop from behind.
        for elem in reversed(char_result):

            perc = elem[1]
            if( elem[1] > percentage_threshold):
                result = elem[0] + result
            else:
                break
    else:
        # loop from front of array.
        for element in char_result:

            perc = element[1]
            if(element[1] > percentage_threshold):
                result = result + element[0]
            else:
                break
    print_char_results(char_result)
    return result

def task_four_distribution(lines, r_a_tree, longest):
    result = [0] * (longest+1) # array of fixed size
    count = 0
    map = {}
    for line in lines:
        line = line.strip('\n')
        r = r_a_tree.matchS(line)

        # store length of S after removal of match
        # all S have a length of longest.
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

def brute_force_t4(lines, longest, threshold, suffix_threshold):
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

    adapt_seq = get_brute_force_results_array(array, longest, lines, threshold, loopBehind=True)
    if(len(adapt_seq) != 0):
        print("--->Adapter suffix percentages: ")
        adapt_seq = adapt_seq_continuation(adapt_seq, longest, lines, suffix_threshold)
    return adapt_seq

def task4_read_unkown_adapt():
    print("#####tdt4287-unkown-adapter.txt######")
    read_file_start_time = time.time()
    lines, longest = read_file("../data/tdt4287-unknown-adapter.txt")
    read_file_end_time = time.time()

    calc_adapt_seq_start_time = time.time()
    print("Adapter seq percentages")
    adapt_seq = brute_force_t4(lines, longest, adapter_threshold, adapter_suffix_threshold)
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
    higly_frequent_sequences = dict(sorted(map.items(), key=lambda item: item[1], reverse = True))
    f = open("higly_frequent_sequences.csv", "w")
    f.write("sequence,occurences")


    # TASK: Does the set contain any highly frequent sequences; i.e. what is the
    # frequency distribution of unique sequences in the set?
    # open and read the file after the appending:
    longest_unique = 0
    for key in higly_frequent_sequences.keys():
        value = higly_frequent_sequences[key]
        f.write(key + ","+str(value)+"\n")
        if len(key) > longest_unique:
            longest_unique = len(key)




    f.close()
    get_frequent_seq_end_time = time.time()

    # TASK:
    # Does the unique set contain any
    # other common (proper) suffix patterns?
    # rerun algorithm on the unique set only.
    print("\nAdapter threshold: "+ str(adapter_threshold) + "%")
    print("Adater suffix threshold: " + str(adapter_suffix_threshold)+"%")
    print("Most likely adapt sequence: " + adapt_seq)

    print("\nUnique set adapter threshold: "+ str(adapter_unique_threshold) + "%")
    print("Unique set adater suffix threshold: " + str(adapter_unique_suffix_threshold)+"%")
    print("Unique sequences: " + str(len(map)))
    print("Adapter match percentages:")
    unique_adapt_seq = brute_force_t4(map.keys(), longest_unique, adapter_unique_threshold, adapter_unique_suffix_threshold)
    print("Likely adapter for unique set:"+ unique_adapt_seq)
    print("______________________________________________")



    print("\nTime used in seconds:")
    print("Read file time:                " + str(read_file_end_time - read_file_start_time))
    print("Calculate adapt sequence time: " + str(calc_adapt_seq_end_time - calc_adapt_seq_start_time))
    print("Match fragments time:          " + str(match_fragments_end_time - match_fragments_start_time))
    print("Get frequent keys time:        " + str(get_frequent_seq_end_time - get_frequent_seq_start_time))


def task4_analyze_set_1M():
    print("\n\n#####s_3_sequence_1M.txt######")
    read_file_start_time = time.time()
    lines, longest = read_file("../data/s_3_sequence_1M.txt")
    read_file_end_time = time.time()

    calc_adapt_seq_start_time = time.time()
    adapt_seq = brute_force_t4(lines, longest, adapter_threshold, adapter_suffix_threshold)
    calc_adapt_seq_end_time = time.time()
    # build tree
    a_reversed = adapt_seq[::-1] + "$"
    match_fragments_start_time = time.time()
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    map = task_four_distribution(lines, tree, longest)
    match_fragments_end_time = time.time()

    print("\nAdapter threshold: " + str(adapter_threshold) + "%")
    print("Adater suffix threshold: " + str(adapter_suffix_threshold) + "%")
    print("Most likely adapt sequence: " + adapt_seq)
    print("______________________________________________")



    print("\nTime used in seconds:")
    print("Read file time:                " + str(read_file_end_time - read_file_start_time))
    print("Calculate adapt sequence time: " + str(calc_adapt_seq_end_time - calc_adapt_seq_start_time))
    print("Match fragments time:          " + str(match_fragments_end_time - match_fragments_start_time))


def task4_analyze_seqset3():
    print("\n\n#####seqset3.txt######")
    read_file_start_time = time.time()
    lines, longest = read_file("../data/s_3_sequence_1M.txt")
    read_file_end_time = time.time()

    calc_adapt_seq_start_time = time.time()
    adapt_seq = brute_force_t4(lines, longest, adapter_threshold, adapter_suffix_threshold)
    calc_adapt_seq_end_time = time.time()
    # build tree
    a_reversed = adapt_seq[::-1] + "$"
    match_fragments_start_time = time.time()
    tree = SuffixTree(a_reversed)
    tree.build_suffix_tree()
    map = task_four_distribution(lines, tree, longest)
    match_fragments_end_time = time.time()

    print("\nAdapter threshold: " + str(adapter_threshold) + "%")
    print("Adater suffix threshold: " + str(adapter_suffix_threshold) + "%")
    print("Most likely adapt sequence: " + adapt_seq)
    print("______________________________________________")

    print("\nTime used in seconds:")
    print("Read file time:                " + str(read_file_end_time - read_file_start_time))
    print("Calculate adapt sequence time: " + str(calc_adapt_seq_end_time - calc_adapt_seq_start_time))
    print("Match fragments time:          " + str(match_fragments_end_time - match_fragments_start_time))



if __name__ == '__main__':
    task4_read_unkown_adapt()
    # REMAINDING TASKS

    # Does the unique set contain any
    # other common (proper) suffix patterns? Such additional common suffixes could
    # indicate bias in the sequencing experiment.
    #  Reuse algorithm on my new set?

    # Does the set in
    # s_3_sequence_1M.txt.gz contain additional common suffix patterns?
    # Same as above
    #
    # What
    # sequence does your algorithm return if you use your algorithm to analyze the files
    # s_3_sequence_1M.txt.gz and Seqset3.txt.gz?
    # just use algorithm and see what it returns?
    task4_analyze_set_1M()
    task4_analyze_seqset3()


