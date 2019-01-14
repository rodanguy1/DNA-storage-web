import re
DELETION = "1"
INSERTION = "2"
MISMATCH = "3"

CIGAR_DICT = {
    "=" : "0",
    "I" : INSERTION,
    "D" : DELETION,
    "X" : MISMATCH
}


def get_reverse_compliment(sequence):
    bases_compliment = {
        "A": "T",
        "T": "A",
        "G": "C",
        "C": "G"
    }

    reverse = sequence[::-1]
    reverse_compliment = [bases_compliment[x] for x in reverse]
    return "".join(reverse_compliment)


def get_fastq_sequnces(path_to_file, nrows):
    sequences = []
    with open(path_to_file) as fastq_file:
        line = fastq_file.readline()
        while line:
            # do something
            line = fastq_file.readline()
            if re.match("[ACGT]+\Z", line[:-1]):
                sequences.append(line[:-1])
                if nrows != -1 and len(sequences) >= nrows:
                    return sequences

    return sequences


def parse_cigar(path):
    values = re.findall(r'\d+', path)
    chars = re.findall(r'[=IDX]', path)


    str = ""
    for val, char in zip(values, chars):
        tmp = CIGAR_DICT[char]*int(val)
        str += tmp

    return str