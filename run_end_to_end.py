import os
import subprocess
import json
import argparse

ENV_MATLAB_KEY = 'matlab'
CONFIG_PATH_RELATIVE_OUTPUT = 'pathRelativeOutput'

FILE_SIMULATION_NEWICK = 'simulation.newick'
FILE_RECONSTRUCTED_NEWICK = 'reconstructed.newick'
FILE_TMC_LOG = 'tmc.log'
FILE_MUTATION_TABLE = 'mutation_table.txt'
FILE_RECONSTRUCTED_PNG = 'reconstructed.png'
FILE_COMPARISON_METRICS_RAW = 'scores.raw.out'
FILE_COMPARISON_METRICS_PRETTY = 'scores.pretty.out'

PATH_ESTGT = './eSTGt/eSTGt'
PATH_SIMULATION_LIB = './src/simulation'
PATH_RECONSTRUCT_LIB = './src/reconstruction'
PATH_TREECMP_BIN = './TreeCmp/bin/treeCmp.jar'


def read_json_config(path):

    with open(path, 'rt') as file_in:
        return json.loads(file_in.read())


def run_command(cmd):
    "run command"

    process = subprocess.Popen(cmd)

    process.wait()


def run_matlab_code(path_matlab, matlab_code):
    "run matlab script"

    cmd = [
        os.path.join(path_matlab, 'matlab'),
        '-nodisplay', '-nosplash', '-nodesktop',
        '-r', matlab_code
    ]

    run_command(cmd)


def generate_tree_ascii_plot(path_newick):

    import dendropy

    # read simulation.newick
    tree = dendropy.Tree.get_from_path(path_newick, "newick")

    # write ascii plot for simulation tree
    with open('{}.ascii-plot.txt'.format(path_newick), 'wt') as fout:
        fout.write(tree.as_ascii_plot())
        fout.write('\n')


def simulate(path_matlab, path_project, config_filename):
    "run simulation"

    # run MATLAB simulation
    matlab_code = "addpath('{0}', '{1}', '{2}'); run_simul('{2}', '{3}'); exit;".format(
        PATH_ESTGT, PATH_SIMULATION_LIB, path_project, config_filename
    )

    run_matlab_code(path_matlab, matlab_code)

    # read simulation configuration
    config = read_json_config(os.path.join(path_project, config_filename))

    path_simulation_output = os.path.join(
        path_project, config[CONFIG_PATH_RELATIVE_OUTPUT]
    )

    return path_simulation_output


def reconstruct(path_simulation_output, root_cell_notation='root'):

    import sys
    sys.path.append("/home/chun/clineage/")
    import clineage.wsgi

    import os
    from frogress import bar

    # transpose dictionary
    from sequencing.calling.queries.mutation_maps import transpose_dict

    from sequencing.phylo.triplets_wrapper import get_cells_and_root, parse_mutations_table, run_sagis_triplets, run_sagis_triplets_binary

    # construct path for input mutation table
    path_mutation_table = os.path.join(
        path_simulation_output, FILE_MUTATION_TABLE
    )

    # parse mutation table
    calling = parse_mutations_table(path_mutation_table, inverse=False)

    # verify the presence of a root cell in the input data.
    possible_roots = [cell for cell in calling if root_cell_notation in cell]
    assert len(possible_roots) == 1
    root_label = possible_roots[0]
    root = (root_label, calling[root_label])
    cells = []
    for cell in calling:
        if cell == root_label:
            continue
        cells.append((cell, calling[cell]))
    assert len(cells) > 2

    print(possible_roots)

    print(cells)

    # transpose
    tcalling = transpose_dict(calling)

    import dendropy

    # run sagis triplets
    rldr = [root_cell_notation]  # cf. 'Ave'
    triplets_tree_path = os.path.join(
        path_simulation_output, FILE_RECONSTRUCTED_NEWICK
    )

    run_sagis_triplets(
        textual_mutation_dict=tcalling,
        cells_to_be_used_as_root=rldr,
        newick_tree_path=triplets_tree_path,
        tripletsnumber=5000000,
        score_threshold=0,
        scoring_method='uri10',
        loci_filter='ncnr')

    # fixme: would be nice if we can do this when calling `run_sagis_triplets`
    os.rename(
        "treeReconstruction.log",
        os.path.join(path_simulation_output, FILE_TMC_LOG)
    )

    # load reconstructed tree
    tree_reconstructed = dendropy.Tree.get_from_path(
        triplets_tree_path,
        "newick"
    )

    # prune root
    root_node = tree_reconstructed.find_node_with_taxon_label(
        root_cell_notation
    )
    if root_node:
        tree_reconstructed.prune_subtree(root_node)

    # re-save the newwick after eliminating quotes around taxa labels
    tree_reconstructed.write_to_path(
        triplets_tree_path, schema='newick', unquoted_underscores=True)


