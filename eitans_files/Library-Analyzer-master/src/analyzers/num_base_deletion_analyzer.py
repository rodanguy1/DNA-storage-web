from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import edlib
import re

from src.analyzers.deletion_analyzer import DeletionAnalyzer

DELETION = "2"
INSERTION = "1"
MISMATCH = "3"

CIGAR_DICT = {
    "=" : "0",
    "I" : INSERTION,
    "D" : DELETION,
    "X" : MISMATCH
}


class CountBaseDeletionAnalyzer (DeletionAnalyzer):

    # Will store the number of deletions for each base.
    base_deletion = {}

    def __init__(self):
        super(DeletionAnalyzer, self).__init__()
        self.base_deletion = {
            'A' : 0,
            'G' : 0,
            'C' : 0,
            'T' : 0
        }

    def analyze(self, library_reads, library_design):
        if not library_reads.did_edit_distance:
            print("You can prefrom deletion analyzing on reads that did not go through edit distance")
            return None

        # Get all the reads we managed to match.
        matched_reads = library_reads.get_matched_reads()
        analyzed = 0

        print("Started Analyzing\n\t")
        for read in matched_reads:
            # TODO find a better name.
            query_target_path = read.get_cigar_path()
            variant = library_design.get_variant_by_read(read)

            # Update Deletion counts
            self.update_deletion(query_target_path, variant())

            # # Update progress
            analyzed += 1
            if analyzed % 1000 == 0:
                print("#", end=" ")
            if analyzed % 10000 == 0:
                print ("\n")

        print("\n")
        total_base_count = library_reads.get_total_matched_base_count()
        self.base_deletion = {k: float(v) / total_base_count for k,v in self.base_deletion.items()}

        self.conclude()

    def generate_content(self):
        for letter in self.base_deletion:
            pass

    def update_deletion(self, path, variant):
        deletion_indices = self.locate_deletion_locations(path)

        if len(deletion_indices) == 0:
            return

        for i in deletion_indices:
            self.base_deletion[variant[i]] += 1

    def conclude(self):
        for key, val in self.base_deletion.items():
            print ("{} deletion rate = {}".format(key, val))






if __name__ == "__main__":
    query = "CCAATATCCTTAGCTGATCACCCATATGCCCACTAAGTACCCGGAAGAGCGAATGGCGTAGTGCCATGTTCCTTATTGCCCGGGCCACAGTTGACATTAGATATGG"
    target = "CCAATATCCTTAGCTGATCACCCATATGCCCACTAAGTACCCGGAAGAGCGAATGGCGTAGTGCCGCAGCCACACACAGCAGGAGCAGAATTCGTGTCAACATGGGCATGTTCCTTATTGCCCGGGCCACAGTTGACATTAGATATGG"
    align = edlib.align(query,
                        target,
                        task="path")
    print("Query length = {}\t Target length = {}".format(len(query), len(target)))
    parse_cigar(align['cigar'])
    # print align['cigar']