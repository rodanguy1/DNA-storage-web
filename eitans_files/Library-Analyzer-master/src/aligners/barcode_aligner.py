import numpy as np

from src.aligners.aligner import Aligner


class BarcodeAligner(Aligner):
    def __init__(self, library_design, data):
        super(BarcodeAligner, self).__init__()
        if not library_design.has_barcode():
            print ("The library design sent to barcode aligner has no barcode.")

        self.library_design = library_design

        self.data = data

        barcode_start = data['barcode_start']
        barcode_end = data['barcode_end']
        self.extract_barcode = lambda x: x[barcode_start:barcode_end]

        self.variant_barcodes = []
        self.set_candidates()

    def set_candidates(self, candidates=[]):
        self.variant_barcodes = self.get_library_design_barcodes(candidates)

        # TODO The cnadidates mechanism does not take the id's into account. Need to solve soon.
        # TODO this will not work with candidates.
        num_of_variants = len(self.variant_barcodes)
        variant_range = np.arange(num_of_variants)

        self.variant_barcodes = dict(zip(self.variant_barcodes[:], variant_range))

    def align_variant_to_read(self, read):
        reads = self.extract_barcode(read)
        if isinstance(reads, str):
            reads = [reads]

        for read in reads:
            val = self.variant_barcodes.get(read)
            if val is not None:
                return val

        return -1

    def get_library_design_barcodes(self, candidates=[]):
        return self.library_design.get_library_barcodes(candidates)



if __name__ == "__main__":
    pass
