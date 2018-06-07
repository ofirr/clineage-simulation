import sys
sys.path.append("/home/chun/clineage/")
import clineage.wsgi

import os
from frogress import bar

# transpose dictionary
from sequencing.calling.queries.mutation_maps import transpose_dict

from sequencing.phylo.triplets_wrapper import get_cells_and_root, parse_mutations_table, run_sagis_triplets, run_sagis_triplets_binary

work_path = './outputs'

# construct path for input mutation table
path_mutation_table =  os.path.join(work_path, 'mutation_table.txt')

# parse mutation table
calling = parse_mutations_table(path_mutation_table, inverse=False)
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

print(possible_roots)

print(cells)

# transpose
tcalling = transpose_dict(calling)

import dendropy

# run sagis triplets
rldr = ['Ave']
triplets_tree_path = os.path.join(work_path, 'reconstructed.newick')

run_sagis_triplets(
    textual_mutation_dict=tcalling,
    cells_to_be_used_as_root=rldr,
    newick_tree_path=triplets_tree_path,
    tripletsnumber=5000000,
    score_threshold=0,
    scoring_method='uri10',
    loci_filter='ncnr')

# fixme: would be nice if we can do this when calling `run_sagis_triplets`
os.rename("treeReconstruction.log", os.path.join(work_path, "sagis_triplets.log"))

tree_reconstructed = dendropy.Tree.get_from_path(
    triplets_tree_path,
    "newick"
)

# prune root if necessary
# root_node = tree.find_node_with_taxon_label('root')
# tree.prune_subtree(root_node);

with open(os.path.join(work_path, 'reconstructed.ascii_plot.txt'), 'wt') as fout:
    fout.write(tree_reconstructed.as_ascii_plot())
    fout.write('\n')

# re-save the newwick after eliminating quotes around taxa labels
tree_reconstructed.write_to_path(triplets_tree_path, schema='newick', unquoted_underscores=True)

# read simulation.newick
tree_simulation = dendropy.Tree.get_from_path(
    os.path.join(work_path, 'simulation.newick'),
    "newick"
)

with open(os.path.join(work_path, 'simulation.ascii_plot.txt'), 'wt') as fout:
    fout.write(tree_simulation.as_ascii_plot())
    fout.write('\n')

