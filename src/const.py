import os

ENV_MATLAB_KEY = 'matlab'

CONFIG_PATH_RELATIVE_OUTPUT = 'pathRelativeOutput'
CONFIG_PROGRAM_FILE = 'programFile'
CONFIG_RECONSTRUCT_SCORING_METHOD = 'scoringMethod'
CONFIG_RECONSTRUCT_CHOOSING_METHOD = 'choosingMethod'
CONFIG_PARSING_METHOD = 'parsingMethod'
CONFIG_SIMULATION_BIALLELIC = 'biallelic'

FILE_SIMULATION_XML = 'simulation.xml'
FILE_SIMULATION_NEWICK = 'simulation.newick'
FILE_RECONSTRUCTED_NEWICK = 'reconstructed.newick'
FILE_RECONSTRUCTED_TMP_NEWICK = 'reconstructed.tmp.newick'
FILE_TRIPLETS_LIST_RAW = 'triplets-list.raw.txt'
FILE_TRIPLETS_LIST_CSV = 'triplets-list.csv'
FILE_TRIPLETS_LIST_ID_NAME_CSV = 'triplets-list.id-name.csv'
FILE_TMC_LOG = 'tmc.log'
FILE_MUTATION_TABLE = 'mutation_table.txt'
FILE_RECONSTRUCTED_PNG = 'reconstructed.png'
FILE_COMPARISON_METRICS_RAW = 'scores.raw.out'
FILE_COMPARISON_METRICS_PRETTY = 'scores.pretty.out'
FILE_DIFF_METRICS = 'diff-score.json'
FILE_REPORT_HTML = 'report.html'
FILE_SISTERS_COUNT = 'sisters.csv'

FILE_CONFIG_GENOTYPING = 'config.genotyping.yml'

PATH_SIMULATION_LIB = './src/simulation'
PATH_RECONSTRUCT_LIB = './src/reconstruction'
PATH_ESTGT_GIT = './bin/eSTGt'
PATH_ESTGT_BIN = os.path.join(PATH_ESTGT_GIT, 'eSTGt')
PATH_TREECMP_BIN = './bin/TreeCmp/bin/treeCmp.jar'
PATH_TMC_BIN = './bin/TMC/treeFromTriplets'

# position in the run_flag array that is constructed by argparse
FLAG_TREE_SIMULATION = 0
FLAG_GENOTYPING = 1
FLAG_RECONSTRUCTION = 2

FLAG_RUN_TREE_SIMULATION = '0'
FLAG_SKIP_TREE_SIMULATION = '1'
FLAG_ONLY_TREE_SIMULATION = '2'

FLAG_RUN_GENOTYPING = '0'
FLAG_SKIP_GENOTYPING = '1'

FLAG_RUN_RECONSTRUCTION = '0'
FLAG_SKIP_RECONSTRUCTION = '1'
