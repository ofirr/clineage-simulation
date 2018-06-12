close all;

% read simulation tree from newick file
simulation_tree = phytreeread('../../analysis/tmc/case-07/simulation.newick');

% read reconstructed tree from newick file
reconstructed_tree = phytreeread('../../analysis/tmc/case-07/reconstructed.newick');

% reorder leaves in reconstructed tree to match leaf order in simulation tree
reconstructed_tree_reordered = reorder(reconstructed_tree, simulation_tree);

% plot
t2 = plot(reconstructed_tree_reordered);

% set title
title('Reconstructed (Reordered)');

t1 = plot(simulation_tree);
title('Simulation');

[idx1, dist1, names1] = get_leaf_indexes(simulation_tree);
[idx2, dist2, names2] = get_leaf_indexes(reconstructed_tree);

diff_idx = dist1 ~= dist2;

set(t1.BranchLines(diff_idx), 'LineWidth', 5');
set(t2.BranchLines(diff_idx), 'LineWidth', 5');

m = {};
m(:, 1) = names;
m(:, 2) = num2cell(dist);



function [idx, dist, names] = get_leaf_indexes(tree)

    dist = get(tree, 'Distances');
    all_names = get(tree, 'NodeNames');
    leaf_names = get(tree, 'LeafNames');

    idx = ~cellfun('isempty', regexp(all_names, "^Run") );
    dist = dist(idx);
    names = all_names(idx);
end
