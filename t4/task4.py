# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import matplotlib.pyplot as plt
from suffix_tree import *
from suffix_tree import Tree
from suffix_tree import ukkonen_gusfield

from suffix_tree import ukkonen

from suffix_tree import naive
from enum import Enum


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

def read_file(filename):
    f = open(filename, 'r')
    lines = []
    longest = 0
    counter = 0
    while True:
        line = f.readline()
        if len(line) > longest:
            longest = len(line)
        if not line:
            break
        else:
            lines.append(line)
    f.close()
    return lines, longest

def brute_force_adapter_sequence(array, longest):
    A = 0
    T = 1
    G = 2
    C = 3
    for i in range(0, longest):
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
        print("For index: " + str(i) + " most likely is " + current_most_likely + " with a percentage of " + str(current_most_likely_number/total*100))



def brute_force():
    lines, longest = read_file("../data/tdt4287-unknown-adapter.txt")
    print(longest)
    # two dim array with longest * 4.
    A = 0
    T = 1
    G = 2
    C = 3
    array = [[0 for x in range(4)] for y in range(longest)]
    for sequence in lines:
        seq_length = len(sequence)-1
        if seq_length == 120:
            print("")
        for i in range(0, seq_length):
                if sequence[i] == 'A':
                    array[longest-seq_length+i-1][A] += 1

                elif sequence[i] == 'T':
                    array[longest-seq_length+i-1][T] += 1

                elif sequence[i] == 'G':
                    array[longest-seq_length+i-1][G] += 1

                else:
                    array[longest-seq_length+i-1][C] += 1


    print("done")
    brute_force_adapter_sequence(array, longest)

def print_hi(name):
    # lines = read_file_dict("../data/tdt4287-unknown-adapter.txt")
    # tree = Tree(lines, naive.Builder)
    # cmn_sub = tree.common_substrings()
    brute_force()





# b = Builder.ukkon
    #tree.add()
# d   : dict = lines,
#              builder: Type[Builder] = ukkonen.Builder) -> None

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('YO')

