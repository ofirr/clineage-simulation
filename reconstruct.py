import os
import pandas as pd
import numpy as np
import re
from sklearn import preprocessing
from shutil import copyfile
import tempfile

from src import const
import sys
sys.path.append("/home/{}/clineage/".format(os.environ['USER']))
import clineage.wsgi

# --> extracted from production
import csv
import networkx as nx
import functools

sys.path.append(
    '/home/{}/s/Ofir/triplets/triplets/'.format(os.environ['USER'])
)
from TMC_CLI import parse_mutations_table, paired_triplets_generator, format_triplet
from triplets_input_generators.splittable_bi import solved_splittable_bi_generator
from triplets_input_generators.full_biallelic import solved_biallelic_generator
from triplets_input_generators.mono import solved_mono_generator
from triplets_input_generators.best_shot import splitable_then_full


class NoSuchTripletsGenerator(Exception):
    pass


def get_triplets_generator(triplets_generator_name):
    if triplets_generator_name == 'mono':
        return solved_mono_generator
    if triplets_generator_name == 'splitable':
        return solved_splittable_bi_generator
    if triplets_generator_name == 'full_bi':
        return solved_biallelic_generator
    if triplets_generator_name == 'splitable_then_full':
        return splitable_then_full
    if triplets_generator_name == 'full_then_splittable':
        return functools.partial(splitable_then_full, reversed=True)
    raise NoSuchTripletsGenerator(triplets_generator_name)


def transpose_dict(d):
    td = dict()
    for k1 in d:
        for k2 in d[k1]:
            td.setdefault(k2, dict())[k1] = d[k1][k2]
    return td


def add_root_to_dict(
        textual_mutation_dict,
        cells_to_be_used_as_root,
):
    new_d = dict()
    if cells_to_be_used_as_root == ['Ave']:
        cells_to_be_used_as_root = set(
            c for loc in textual_mutation_dict for c in textual_mutation_dict[loc]
        )
    else:
        cells_to_be_used_as_root = set(cells_to_be_used_as_root)
    root_collection = dict()
    for loc in textual_mutation_dict:
        for c in textual_mutation_dict[loc].keys() & cells_to_be_used_as_root:
            root_collection.setdefault(loc, []).append(
                textual_mutation_dict[loc][c]
            )
    for loc in root_collection:
        val = int(np.median(root_collection[loc]))
        new_d.setdefault(loc, dict())['root'] = val
        new_d[loc].update(textual_mutation_dict[loc])
    return new_d


def get_cells_and_root(mutation_table_path_for_triplets):
    calling = parse_mutations_table(
        mutation_table_path_for_triplets, inverse=True
    )
    # Verify the presence of a root cell in the input data.
    possible_roots = [cell for cell in calling if 'root' in cell]
    assert len(possible_roots) == 1
    root_label = possible_roots[0]
    root = (root_label, calling[root_label])
    cells = []
    for cell in calling:
        if cell == root_label:
            continue
        cells.append((cell, calling[cell]))
    assert len(cells) > 2
    return root, cells


def print_mutation_dict_to_file(textual_mutation_dict, output_path):
    loci_columns = {
        msl for sr in textual_mutation_dict for msl in textual_mutation_dict[sr]}
    with open(output_path, 'w') as f:
        fieldnames = ['names'] + list(loci_columns)
        writer = csv.DictWriter(f, fieldnames=fieldnames, dialect='excel-tab')
        writer.writeheader()
        for sr in textual_mutation_dict:
            row_dict = {'names': sr}
            row_dict.update(textual_mutation_dict[sr])
            row_dict.update(
                {loc: 'NaN' for loc in loci_columns -
                    textual_mutation_dict[sr].keys()}
            )
            writer.writerow(row_dict)


def map_cell_ids_for_sagi(rtd):
    rtd_for_sagi = dict()
    cell_id_map_for_sagi = dict()
    for i, cell_id in enumerate(rtd.keys()):
        cell_id_map_for_sagi[cell_id] = i
        if 'root' in cell_id:
            rtd_for_sagi[cell_id] = rtd[cell_id]
            continue
        rtd_for_sagi[i] = rtd[cell_id]
    return rtd_for_sagi, cell_id_map_for_sagi


