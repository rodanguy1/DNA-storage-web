""""
This file is used to load the oligo design file.
In case we want to enable different file types and format this loader should return a standardized Data Frame.
Should we want to process the file (drop columns, change upeer/lower etc..) these pre processing
events should happen here.
"""

# Imports
import pandas as pd


def load_oligo_design(file):
    """
    Reads the given file name into a pandas dataframe, returns the dataframe.
    :param file: The file name from which to build the dataframe.
    :return: A Dataframe containing the data in the file.
    """
    oligo_df = pd.read_csv(file)
    return oligo_df
