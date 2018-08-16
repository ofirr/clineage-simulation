import os
import json
import argparse
import re
import pandas as pd

from src import const
from src import utils


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
        const.PATH_ESTGT, const.PATH_SIMULATION_LIB, path_project, config_filename
    )

    utils.run_matlab_code(path_matlab, matlab_code)


def reconstruct(path_simulation_output, root_cell_notation, scoring_method, choosing_method, quiet=True):

    import sys
    sys.path.append("/home/chun/clineage/")
    import clineage.wsgi

    from sequencing.phylo.triplets_wrapper import parse_mutations_table, calculate_triplets_tree, run_sagis_triplets_binary, convert_names_in_sagis_newick

    # construct path for input mutation table
    path_mutation_table = os.path.join(
        path_simulation_output, const.FILE_MUTATION_TABLE
    )

    # parse mutation table
    calling = parse_mutations_table(path_mutation_table, inverse=True)

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
    path_triplets_list_csv = os.path.join(
        path_simulation_output, const.FILE_TRIPLETS_LIST_CSV
    )

    # create triplets list using given parameters
    rldr = [root_cell_notation]  # cf. 'Ave'
    cell_id_map_for_sagi = calculate_triplets_tree(
        textual_mutation_dict=calling,
        triplets_file=path_triplets_list_raw,
        cells_to_be_used_as_root=rldr,
        score_threshold=0,
        choosing_method=choosing_method,
        scoring_method=scoring_method,
        printscores=True,
        loci_filter="ncnr",
        sabc=0,
        tripletsnumber=5000000  # basically, max num of triplets
    )

    # run sagis triplets binary
    # the output newick will have the numeric ids which correspond to the actual cell names
    ret_code = run_sagis_triplets_binary(
        path_triplets_list_raw,
        path_reconstructed_tmp_newick
    )

    # convert the numeric ids in newick to the actual cell names
    convert_names_in_sagis_newick(
        path_reconstructed_tmp_newick,
        path_reconstructed_newick,
        cell_id_map_for_sagi
    )

    # fixme: would be nice if we can do this when calling `run_sagis_triplets_binary`
    # fixme: problematic when running multiple simultaneously using SGE
    # os.rename(
    #     "treeReconstruction.log",
    #     os.path.join(path_simulation_output, const.FILE_TMC_LOG)
    # )

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

    # construct easy triplet lookup table
    df_mapping = pd.DataFrame.from_dict(cell_id_map_for_sagi, orient='index')
    df_mapping = df_mapping.reset_index() \
        .set_index(0) \
        .rename(columns={'index': 'cellname'})
    df_mapping.index.name = 'index'

    # iterate through triplets list
    # parse so that we can construct a nice pandas dataframe out of it
    tmp = []
    with open(path_triplets_list_raw, 'rt') as fin:
        data = fin.read()
        # e.g.
        # 8,0|3:0.5774 18,8|11:1.4142 15,0|9:0.3416 6,0|3:1.2041
        triplets = data.split(' ')
        for triplet in triplets:
            try:
                # e.g.
                # 1,12|11:0.8165
                match = re.search(r'(\d+),(\d+)\|(\d+):(.*)', triplet)
                if match:
                    sa, sb, sc, dist = match.groups()
                    sa = int(sa)
                    sb = int(sb)
                    sc = int(sc)
                    dist = float(dist)

                    # lookup the actuall cell that corresponds to the id
                    # from the mapping dataframe
                    cellnames = list(df_mapping.loc[[sa, sb, sc]].cellname)

                    tmp.append(
                        [sa, sb, sc] + cellnames + [dist]
                    )
            except:
                raise Exception(triplet)

    # create a dataframe and save to csv
    df_triplets = pd.DataFrame(
        tmp, columns=['sai', 'sbi', 'sci', 'sa', 'sb', 'sc', 'dist']
    )
    df_triplets.to_csv(path_triplets_list_csv, index=False)

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
        const.PATH_ESTGT, const.PATH_RECONSTRUCT_LIB, path_simulation_newick, path_reconstructed_newick, path_png
    )

    utils.run_matlab_code(path_matlab, matlab_code)


def highlight_tree_differences_to_png(path_matlab, path_simulation_newick, path_reconstructed_newick, path_sisters_csv, path_diff_metrics):

    matlab_code = "addpath('{0}', '{1}'); highlight_differences2('{2}', '{3}', '{4}', '{5}'); exit;".format(
        const.PATH_ESTGT, const.PATH_RECONSTRUCT_LIB,
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


def run(path_matlab, path_project, config_filename, generate_tree_only, quiet):
    "run function"

    # run stochastic lineage tree simulation
    simulate_lineage_tree(
        path_matlab, path_project, config_filename
    )

    # read simulation configuration
    config = utils.read_json_config(
        os.path.join(path_project, config_filename))

    path_simulation_output = os.path.join(
        path_project, config[const.CONFIG_PATH_RELATIVE_OUTPUT]
    )

    # take simulation tree and make ascii plot
    generate_tree_ascii_plot(
        os.path.join(path_simulation_output, const.FILE_SIMULATION_NEWICK)
    )

    # user wants to generate tree only
    if generate_tree_only:
        return

    # reconstruct based on mutation table generated from simulation
    reconstruct(
        path_simulation_output,
        'root',
        config.get(const.CONFIG_RECONSTRUCT_SCORING_METHOD, 'uri10'),
        config.get(const.CONFIG_RECONSTRUCT_CHOOSING_METHOD, 'mms'),
        quiet
    )

    # take reconstructed tree and make ascii plot
    generate_tree_ascii_plot(
        os.path.join(path_simulation_output, const.FILE_RECONSTRUCTED_NEWICK)
    )

    # highlight tree differences and save to png
    highlight_tree_differences_to_png(
        envs[const.ENV_MATLAB_KEY],
        os.path.join(path_simulation_output, const.FILE_SIMULATION_NEWICK),
        os.path.join(path_simulation_output, const.FILE_RECONSTRUCTED_NEWICK),
        os.path.join(path_simulation_output, const.FILE_SISTERS_COUNT),
        os.path.join(path_simulation_output, const.FILE_DIFF_METRICS)
    )

    # compare simulation tree and reconstructed tree
    compare(
        os.path.join(path_simulation_output, const.FILE_SIMULATION_NEWICK),
        os.path.join(path_simulation_output, const.FILE_RECONSTRUCTED_NEWICK),
        os.path.join(path_simulation_output, const.FILE_COMPARISON_METRICS_RAW)
    )

    # report the final comparison metrics in a pretty format
    report(
        os.path.join(path_simulation_output,
                     const.FILE_COMPARISON_METRICS_RAW),
        os.path.join(path_simulation_output,
                     const.FILE_COMPARISON_METRICS_PRETTY),
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
        "--generate-tree-only",
        action="store_true",
        default=False,
        dest="generate_tree_only"
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
            params.generate_tree_only,
            params.quiet
        )
