from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
from src.analyzers.deletion_analyzer import DeletionAnalyzer
from src.utils.content import Content


class DeletionPositionPerBaseAnalyzer (DeletionAnalyzer):

    # Will store the number of deletions for each base.
    base_deletion = {}

    name = "Deletion position per base analyzer"
    def __init__(self, data):
        super(DeletionAnalyzer, self).__init__()
        self.base_deletion = {
            'A': 0,
            'G': 0,
            'C': 0,
            'T': 0
        }

        self.longest_read_length = data['longest_sequence']

        for key in self.base_deletion:
            self.base_deletion[key] = np.zeros(self.longest_read_length)

    def analyze(self, library_reads, library_design):
        if not library_reads.did_edit_distance():
            print("You can perform deletion analyzing on reads that did not go through edit distance")
            return None

        # Get all the reads we managed to match.
        matched_reads = library_reads.get_matched_reads()
        print("Number of matched reads = {}".format(len(matched_reads)))

        bar = self.get_progress_bar(len(matched_reads))
        for read in matched_reads:
            # TODO find a better name.
            query_target_path = read.get_cigar_path()
            variant = library_design.get_variant_by_read(read)

            # Update Deletion counts
            self.update_deletion(query_target_path, variant())

            # # Update progress
            bar.next()

        bar.finish()

        # Dividing each position by the amount of expected base in that position..
        letter_position = self.get_position_base_count(library_reads, library_design)
        for key, value in self.base_deletion.items():
            self.base_deletion[key] /= letter_position[key]

        return self.generate_content(letter_position)

    def __str__(self):
        return 'Per base deletion analyzer'

    def generate_content(self, letter_position):
        content_array = []
        colors = {
            "A": "#0099ff",
            "C": "#ff9900",
            "G": "#7fff99",
            "T": "#e60042"
        }

        headline = Content(Content.Type.TEXT, "Base Deletion Ratio Per Position")
        content_array.append(headline)

        for letter, deletion_position_rate in self.base_deletion.items():
            # Create scatter plot
            plt.xlabel("{}".format(letter))
            plt.ylabel("Deletion rate")
            sns.regplot(np.arange(len(deletion_position_rate)), deletion_position_rate, color=colors[letter], fit_reg=False)

            # Save scatter as image
            image_one_name = './temp/a_d_{}.png'.format(letter)
            print("\n*******************DEBUG: pwd is: ",str(os.getcwd()),"the dir temp exists: ",str(os.path.exists('./temp')))
            plt.savefig(image_one_name)
            plt.clf()

            # Create and add content
            image_one = Content(Content.Type.IMAGE, image_one_name)
            content_array.append(image_one)

        # Generate stacked bar graph for base position distribution.
        df = pd.DataFrame(letter_position)
        image_name = "stacked_letters.png"
        figure = df.plot(kind='bar', stacked=True).get_figure()
        figure.savefig(image_name)
        figure.clf()
        content_array.append(Content(Content.Type.IMAGE, image_name))

        return content_array

    def update_deletion(self, path, variant):
        deletion_indices = self.locate_deletion_locations(path)

        if len(deletion_indices) == 0:
            return

        for i in deletion_indices:
            self.base_deletion[variant[i]][i] += 1


    def get_position_base_count(self, library_reads, library_design):
        """
        Compute how many bases should ideally be in each position if all the reads where perfect.
        :param library_reads: 
        :param library_design: 
        :return: A dictionary with all the letters and for each letter an array where each index
        corresponds to a position and each value indicates how many of the base should be in that position. 
        """

        # Starting each array with ones,
        letter_position = {
            'A' : np.ones(self.longest_read_length),
            'G' : np.ones(self.longest_read_length),
            'T' : np.ones(self.longest_read_length),
            'C' : np.ones(self.longest_read_length)
        }

        df_copy = library_reads.get_df_copy()
        group_by_variant = df_copy.groupby('variant_id')

        for variant_id, group in group_by_variant:
            if variant_id == -1:
                continue

            num_of_reads = len(group)
            variant = library_design.get_variant_by_id(variant_id)
            # Converting variant sequence to a numpy string array for vectorization purposes.
            v_sequence = np.asarray(list(variant()))

            for letter in letter_position:
                letter_in_sequence = (v_sequence == letter)
                letter_in_sequence = letter_in_sequence * num_of_reads

                # Some variants are shorter which will cause a bug. This fixes the bug. yeah!
                sequence_length = len(v_sequence)
                letter_position[letter][:sequence_length] += letter_in_sequence

        return letter_position