def plot_recontructed_tree(path_matlab, path_newick, path_png):

    # run MATLAB simulation
    matlab_code = "addpath('{0}', '{1}'); plot_reconstructed_tree('{2}', '{3}'); exit;".format(
        PATH_ESTGT, PATH_RECONSTRUCT_LIB, path_newick, path_png
    )

    run_matlab_code(path_matlab, matlab_code)


def compare(path_simulation_newick, path_reconstructed_newick, path_score_output):

    #  Metrics for rooted trees
    metrics = {
        "rooted": "mc rc ns tt mp mt co",
        "unrooted": "ms rf pd qt um"
    }

    cmd = [
        'java', '-jar', PATH_TREECMP_BIN,
        '-P', '-N', '-I'
        '-r', path_simulation_newick,
        '-i', path_reconstructed_newick,
        '-o', path_score_output,
        '-d'
    ]

    cmd.extend(metrics['rooted'].split(' '))

    run_command(cmd)


def report(path_scores_output_raw, path_scores_output_pretty):

    from io import StringIO
    import pandas as pd
    import os

    # read the first two lines that contain various metrics
    df_metrics = pd.read_csv(path_scores_output_raw, sep='\t', nrows=1)

    # transpose and rename the column to 'metrics'
    df_metrics = df_metrics.T.rename(columns={0: 'metrics'})

    # display to the screen
    print(df_metrics)
    print()

    # read the summary section
    df_summary = pd.read_csv(path_scores_output_raw, sep='\t', skiprows=4)

    print(df_summary)

    with open(path_scores_output_pretty, 'wt') as fout:
        fout.write(df_metrics.to_string())
        fout.write(df_summary.to_string())


def run(path_matlab, path_project, config_json):
    "run function"

    # run simulation
    path_simulation_output = simulate(
        path_matlab, path_project, config_json
    )

    # take simulation tree and make ascii plot
    generate_tree_ascii_plot(
        os.path.join(path_simulation_output, FILE_SIMULATION_NEWICK)
    )

    # reconstruct based on mutation table generated from simulation
    reconstruct(path_simulation_output)

    # take reconstructed tree and make ascii plot
    generate_tree_ascii_plot(
        os.path.join(path_simulation_output, FILE_RECONSTRUCTED_NEWICK)
    )

    # plot the reconstructed tree
    plot_recontructed_tree(
        envs[ENV_MATLAB_KEY],
        os.path.join(path_simulation_output, FILE_RECONSTRUCTED_NEWICK),
        os.path.join(path_simulation_output, FILE_RECONSTRUCTED_PNG)
    )

    # compare simulation tree and reconstructed tree
    compare(
        os.path.join(path_simulation_output, FILE_SIMULATION_NEWICK),
        os.path.join(path_simulation_output, FILE_RECONSTRUCTED_NEWICK),
        os.path.join(path_simulation_output, FILE_COMPARISON_METRICS_RAW)
    )

    # report the final comparison metrics in a pretty format
    report(
        os.path.join(path_simulation_output, FILE_COMPARISON_METRICS_RAW),
        os.path.join(path_simulation_output, FILE_COMPARISON_METRICS_PRETTY),
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
        "--multi",
        action="store_true",
        dest="multi"
    )

    # parse arguments
    params = parser.parse_args()

    # read environment configuration
    envs = read_json_config(params.path_env)

    if params.multi:
        with open(os.path.join(params.path_project, 'config.list'), 'rt') as fin:
            config_jsons = fin.read().splitlines()
    else:
        config_jsons = ['config.json']

    return params, envs, config_jsons


if __name__ == "__main__":

    params, envs, config_jsons = parse_arguments()

    for config_json in config_jsons:

        if not os.path.exists(os.path.join(params.path_project, config_json)):
            raise Exception("Unable to find {}".format(config_json))

        print()
        print("{} #############################################".format(config_json))
        print()

        run(envs[ENV_MATLAB_KEY], params.path_project, config_json)
