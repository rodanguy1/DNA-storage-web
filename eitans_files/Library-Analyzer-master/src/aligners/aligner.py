# Todo : Might want to change the name of the function - looks like you need to send variant to align_variant_to_read
class Aligner(object):
    def __init__(self):
        # To support a cascading flow where one aligner can move candidates to the next we will use a candidates list.
        self.candidates = []
        pass

    def align_variant_to_read(self, read):
        print("This method must be implemented in the aligner class, otherwise the aligner has no meaning")
        return 0

    def set_candidates(self, candidates):
        self.candidates = candidates
