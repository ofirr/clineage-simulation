import os
import json
import argparse
import re
import yaml
import pandas as pd

from src import const
from src import utils
from record_versions import record_versions

from genotyping import run_genotyping_simulation
from reconstruct import normalize_triplet_dist, calculate_triplets_tree, simplified_triplets_calculation

import sys
sys.path.append("/home/{}/clineage/".format(os.environ['USER']))
import clineage.wsgi


def generate_tree_ascii_plot(path_newick):

    import dendropy

    # read simulation.newick
    tree = dendropy.Tree.get_from_path(path_newick, "newick")

    # write ascii plot for simulation tree
    with open('{}.ascii-plot.txt'.format(path_newick), 'wt') as fout:
        fout.write(tree.as_ascii_plot())
        fout.write('\n')


def simulate_lineage_tree(path_matlab, path_project, config_filename):
    "run stochastic lineage tree simulation"

    # run MATLAB simulation
    matlab_code = "addpath('{0}', '{1}', '{2}'); run_simul('{2}', '{3}'); exit;".format(
        const.PATH_ESTGT_BIN, const.PATH_SIMULATION_LIB, path_project, config_filename
    )

    utils.run_matlab_code(path_matlab, matlab_code)


def handle_monoallelic(path_project, path_simulation_output):

    from sequencing.phylo.triplets_wrapper import parse_mutations_table

    methods = []

    path_genotyping_config = os.path.join(
        path_project, const.FILE_CONFIG_GENOTYPING
    )

    # if config doesn't exist, mutation_table.txt that came out of eSTGt
    # as the final calling
    if not os.path.exists(path_genotyping_config):

        # construct path for input mutation table
        path_mutation_table = os.path.join(
            path_simulation_output, const.FILE_MUTATION_TABLE
        )

        # parse mutation table
        calling = parse_mutations_table(
            path_mutation_table,
            inverse=True
        )

        methods.append((path_simulation_output, calling))

    else:

        with open(path_genotyping_config, 'rt') as stream:
            params_list = yaml.load(stream)

        for case, params in enumerate(params_list["genotyping"]):

            path_genotype_simulation_output = os.path.join(
                path_simulation_output,
                "n-{0:06d}".format(params.get('n'))
            )

            calling = parse_mutations_table(
                os.path.join(
                    path_genotype_simulation_output,
                    const.FILE_MUTATION_TABLE
                ),
                inverse=True
            )

            methods.append((path_genotype_simulation_output, calling))

    return methods


def handle_biallelic(parsingMethod, path_project, path_simulation_output):

    from biallelic import get_method
    method = get_method(parsingMethod)

    methods = []

    path_genotyping_config = os.path.join(
        path_project, const.FILE_CONFIG_GENOTYPING
    )

    if not os.path.exists(path_genotyping_config):
        return methods

    with open(path_genotyping_config, 'rt') as stream:
        params_list = yaml.load(stream)

    for case, params in enumerate(params_list["genotyping"]):
        path_genotype_simulation_output = os.path.join(
            path_simulation_output,
            "n-{0:06d}".format(params.get('n'))
        )

        calling = method(
            os.path.join(
                path_genotype_simulation_output,
                const.FILE_MUTATION_TABLE
            )
        )

        methods.append((path_genotype_simulation_output, calling))

    return methods


def run_triplet_maxcut(path_triplets_file, path_output_newick, path_tmc_log):

    class EmptyTripletsFile(Exception):
        pass

    if os.stat(path_triplets_file).st_size == 0:
        raise EmptyTripletsFile('Empty file: {}'.format(path_triplets_file))

    import tempfile
    import subprocess

    cmd = [
        os.path.abspath(const.PATH_TMC_BIN),
        '-fid',
        path_triplets_file,
        '-frtN',
        path_output_newick,
        '-flg',
        path_tmc_log,
        '-w', '1',
        '-index', '2'
    ]

    # create a temporary working directory for TMC
    with tempfile.TemporaryDirectory() as path_tmc_work:

        print('TMC work directory: {}'.format(path_tmc_work))

        # TMC creates a treeReconstructio.log in the current working directory
        process = subprocess.Popen(cmd, cwd=path_tmc_work)

        return process.wait()


