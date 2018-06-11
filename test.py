import os
import subprocess
import json
import argparse

ENV_MATLAB_KEY='matlab'

FILE_SIMULATION_NEWICK='simulation.newick'
FILE_RECONSTRUCTED_NEWICK='reconstructed.newick'
FILE_TMC_LOG='tmc.log'
FILE_MUTATION_TABLE='mutation_table.txt'
FILE_RECONSTRUCTED_PNG='reconstructed.png'
FILE_COMPARISON_METRICS='scores.out'
CONFIG_PATH_RELATIVE_OUTPUT='pathRelativeOutput'


PATH_ESTGT='./eSTGt/eSTGt'
PATH_SIMULATION_LIB='./src/simulation'
PATH_RECONSTRUCT_LIB='./src/reconstruction'
PATH_TREECMP_BIN='./TreeCmp/bin/treeCmp.jar'

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


def generate_tree_ascii_plot(path_output, newick_filename):

    import dendropy

    # read simulation.newick
    tree = dendropy.Tree.get_from_path(
        os.path.join(path_output, newick_filename),
        "newick"
    )

    # write ascii plot for simulation tree
    with open(os.path.join(path_output, '{}.ascii-plot.txt'.format(newick_filename)), 'wt') as fout:
        fout.write(tree.as_ascii_plot())
        fout.write('\n')


def simulate(path_matlab):
    "run simulation"

    path_working='./examples/example-01'
    path_working='./analysis/tmc'

    config_filename = 'config-01.json'

    # run MATLAB simulation
    matlab_code = "addpath('{0}', '{1}', '{2}'); run_simul('{2}', '{3}'); exit;".format(
        PATH_ESTGT, PATH_SIMULATION_LIB, path_working, config_filename
    )

    run_matlab_code(path_matlab, matlab_code)

    # read simulation configuration
    config = read_json_config(os.path.join(path_working, config_filename))

    path_simulation_output = os.path.join(path_working, config[CONFIG_PATH_RELATIVE_OUTPUT])

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
    path_mutation_table =  os.path.join(path_simulation_output, FILE_MUTATION_TABLE)

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
    rldr = [root_cell_notation] # cf. 'Ave'
    triplets_tree_path = os.path.join(path_simulation_output, FILE_RECONSTRUCTED_NEWICK)

    run_sagis_triplets(
        textual_mutation_dict=tcalling,
        cells_to_be_used_as_root=rldr,
        newick_tree_path=triplets_tree_path,
        tripletsnumber=5000000,
        score_threshold=0,
        scoring_method='uri10',
        loci_filter='ncnr')

    # fixme: would be nice if we can do this when calling `run_sagis_triplets`
    os.rename("treeReconstruction.log", os.path.join(path_simulation_output, FILE_TMC_LOG))

    # load reconstructed tree
    tree_reconstructed = dendropy.Tree.get_from_path(
        triplets_tree_path,
        "newick"
    )

    # prune root
    root_node = tree_reconstructed.find_node_with_taxon_label(root_cell_notation)
    tree_reconstructed.prune_subtree(root_node);

    # re-save the newwick after eliminating quotes around taxa labels
    tree_reconstructed.write_to_path(triplets_tree_path, schema='newick', unquoted_underscores=True)


def plot_recontructed_tree(path_matlab, path_simulation_output, newick_filename, png_filename):

    # run MATLAB simulation
    matlab_code = "addpath('{0}', '{1}'); plot_reconstructed_tree('{2}', '{3}', '{4}'); exit;".format(
        PATH_ESTGT, PATH_RECONSTRUCT_LIB, path_simulation_output, newick_filename, png_filename
    )

    run_matlab_code(path_matlab, matlab_code)


def compare(path_simulation_newick, path_reconstructed_newick, path_score_output):

    #  Metrics for rooted trees
    metrics_r="mc rc ns tt mp mt co"

    # metrics for unrooted trees
    metrics_ur="ms rf pd qt um"

    cmd = [
        'java', '-jar', PATH_TREECMP_BIN,
        '-r', path_simulation_newick,
        '-d', metrics_r.split(' '),
        '-i', path_reconstructed_newick,
        '-o', path_score_output,
        '-P', '-N', '-I'
    ]

    run_command(cmd)


def main():
    "main function"

    parser = argparse.ArgumentParser(description='run simulation')

    parser.add_argument(
        "--env",
        action="store",
        dest="path_config_env",
        required=True
    )

    params = parser.parse_args()

    # read environment configuration
    envs = read_json_config(params.path_config_env)

    # run simulation
    path_simulation_output = simulate(envs[ENV_MATLAB_KEY])

    # take simulation tree and make ascii plot
    generate_tree_ascii_plot(path_simulation_output, FILE_SIMULATION_NEWICK)

    # reconstruct based on mutation table generated from simulation
    reconstruct(path_simulation_output)

    # take reconstructed tree and make ascii plot
    generate_tree_ascii_plot(path_simulation_output, FILE_RECONSTRUCTED_NEWICK)

    #
    plot_recontructed_tree(
        envs[ENV_MATLAB_KEY],
        path_simulation_output,
        FILE_RECONSTRUCTED_NEWICK,
        FILE_RECONSTRUCTED_PNG
    )

    compare(
        os.path.join(path_simulation_output, FILE_SIMULATION_NEWICK),
        os.path.join(path_simulation_output, FILE_RECONSTRUCTED_NEWICK),
        os.path.join(path_simulation_output, FILE_COMPARISON_METRICS)
    )


if __name__ == "__main__":

    main()
