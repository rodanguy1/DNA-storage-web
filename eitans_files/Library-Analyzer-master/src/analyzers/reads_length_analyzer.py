import matplotlib.pyplot as plt
import numpy as np

from src.analyzers.analyzer import Analyzer
from src.utils.content import Content


class ReadLengthAnalyzer(Analyzer):
    name = "Read length analyzer"
    def analyze(self, library_reads, library_design):
        if not library_reads.did_matching():
            print("You can not preform variant distribution analysis on a library that did not do matching.")
            return

        sequences = library_reads.get_original_sequences()
        content_data = sequences['sequence'].str.len()

        print(np.where(content_data is None))

        return self.generate_content(content_data)

    @staticmethod
    def generate_content(data):
        plt.title("Reads Length histogram")
        plt.xlabel("Length")
        plt.ylabel("Number of reads")

        plt.hist(data, bins=50)
        plt.savefig("temp/reads_length_histogram.png")

        plt.clf()

        return [Content(Content.Type.TEXT, "Reads length distribution"),
                Content(Content.Type.IMAGE, "temp/reads_length_histogram.png")]