def reconstruct_TMC(calling, path_simulation_output, root_cell_notation, scoring_method, choosing_method, quiet=True):

    from sequencing.phylo.triplets_wrapper import convert_names_in_sagis_newick

    # construct path for final reconstructed newick
    # this one will have the actual cell name
    path_reconstructed_newick = os.path.join(
        path_simulation_output, const.FILE_RECONSTRUCTED_NEWICK
    )

    # construct path for temporary reconstructed newick
    # this one will have the numeric ids instead which correspond to the actual cell names
    path_reconstructed_tmp_newick = os.path.join(
        path_simulation_output, const.FILE_RECONSTRUCTED_TMP_NEWICK
    )

    # construct path for triplets list
    path_triplets_list_raw = os.path.join(
        path_simulation_output, const.FILE_TRIPLETS_LIST_RAW
    )
    path_triplets_list_id_name_csv = os.path.join(
        path_simulation_output, const.FILE_TRIPLETS_LIST_ID_NAME_CSV
    )

    # create triplets list using given parameters
    rldr = [root_cell_notation]  # cf. 'Ave'
    cell_id_map_for_sagi = simplified_triplets_calculation(
        textual_mutation_dict=calling,
        triplets_file=path_triplets_list_raw,
        triplets_generator_name='splitable', # mono_cases: mono  bi_cases: splitable/full_bi
        score_threshold=0,
        choosing_method=choosing_method,
        scoring_method=scoring_method,
        printscores=True,
        loci_filter="ncnr",
        sabc=0,
        tripletsnumber=5000000  # basically, max num of triplets
    )

    # construct easy triplet lookup table (id to cellname)
    df_mapping = pd.DataFrame.from_dict(cell_id_map_for_sagi, orient='index')
    df_mapping = df_mapping.reset_index() \
        .set_index(0) \
        .rename(columns={'index': 'cellname'})
    df_mapping.index.name = 'index'
    df_mapping.to_csv(path_triplets_list_id_name_csv)

    # normalize triplet distance if uri10
    # if scoring_method == 'uri10':
    #     normalize_triplet_dist(path_triplets_list_raw)

    # construct path for tmc log
    path_tmc_log = os.path.join(
        path_simulation_output, const.FILE_TMC_LOG
    )

    # run sagis triplets binary
    # the output newick will have the numeric ids which correspond to the actual cell names
    ret_code = run_triplet_maxcut(
        path_triplets_list_raw,
        path_reconstructed_tmp_newick,
        path_tmc_log
    )

    # convert the numeric ids in newick to the actual cell names
    convert_names_in_sagis_newick(
        path_reconstructed_tmp_newick,
        path_reconstructed_newick,
        cell_id_map_for_sagi
    )

    import dendropy

    # load reconstructed tree
    tree_reconstructed = dendropy.Tree.get_from_path(
        path_reconstructed_newick,
        "newick"
    )

    # prune root
    root_node = tree_reconstructed.find_node_with_taxon_label(
        root_cell_notation
    )
    if root_node:
        tree_reconstructed.prune_subtree(root_node)

    # re-save the newick after eliminating quotes around taxa labels
    tree_reconstructed.write_to_path(
        path_reconstructed_newick, schema='newick', unquoted_underscores=True
    )

    # get the number of sisters for each node
    from ete3 import Tree
    with open(path_reconstructed_newick, 'rt') as fin:
        newick = fin.read()
        ete_tree = Tree(newick)
        sisters = []
        for n in ete_tree.get_leaves():
            sisters.append([n.name, len(n.get_sisters())])
        df = pd.DataFrame(sisters, columns=['cell_name', 'num_sisters'])
        df.to_csv(
            os.path.join(path_simulation_output, const.FILE_SISTERS_COUNT),
            index=False
        )


