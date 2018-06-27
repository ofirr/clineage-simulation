import argparse
import os
import pandas as pd
import subprocess
import scipy
import dendropy


def run_command(cmd):
    "run command"

    process = subprocess.Popen(cmd)

    process.wait()


def compare(path_simulation_newick, path_reconstructed_newick, path_score_output):

    path_treecmp = '/home/chun/projects/clineage-simulation/TreeCmp/bin/treeCmp.jar'

    #  Metrics for rooted trees
    metrics = {
        "rooted": "mc rc ns tt mp mt co",
        "unrooted": "ms rf pd qt um"
    }

    cmd = [
        'java', '-jar', path_treecmp,
        '-P', '-N', '-I'
        '-r', path_simulation_newick,
        '-i', path_reconstructed_newick,
        '-o', path_score_output,
        '-d'
    ]

    cmd.extend(metrics['rooted'].split(' '))

    run_command(cmd)


def get_triples_score(path_simulation_newick, path_reconstructed_newick, path_score_output):

    compare(path_simulation_newick, path_reconstructed_newick, path_score_output)

    df_metrics = pd.read_csv(
        path_score_output,
        sep='\t',
        nrows=1
    )

    return df_metrics['Triples_toYuleAvg'][0]


def write_ascii_plot_file(path_file, plot_ascii):
    with open(path_file, 'wt') as fout:
        fout.write(plot_ascii)
        fout.write('\n')


def reconstruct_scipy_linkage(df_mutation_table, path_out_newick):

    from scipy.cluster import hierarchy

    # get newick without distance
    def getNewick(node, newick, parentdist, leaf_names):
        if node.is_leaf():
            return "%s%s" % (leaf_names[node.id], newick)
        else:
            if len(newick) > 0:
                newick = ")%s" % (newick)
            else:
                newick = ");"
            newick = getNewick(node.get_left(), newick, node.dist, leaf_names)
            newick = getNewick(node.get_right(), ",%s" %
                               (newick), node.dist, leaf_names)
            newick = "(%s" % (newick)
            return newick

    tdf = df_mutation_table.drop(columns='root').transpose()
    link = scipy.cluster.hierarchy.linkage(tdf)
    tree = hierarchy.to_tree(link, False)
    newick_str = getNewick(tree, "", tree.dist, tdf.index)

    with open(path_out_newick, 'wt') as fout:
        fout.write(newick_str)
        fout.write('\n')

    return tree


def reconstruct_neighborjoining(df_mutation_table, path_out_newick):

    from skbio import DistanceMatrix
    from skbio.tree import nj

    tdf = df_mutation_table.drop(columns='root').transpose()
    dm = DistanceMatrix(scipy.spatial.distance.squareform(
        scipy.spatial.distance.pdist(tdf)), tdf.index)

    tree = nj(dm)
    tree.write(path_out_newick, format='newick')
    return tree


def plot_ascii_dendropy(path_newick):

    # read simulation.newick
    tree = dendropy.Tree.get_from_path(path_newick, "newick")

    ascii = tree.as_ascii_plot()
    return ascii


def plot_ascii_ete(path_newick):

    from ete3 import Tree

    with open(path_newick, 'rt') as fin:
        newick = fin.read()
        tree = Tree(newick)
        ascii = tree.get_ascii()
        return ascii


