""""
This file is used to load the library file.
In case we want to enable different file types and format this loader should return a standardized Data Frame.
Should we want to process the file (drop columns, change upeer/lower etc..) these pre processing
events should happen here.
"""

import pandas as pd
from src.utils import biology


def load_library(file, as_df=True, n_reads=-1):
    if isinstance(file, list):
        sequences = []
        for file_name in file:
            sequences.extend(biology.get_fastq_sequnces(file_name, n_reads))
            print(" - Got sequences from {}".format(file_name))
    else:
        sequences = biology.get_fastq_sequnces(file, n_reads)

    if as_df:
        return pd.DataFrame(sequences, columns=['sequence'])
    else:
        return sequences
