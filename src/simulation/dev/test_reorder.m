close all;

% read simulation tree from newick file
simulation_tree = phytreeread('../../../analysis/tmc/case-07/simulation.newick');

% read reconstructed tree from newick file
reconstructed_tree = phytreeread('../../../analysis/tmc/case-07/reconstructed.newick');

% reorder leaves in reconstructed tree to match leaf order in simulation tree
reconstructed_tree_reordered = reorder(reconstructed_tree, simulation_tree);

% plot
plot(reconstructed_tree_reordered);

% set title
title('Reconstructed (Reordered)');
