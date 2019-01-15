# coding=utf-8
"""
This class represents the Oligo library.
We'll keep a reference for all the sequences and will enable easy quereing.
"""
#import edlib
import pandas as pd
import json

from src.library_reads.read import Read
from src.utils import biology

SEQUENCES_COLUMN = "sequence"
ID_COLUMN = "variant_id"


class LibraryReads(object):
    config = False
    original_sequences = []

    def __init__(self, data):
        if isinstance(data, list):
            seq_df = pd.DataFrame(data=data, columns=[SEQUENCES_COLUMN])
            self.original_sequences = data

        if isinstance(data, str):
            seq_df = pd.read_csv(data)

        if isinstance(data, pd.DataFrame):
            seq_df = data

        self.seq_df = seq_df

    def preprocess_reads(self, preprocessor):
        """
        Preprocessor the library reads with a certain preprocess procedure defined by the given object. 
        :param preprocessor: The object in charge of the preproccessing. Should have a process method which takes a 
        string and return a string or None if the read should be removed from the library.
        :return: No return.
        """

        # Process sequences
        print("Number of reads before preprocessing : {}".format(self.seq_df.shape[0]))
        self.seq_df[SEQUENCES_COLUMN] = \
            self.seq_df.apply(lambda row: preprocessor.process(row[SEQUENCES_COLUMN]), axis=1)

        # Remove nan values from the sequences column
        self.seq_df = self.seq_df.dropna(subset=[SEQUENCES_COLUMN])
        print("Number of reads after preprcoessing : {}".format(self.seq_df.shape[0]))

    # TODO I'm not sure this is the right place for this.
    # TODO Strong couplling between the reads and the matching might be better for an matching object to get this class.
    # TODO For now it stays!
    def match_sequences(self, matcher):
        """"
        This method matches each sequence in the library with an oligo using the supplied matcher.
        The matcher should implement a find_best_oligo_match function.
        """
        self.seq_df['variant_id'] = self.seq_df.apply(lambda row:  matcher.find_best_oligo_match(row['sequence']), axis=1)

        # Sorting the data by the variant id.
        self.seq_df = self.seq_df.sort_values('variant_id').reset_index(drop=True)

    def compute_edit_distance(self, library_design):
        if self.did_matching() is False:
            print("Can not compute edit distance for un matched library")
            return

        def generate_cigar_path(row):
            variant_id = row['variant_id']
            if variant_id == -1:
                return -1

            read_sequence = row['sequence']
            variant_sequence = library_design.get_variant_sequence(variant_id).upper()

            # Aligning the read and the variant. variant=query, read=target
            align = edlib.align(read_sequence, variant_sequence, task="path")

            # TODO find a better name.
            query_target_path = biology.parse_cigar(align['cigar'])
            return query_target_path

        self.seq_df['cigar_path'] = self.seq_df.apply(generate_cigar_path, axis=1)

    def save_library_state(self, name="library_reads.csv"):
        self.seq_df.to_csv(name)

    def get_unmatched_reads(self):
        unmatched_df = self.seq_df.loc[self.seq_df[ID_COLUMN] == -1]
        return [Read(row) for _, row in unmatched_df.iterrows()]

    def get_unmatched_reads_count(self):
        """
        :return: The number of unmatched reads in the library. 
        """
        unmatched = self.get_unmatched_dataframe()
        return unmatched.shape[0]

    def get_matched_reads_count(self):
        """
        :return: The number of unmatched reads in the library. 
        """
        matched = self.get_matched_dataframe()
        return matched.shape[0]

    def get_matched_reads(self):
        """
        Get all the matched sequences in the library.
        :return: A generator of the sequences (iterator object)
        """
        matched_df = self.get_matched_dataframe()
        return [Read(row) for _, row in matched_df.iterrows()]

    def iterate_matched_reads(self):
        matched_df = self.get_matched_dataframe()
        for _, row in matched_df.iterrows():
            yield Read(row)

    def get_total_matched_base_count(self):
        """
        Return the total number of bases among the matched reads.
        If we had 2 matched reads:"ACGT", "ACCGT" we return 9.
        :return: 
        """
        matched_df = self.get_matched_dataframe()
        return matched_df['sequence'].str.count("[A-Za-z]").sum()

    def did_matching(self):
        if 'variant_id' in self.seq_df.columns:
            return True

        return True

    def did_edit_distance(self):
        if 'cigar_path' in self.seq_df.columns:
            return True

        return False

    def set_config_file(self, file_name):
        with open(file_name) as f:
            self.config = json.load(f)

    def get_config_file(self):
        if self.config:
            return self.config

        return None

    def set_original_sequences(self, sequences):
        self.original_sequences = sequences.copy()

    def get_original_sequences(self):
        return self.original_sequences

    def get_df_copy(self):
        return self.seq_df.copy()

    def __len__(self):
        return self.seq_df.shape(0)

    def __iter__(self):
        for _, read in self.seq_df.iterrows():
            yield Read(read)

    # ***************************************************************** Private methods *******************************
    def get_matched_dataframe(self):
        return self.seq_df.loc[self.seq_df[ID_COLUMN] != -1]

    def get_unmatched_dataframe(self):
        return self.seq_df.loc[self.seq_df[ID_COLUMN] == -1]
