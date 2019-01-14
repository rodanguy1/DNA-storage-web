from progress.bar import Bar


class Analyzer(object):
    def __init__(self):
        pass

    def analyze(self, library_reads, library_design):
        """
        Analyzes a certain criteria of the library
        :param library_reads: A Library reads object.
        :return: A content object which can be used to visualize the analysis.
        """
        print("This method should be implemented by the analyzer object.")
        return False

    def get_progress_bar(self, length):
        return Bar('{} Analyzing'.format(str(self)), max=length)

    def __str__(self):
        return "Analyzer"
