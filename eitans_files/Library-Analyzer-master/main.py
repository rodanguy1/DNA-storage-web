import time
from pathlib import Path
import sys
import os

from src.aligners.barcode_aligner import BarcodeAligner
from src.aligners.library_matcher import OligoMatcher
# from src.analyzers.deletion_analyzer import DeletionAnalyzer
from src.analyzers.deletion_position_per_base_analyzer import DeletionPositionPerBaseAnalyzer
from src.analyzers.general_analyzer import GeneralAnalyzer
from src.analyzers.reads_length_analyzer import ReadLengthAnalyzer
from src.analyzers.variant_distriution_analyzer import VariantDistributionAnalyzer
from src.library_design import library_design_loader
from src.library_design.library_design import LibraryDesign
from src.library_reads import library_loader
from src.library_reads.library_reads import LibraryReads
from src.library_reads.preprocessor import FixPreProcessor
from src.utils.pdf_generator import PDFGenerator
from utils.config import basedir
# Plotting setup
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

sns.set()
sns.set_palette('muted')
plt.rc("axes.spines", top=False, right=False)  # Remove top and right borders. Looks nicer.
mpl.rcParams['savefig.dpi'] = 300  # Save plot will be in a higher resolution.


# TODO move file names to another file.
class DatasetFiles(object):
    ZOHAR = "Twist_zohar"
    PART = "Twist_combined_first100k.fastq"

    SCHIRMAN_1 = "Nucleotide"
    SCHIRMAN_2 = "r_loops"
    SCHIRMAN_3 = "splicing"

    TALI = "tali"
    TALI_FOLDER = "/data/tali_data/"

    TOY = "toy_data"
    TOY_FOLDER = "data/toy_data/"
BASE_DIR = os.getcwd()+os.sep
if os.environ.get('mode') == 'prod':
    BASE_DIR = '/home/omersabary/DNA-storage-web/'
DATASET_FOLDER = DatasetFiles.TOY_FOLDER
DATASET_FILE = DatasetFiles.TOY

DATASET_READS_SUFFIX = "_reads.fastq"
DATASET_DESIGN_SUFFIX = "_design.csv"
DATASET_CONFIG_SUFFIX = "_config.json"

# A const to decide whether to use existing files or re calculate. [Matching and Alignment].
OVERRIDE = True
EDIT_DISTANCE = False
# An int to allow a smaller chunk of reads from the fastq file.
NREADS = -1


def get_library_reads_and_design(reads_file, design_file, override=False):
    print("\n| Setting up library design and reads object:")
    library_design_df = library_design_loader.load_oligo_design(design_file)
    library_design = LibraryDesign(library_design_df)
    print(" - Generated the design obj")

    read_file_noprefix = reads_file[:-12]
    aligned_file = Path("{}_after_alignment.csv".format(read_file_noprefix))
    matched_file = Path("{}_after_matching.csv".format(read_file_noprefix))
    config_file = Path(read_file_noprefix + DATASET_CONFIG_SUFFIX)

    sequences = library_loader.load_library(DATASET_FOLDER + DATASET_FILE + DATASET_READS_SUFFIX, True, NREADS)

    if aligned_file.exists() and not override:
        library_reads = LibraryReads(str(aligned_file))
    elif matched_file.exists() and not override:
        library_reads = LibraryReads(str(matched_file))
    else:
        library_reads = LibraryReads(sequences)

    if config_file.exists():
        library_reads.set_config_file(config_file)
        print(" - Config file set")
    else:
        assert 'Config file does not exist'

    # TODO need to find a cleaner way to do this. LibraryReads Save/Load should be upgraded.
    library_reads.set_original_sequences(sequences)

    print(" - Generated the reads obj")
    return library_reads, library_design


def get_library_reads_and_design_simple(design_file, read_metafile, config_file):
    library_design_df = library_design_loader.load_oligo_design(design_file)
    library_design = LibraryDesign(library_design_df)

    reads_file_names = get_filenames_from_file(read_metafile)
    sequences = library_loader.load_library(reads_file_names)

    library_reads = LibraryReads(sequences)
    print('DEBUG: the type of library_reads is' + str(type(library_reads)))
    library_reads.set_config_file(config_file)
    library_reads.set_original_sequences(sequences)

    return library_reads, library_design


