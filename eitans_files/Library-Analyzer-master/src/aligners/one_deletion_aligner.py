from barcode_aligner import BarcodeAligner
import edlib

DEFAULT_DISTANCE = 1

class OneEditAligner (BarcodeAligner):
    def __init__(self, library_design, data):
        super(OneEditAligner, self).__init__(library_design, data)
        self.library_design = library_design

        if data.distance:
            allowed_distance = data.distance
        else :
            allowed_distance = DEFAULT_DISTANCE

        self.allowed_distance = allowed_distance



    def align_variant_to_read(self, read):
        reads = self.extract_barcode(read)

        if isinstance(reads, str):
            reads = [reads]

        optional = []
        for read in reads:
            for var in self.variant_barcodes:
                pass

if __name__ == "__main__":
    print edlib.align("CCGGTT", "GG", task="path", mode='HW')

