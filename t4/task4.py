# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import matplotlib.pyplot as plt


A = 0
T = 1
G = 2
C = 3
adapter_threshold = 60
adapter_suffix_threshold = 90

def read_file_dict(filename):
    f = open(filename, 'r')
    lines = {}
    nr = 0
    for l in f:
        break
        lines[nr] = l.strip('\n')
        nr += 1
        if nr == 2:
            break
    f.close()
    # line1="AGACCGCCTGGGAATACCGGGTGCTGTAGGCTTAGATCGGAAGAGCACACGTCTGAACTCCAGTCACGTAGAGATCTCGTATGCCGTCTTCTGCTTGAA"
    # line2="ATGTAGGTAAGGGAAGTCGGCAAGCCGGATCCGTAACTTCGGGAGATCGGAAGAGCACACGTCTGAACTCCAGTCACGTAGAGATCTCGTATGCCGTCTTCTGCTTGA"
    # line3="AAACCGATACCATTACTGAGTAGATCCGAAGAGCA"
    # line4 ="CGACTCTTAGAAGATCGGAAGAGCACACGTCTGAACTCCAGTCACGTAGAGATCTCGTATGCCGTCTTCTGCTTGAAAAAAAAAAAAGATCGGAAGAGCACACGTCTAAACTCCAGTCAC"
    # lines[nr] = line1
    # nr +=1
    #
    # lines[nr] = line2
    # nr +=1
    #
    # lines[nr] = line3
    # nr +=1
    #
    # lines[nr] = line4
    # nr +=1
    #
    return lines

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
        #if counter == 10 000:
        #    break

    f.close()
    print("File closed")
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


def brute_force():
    lines, longest = read_file("../data/tdt4287-unknown-adapter.txt")
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
    # long string: A G C T A G
    # short string:      T A G
    # array:
    #              0 1 2 3 4 5
    #                1 1 2 2 2
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

def print_hi(name):
    adapt_seq = brute_force()
    print("Most likely adapt sequence")
    print(adapt_seq)


if __name__ == '__main__':
    print_hi('YO')