def get_filenames_from_file(file_name):
    with open(file_name, 'r') as file:
        files_names = file.read().splitlines()

    return files_names


def preprocess_reads(library_reads):
    print("| preprocessing library reads")
    processor = FixPreProcessor(library_reads.get_config_file())
    library_reads.preprocess_reads(processor)


def match_reads_to_design(library_reads, library_design):
    print("\n| Matching reads to design")
    variant_matcher = OligoMatcher(library_design)

    config = library_reads.get_config_file()
    wanted_keys = ['barcode_start', 'barcode_end']

    aligner = BarcodeAligner(library_design, dict((k, config[k]) for k in wanted_keys if k in config))
    variant_matcher.add_aligner(aligner)

    library_reads.match_sequences(variant_matcher)
    library_reads.save_library_state("{}_after_matching.csv".format(DATASET_FOLDER + DATASET_FILE))

    matched_count = library_reads.get_matched_reads_count()
    un_matched_count = library_reads.get_unmatched_reads_count()
    print(" - Finished matching.")
    print(" -- managed to match - {}".format(matched_count))
    print(" -- % of successful match - {}".format(matched_count / (matched_count + un_matched_count)))


def align_reads_to_variants(library_reads, library_design):
    print("\n| Aligning reads to design")
    library_reads.compute_edit_distance(library_design)

    library_reads.save_library_state("{}_after_alignment.csv".format(DATASET_FOLDER + DATASET_FILE))
    print(" - Finished read alignment")


def analyze_library(library_reads, library_design, time_stamp=""):
    print("\n| Analyzing library")
    contents = []

    analyzers = [GeneralAnalyzer(),
                 ReadLengthAnalyzer(),
                 VariantDistributionAnalyzer()]
    # DeletionPositionPerBaseAnalyzer({'longest_sequence': library_design.get_design_longest_sequence()})]

    for analyzer in analyzers:
        contents.append(analyzer.analyze(library_reads, library_design))
        print(" - Finished with : {}".format(analyzer.name))

    with PDFGenerator("{}_report.pdf".format(time_stamp)) as pdf_gen:
        for content in contents:
            if content:
                pdf_gen.add_content_array(content)


if __name__ == "__main__":
    print("Running main")
    t_start = time.time()

    # Temporary images will be saved in the temp folder, if not temp folder exists we create one.
    if not os.path.isdir("temp"):
        os.makedirs("temp")

    time_stamp = ""
    if len(sys.argv) == 1:  # if no arguments are passed try to retrieve data from CONSTS.
        lr_obj, ld_obj = get_library_reads_and_design(DATASET_FOLDER + DATASET_FILE + DATASET_READS_SUFFIX,
                                                      DATASET_FOLDER + DATASET_FILE + DATASET_DESIGN_SUFFIX,
                                                      OVERRIDE)
    elif len(sys.argv) == 2:  # if we have on argument is the user_id
        DATASET_FOLDER = BASE_DIR+'input_files_dir' + os.sep
        DATASET_FILE = sys.argv[1]
        OVERRIDE = False
        time_stamp = sys.argv[1]
        lr_obj, ld_obj = get_library_reads_and_design(DATASET_FOLDER + DATASET_FILE + DATASET_READS_SUFFIX,
                                                      DATASET_FOLDER + DATASET_FILE + DATASET_DESIGN_SUFFIX,
                                                      OVERRIDE)

    else:  # Otherwise use supplied arguments to retrieve data.
        assert len(sys.argv) > 3, "You must supply 3 arguments : design file path, reads file path, config file path"
        design_file = sys.argv[1]
        reads_file = sys.argv[2]
        config_file = sys.argv[3]
        if len(sys.argv) == 5:
            time_stamp = sys.argv[4]

        lr_obj, ld_obj = get_library_reads_and_design_simple(design_file, reads_file, config_file)

    if not lr_obj.did_matching() or OVERRIDE:
        preprocess_reads(lr_obj)
        match_reads_to_design(lr_obj, ld_obj)

    if EDIT_DISTANCE and (not lr_obj.did_edit_distance() or OVERRIDE):
        align_reads_to_variants(lr_obj, ld_obj)

    # This delay fix a strange error. Probably something with reading from a file we just finished writing to.
    time.sleep(2)

    analyze_library(lr_obj, ld_obj, time_stamp)

    print("\n -(\) - Main test took : {} time.".format(time.time() - t_start))