# deprecated
def plot_recontructed_tree(path_matlab, path_simulation_newick, path_reconstructed_newick, path_png):

    matlab_code = "addpath('{0}', '{1}'); plot_reconstructed_tree('{2}', '{3}', '{4}'); exit;".format(
        const.PATH_ESTGT_BIN, const.PATH_RECONSTRUCT_LIB, path_simulation_newick, path_reconstructed_newick, path_png
    )

    utils.run_matlab_code(path_matlab, matlab_code)


def highlight_tree_differences_to_png(path_matlab, path_simulation_newick, path_reconstructed_newick, path_sisters_csv, path_diff_metrics):

    matlab_code = "addpath('{0}', '{1}'); highlight_differences2('{2}', '{3}', '{4}', '{5}'); exit;".format(
        const.PATH_ESTGT_BIN, const.PATH_RECONSTRUCT_LIB,
        path_simulation_newick, path_reconstructed_newick, path_sisters_csv, path_diff_metrics
    )

    utils.run_matlab_code(path_matlab, matlab_code)


def compare(path_simulation_newick, path_reconstructed_newick, path_score_output):

    #  Metrics for rooted trees
    metrics = {
        "rooted": "mc rc ns tt mp mt co",
        "unrooted": "ms rf pd qt um"
    }

    cmd = [
        'java', '-jar', const.PATH_TREECMP_BIN,
        '-P', '-N', '-I'
        '-r', path_simulation_newick,
        '-i', path_reconstructed_newick,
        '-o', path_score_output,
        '-d'
    ]

    cmd.extend(metrics['rooted'].split(' '))

    utils.run_command(cmd)


def report(path_scores_output_raw, path_scores_output_pretty, quiet=True):

    # read the first two lines that contain various metrics
    df_metrics = pd.read_csv(path_scores_output_raw, sep='\t', nrows=1)

    # transpose and rename the column to 'metrics'
    df_metrics = df_metrics.T.rename(columns={0: 'metrics'})

    # read the summary section
    df_summary = pd.read_csv(path_scores_output_raw, sep='\t', skiprows=4)

    if not quiet:
        # display to the screen
        print(df_metrics)
        print()
        print(df_summary)

    with open(path_scores_output_pretty, 'wt') as fout:
        fout.write(df_metrics.to_string())
        fout.write('\n')
        fout.write('\n')
        fout.write(df_summary.to_string())
        fout.write('\n')


def get_seed_from_simulation_xml(path_xml):

    from lxml import etree

    parser = etree.XMLParser(remove_blank_text=True)
    xdoc = etree.parse(path_xml, parser=parser)
    seed = int(xdoc.xpath('./ExecParams/Seed')[0].text.strip())

    return seed


