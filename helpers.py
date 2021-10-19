A = "TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG"


def read_file(filename: str = ".\\data\\s_3_sequence_1M.txt"):
    with open(filename, "r") as f:
        return f.readlines()
