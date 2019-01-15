import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import seaborn as sns

import pickle # TODO : remove after tali haran data as been processed.

from src.analyzers.analyzer import Analyzer
from src.utils.content import Content


class VariantDistributionAnalyzer(Analyzer):
    name = "variant distribution analyzer"

    def __init__(self):
        pass

    def analyze(self, library_reads, library_design):
        if not library_reads.did_matching():
            print("You can not preform variant distribution analysis on a library that did not do matching.")
            return
        # Get library reads dataframe.
        reads_df = library_reads.get_df_copy()

        # Get variant id series and remove the rows where variant id is unknown.
        variants_ser = reads_df['variant_id']
        matched_variants_ser = variants_ser.where(variants_ser != -1).dropna()

        # Count the number of reads each variant has.
        variants_count = matched_variants_ser.value_counts().sort_index()

        # save data.
        return self.generate_content({'variants_count': variants_count})

    @staticmethod
    def generate_content(data):
        variants_count = data['variants_count']
        if len(variants_count) > 15000:
            var_distribution_data = variants_count.sample(15000)
        else:
            var_distribution_data = variants_count

        # Generating the number of reads per variant graph.
        plt.title("Number of reads per variant (sorted).")
        plt.xlabel("Variant Rank")
        plt.ylabel("Number of reads.")

        plt.ylim(0, np.max(var_distribution_data) + 2)
        sorted_data = np.flipud(np.sort(var_distribution_data.values))
        plt.bar(np.arange(len(sorted_data)), sorted_data, edgecolor=sns.color_palette()[0]) # Edge color solution is a bit hacky but I don't have a better idea.

        plt.savefig("temp/variant_distribution.png")
        plt.clf()

        # Adding the unmatched reads
        # unmatched_count = library_reads.get_unmatched_reads_count()
        # count_with_unmatched = np.concatenate((counts, [-1] * unmatched_count))

        # Generating the number of reads distribution.
        plt.title("Reads distribution")
        plt.xlabel("Number of Reads")
        plt.ylabel("Number of Variants")

        # Set the number of bins to the number of distinct values.
        bins = len(set(variants_count.values))

        # Set the y-axis range. (otherwise ymax is the len of the data and the values ares almost invisible).
        most_common, num_most_common = Counter(variants_count.values).most_common(1)[0]
        print("Most common value is {} and it appeared {} times".format(most_common, num_most_common))
        plt.ylim(0, num_most_common + 1000)

        labels, counts = np.unique(variants_count.values, return_counts=True)
        plt.bar(labels, counts, align='center')
        plt.gca().set_xticks(labels)

        # TODO : Remove after tali haran data as been processed.
        with open('labels.pkl', 'wb') as fid:
            pickle.dump(labels, fid)

        with open('counts.pkl', 'wb') as fid:
            pickle.dump(counts, fid)

        plt.savefig("temp/variant_read_distribution.png")
        plt.clf()

        content = [Content(Content.Type.TEXT, "Variants Distribution"),
                   Content(Content.Type.IMAGE, "temp/variant_distribution.png"),
                   Content(Content.Type.IMAGE, "temp/variant_read_distribution.png")]

        return content