def run(path_project, seed_num, n_num, case_num, path_output_base):

    if n_num == None:
        path_part_seed_n_case = 'seed-{0}/case-{1:02d}'.format(
            seed_num, case_num)
    else:
        path_part_seed_n_case = 'seed-{0}/n-{1:03d}/case-{2:02d}'.format(
            seed_num, n_num, case_num)

    # construct working path
    path_work = os.path.join(path_project, path_part_seed_n_case)

    # construct output path
    path_output_dir = os.path.join(path_output_base, path_part_seed_n_case)

    # create output directory
    os.makedirs(path_output_dir, exist_ok=True)

    FILE_RECONSTRUCTED_NEWICK_NJ = 'reconstructed.nj.newick'
    FILE_RECONSTRUCTED_NEWICK_SCIPYLINKAGE = 'reconstructed.scipylnk.newick'

    # construct other paths
    path_scipylnk_newick = os.path.join(
        path_output_dir, FILE_RECONSTRUCTED_NEWICK_SCIPYLINKAGE
    )

    path_nj_newick = os.path.join(
        path_output_dir, FILE_RECONSTRUCTED_NEWICK_NJ)

    path_simulation_newick = os.path.join(path_work, 'simulation.newick')

    path_tmc_newick = os.path.join(path_work, 'reconstructed.newick')

    path_scipylnk_score = os.path.join(path_output_dir, 'scores.scipylnk.txt')

    path_nj_score = os.path.join(path_output_dir, 'scores.nj.txt')

    path_tmc_score = os.path.join(path_output_dir, 'scores.tmc.txt')

    path_nj_ascii_plot = os.path.join(
        path_output_dir, 'reconstructed.newick.nj.ascii-plot.txt'
    )

    path_scipylnk_ascii_plot = os.path.join(
        path_output_dir, 'reconstructed.newick.scipylnk.ascii-plot.txt'
    )

    path_mutation_table = os.path.join(path_work, 'mutation_table.txt')

    # read mutation table
    df_mutation_table = pd.read_csv(
        path_mutation_table, sep='\t', index_col='names'
    )

    # reconstruct using scipy linkage
    reconstruct_scipy_linkage(df_mutation_table, path_scipylnk_newick)

    # reconstruct using neighbor joining
    tree_nj = reconstruct_neighborjoining(df_mutation_table, path_nj_newick)

    # write back reconstructed tree using neighbor joining
    # after suppressing edge lengths
    tree = dendropy.Tree.get_from_path(path_nj_newick, "newick")
    tree.write_to_path(
        path_nj_newick,
        schema='newick',
        suppress_edge_lengths=True
    )

    # get triples score for reconstructed tree using scipy linkage
    score_scipylnk = get_triples_score(
        path_simulation_newick,
        path_scipylnk_newick,
        path_scipylnk_score
    )

    # get triples score for reconstructed tree using neighbor joining
    score_nj = get_triples_score(
        path_simulation_newick,
        path_nj_newick,
        path_nj_score
    )

    # get triples score for reconstructed tree using TMC
    score_tmc = get_triples_score(
        path_simulation_newick,
        path_tmc_newick,
        path_tmc_score
    )

    # generate ascii plot and write to a file
    ascii_plot_scipylnk = plot_ascii_ete(path_scipylnk_newick)
    ascii_plot_nj = plot_ascii_ete(path_nj_newick)

    write_ascii_plot_file(path_nj_ascii_plot, ascii_plot_nj)
    write_ascii_plot_file(path_scipylnk_ascii_plot, ascii_plot_scipylnk)

    print(ascii_plot_scipylnk)
    print(ascii_plot_nj)

    # write triples scores to a file
    with open(os.path.join(path_output_dir, 'final-score.csv'), 'at') as fout:
        cols = []
        cols.append(seed_num)
        if n_num:
            cols.append(n_num)
        cols.append(case_num)
        cols.append(score_tmc)
        cols.append(score_nj)
        cols.append(score_scipylnk)
        fout.write("\t".join([str(x) for x in cols]))
        fout.write('\n')


def parse_arguments():

    parser = argparse.ArgumentParser(description='run simulation')

    parser.add_argument(
        "--project",
        action="store",
        dest="path_project",
        required=True
    )

    parser.add_argument(
        "-s",
        "--seed",
        action="store",
        dest="seed_num",
        required=True
    )

    parser.add_argument(
        "-n",
        "--n",
        action="store",
        dest="n_num",
        default="",
        required=False
    )

    parser.add_argument(
        "--case",
        action="store",
        dest="case_num",
        required=True
    )

    parser.add_argument(
        "--outdir",
        action="store",
        dest="path_output_base",
        required=True
    )

    # parse arguments
    params = parser.parse_args()

    return params


if __name__ == "__main__":

    params = parse_arguments()

    run(
        params.path_project,
        int(params.seed_num),
        int(params.n_num) if params.n_num else None,
        int(params.case_num),
        params.path_output_base
    )