def simplified_triplets_calculation(
        textual_mutation_dict,
        triplets_file,
        triplets_generator_name,
        score_threshold=0,  # print scores
        choosing_method='mms',
        scoring_method='uri10',
        printscores=True,
        loci_filter='ncnr',
        sabc=0,
        tripletsnumber=5000000
):
    triplets_generator = get_triplets_generator(triplets_generator_name)
    rtd = transpose_dict(textual_mutation_dict)
    rtd_for_sagi, cell_id_map_for_sagi = map_cell_ids_for_sagi(rtd)
    d = transpose_dict(rtd_for_sagi)

    print("Generating triplets...")

    with open(triplets_file, 'w') as f:
        for triplet, pair, score in triplets_generator(
                d,
                n=tripletsnumber,
                loci_filter=loci_filter,
                scoring_method=scoring_method,
                choosing_method=choosing_method,
                threshold=score_threshold):
            f.write(
                format_triplet(
                    triplet,
                    pair,
                    score,
                    print_scores=printscores,
                    with_data=False
                )
            )

    return cell_id_map_for_sagi


# deprecated
# def calculate_triplets_tree(
#         textual_mutation_dict,
#         triplets_file,
#         cells_to_be_used_as_root=['Ave'],
#         score_threshold=0,  # print scores
#         choosing_method='mms',
#         scoring_method='uri10',
#         printscores=True,
#         loci_filter='ncnr',
#         sabc=0,
#         tripletsnumber=5000
# ):
#     rtd = transpose_dict(textual_mutation_dict)

#     if 'root' not in rtd:
#         rtd = add_root_to_dict(
#             textual_mutation_dict=textual_mutation_dict,
#             cells_to_be_used_as_root=cells_to_be_used_as_root)
#         rtd = transpose_dict(rtd)

#     rtd_for_sagi, cell_id_map_for_sagi = map_cell_ids_for_sagi(rtd)

#     with tempfile.NamedTemporaryFile() as temp_file:
#         print_mutation_dict_to_file(rtd_for_sagi, temp_file.name)
#         root, cells = get_cells_and_root(temp_file.name)

#     G = nx.Graph()
#     G.add_nodes_from(cells)

#     print("Generating triplets...")
#     with open(triplets_file, 'w') as f:
#         for triplet, pair, score in paired_triplets_generator(root,
#                                                               G,
#                                                               loci_filter=loci_filter,
#                                                               scoring_method=scoring_method,
#                                                               choosing_method=choosing_method,
#                                                               threshold=score_threshold,
#                                                               triplets_num=tripletsnumber,
#                                                               sabc=sabc):
#             f.write(format_triplet(triplet, pair,
#                                    score, print_scores=printscores, with_data=True))

#     return cell_id_map_for_sagi
# <--


def triplets_to_df(path_raw):

    tmp = []

    with open(path_raw, 'rt') as fin:
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

                    tmp.append(
                        [sa, sb, sc, dist]
                    )
            except:
                raise Exception(triplet)

    return pd.DataFrame(
        tmp, columns=['sai', 'sbi', 'sci', 'dist']
    )


def df_to_triplets(df, path_out):

    def convert_to_triplet(item):
        return '{},{}|{}:{}'.format(int(item.sai), int(item.sbi), int(item.sci), item.dist)

    ss_triplets = df.apply(convert_to_triplet, axis=1)

    with open(path_out, 'wt') as stream:
        for row in ss_triplets:
            stream.write(row + ' ')

        stream.write('\n')


def normalize_triplet_dist(path_triplets_list_raw):

    copyfile(path_triplets_list_raw, path_triplets_list_raw + '.bak')

    df = triplets_to_df(path_triplets_list_raw)

    # create an object to transform the data to fit minmax processor
    # reshape(-1, 1) -> one column, x rows
    min_max_scaler = preprocessing.MinMaxScaler()

    dist_normalized = min_max_scaler.fit_transform(
        df.dist.values.reshape(-1, 1))
    df.dist = np.round(dist_normalized, 4)

    df_to_triplets(df, path_triplets_list_raw)