def run(path_matlab, path_project, config_filename, run_flag, quiet):
    "run function"

    # read simulation configuration
    config = utils.read_json_config(
        os.path.join(path_project, config_filename)
    )

    # get seed from simulation.xml
    seed = get_seed_from_simulation_xml(
        os.path.join(
            path_project,
            config.get(const.CONFIG_PROGRAM_FILE, const.FILE_SIMULATION_XML)
        )
    )

    path_simulation_output = os.path.join(
        path_project, config[const.CONFIG_PATH_RELATIVE_OUTPUT]
    )

    if run_flag[const.FLAG_TREE_SIMULATION] == const.FLAG_RUN_TREE_SIMULATION or run_flag[const.FLAG_TREE_SIMULATION] == const.FLAG_ONLY_TREE_SIMULATION:
        # run stochastic lineage tree simulation
        simulate_lineage_tree(
            path_matlab, path_project, config_filename
        )

        # take simulation tree and make ascii plot
        generate_tree_ascii_plot(
            os.path.join(path_simulation_output, const.FILE_SIMULATION_NEWICK)
        )

    # user wants to generate tree only
    if run_flag[const.FLAG_TREE_SIMULATION] == const.FLAG_ONLY_TREE_SIMULATION:
        return

    if run_flag[const.FLAG_GENOTYPING] == const.FLAG_RUN_GENOTYPING:
        # run genotyping simulation (wga proportion, dropout, coverage)
        # output mutation table
        run_genotyping_simulation(
            config.get(const.CONFIG_SIMULATION_BIALLELIC, False),
            path_project,
            path_simulation_output,
            seed
        )

    if run_flag[const.FLAG_RECONSTRUCTION] == const.FLAG_SKIP_RECONSTRUCTION:
        return

    methods = []

    # if biallelic=true
    if config.get(const.CONFIG_SIMULATION_BIALLELIC, False):
        methods = handle_biallelic(
            # use 'A' by default for backward compatibility
            config.get(const.CONFIG_PARSING_METHOD, 'A'),
            path_project,
            path_simulation_output
        )
    else:
        methods = handle_monoallelic(
            path_project,
            path_simulation_output
        )

    for path_reconstruction_output, calling in methods:

        # reconstruct using TMC based on mutation table generated from simulation
        reconstruct_TMC(
            calling,
            path_reconstruction_output,
            'root',
            # use 'uri10' by default for backward compatibility
            config.get(const.CONFIG_RECONSTRUCT_SCORING_METHOD, 'uri10'),
            # use 'mms' by default for backward compatibility
            config.get(const.CONFIG_RECONSTRUCT_CHOOSING_METHOD, 'mms'),
            quiet
        )

        # take reconstructed tree and make ascii plot
        generate_tree_ascii_plot(
            os.path.join(path_reconstruction_output,
                         const.FILE_RECONSTRUCTED_NEWICK)
        )

        # highlight tree differences and save to png
        highlight_tree_differences_to_png(
            envs[const.ENV_MATLAB_KEY],
            os.path.join(path_simulation_output,
                         const.FILE_SIMULATION_NEWICK),
            os.path.join(path_reconstruction_output,
                         const.FILE_RECONSTRUCTED_NEWICK),
            os.path.join(path_reconstruction_output, const.FILE_SISTERS_COUNT),
            os.path.join(path_reconstruction_output, const.FILE_DIFF_METRICS)
        )

        # compare simulation tree and reconstructed tree
        compare(
            os.path.join(
                path_simulation_output, const.FILE_SIMULATION_NEWICK
            ),
            os.path.join(
                path_reconstruction_output,
                const.FILE_RECONSTRUCTED_NEWICK
            ),
            os.path.join(
                path_reconstruction_output,
                const.FILE_COMPARISON_METRICS_RAW
            )
        )

        # report the final comparison metrics in a pretty format
        report(
            os.path.join(
                path_reconstruction_output,
                const.FILE_COMPARISON_METRICS_RAW
            ),
            os.path.join(
                path_reconstruction_output,
                const.FILE_COMPARISON_METRICS_PRETTY
            ),
            quiet
        )


def parse_arguments():

    parser = argparse.ArgumentParser(description='run simulation')

    parser.add_argument(
        "--env",
        action="store",
        dest="path_env",
        required=True
    )

    parser.add_argument(
        "--project",
        action="store",
        dest="path_project",
        required=True
    )

    parser.add_argument(
        "--config",
        nargs='+',
        dest="configs",
        required=True
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        dest="quiet"
    )

    parser.add_argument(
        "--run-flag",
        nargs=3,
        default=[const.FLAG_RUN_TREE_SIMULATION,
                 const.FLAG_RUN_GENOTYPING, const.FLAG_RUN_RECONSTRUCTION],
        dest="run_flag"
    )

    # parse arguments
    params = parser.parse_args()

    # read environment configuration
    envs = utils.read_json_config(params.path_env)

    # get config json files
    config_jsons = utils.handle_config_args(
        params.path_project, params.configs
    )

    return params, envs, config_jsons


if __name__ == "__main__":

    params, envs, config_jsons = parse_arguments()

    print("Run Flag:", params.run_flag)

    # write versions of all dependencies
    record_versions(params.path_project)

    for config_json in config_jsons:

        if not config_json:
            continue

        if not os.path.exists(os.path.join(params.path_project, config_json)):
            raise Exception("Unable to find {}".format(config_json))

        print()
        print("{} #############################################".format(config_json))
        print()

        run(
            envs[const.ENV_MATLAB_KEY],
            params.path_project,
            config_json,
            params.run_flag,
            params.quiet
        )
