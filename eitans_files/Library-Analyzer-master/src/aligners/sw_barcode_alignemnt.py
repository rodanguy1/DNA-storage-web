from barcode_aligner import BarcodeAligner
from Bio import pairwise2

MATCH_SCORE = 1
MISMATCH_SCORE = -4
GAP_OPEN = -1
GAP_CONTINUE = -3
THRESHOLD = 7


class SwBarcodeAligner(BarcodeAligner):
    def __init__(self, library_design, data):
        super(SwBarcodeAligner, self).__init__(library_design, data)
        self.test = 0

    def align_variant_to_read(self, read):
        if self.test > 0:
            return -1

        self.test += 1

        potential = []
        for variant, index in self.variant_barcodes.iteritems():
            sw_alignment = pairwise2.align.localms(read[33:47].upper(), variant.upper(),
                                            MATCH_SCORE,
                                            MISMATCH_SCORE,-2,-2)
            alignment_score = sw_alignment[0][2]

            if alignment_score > THRESHOLD:
                potential.append((sw_alignment[0], index))

        print read
        for value in potential:
            print value

if __name__ == "__main__":
    align = pairwise2.align.localms("GGGCCGGG", "AAACCAAA", 1, -5, -5, -5)

    for a in align:
        print a
