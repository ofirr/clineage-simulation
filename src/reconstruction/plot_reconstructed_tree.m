function [] = plot_reconstructed_tree(path_simulation_newick, path_reconstructed_newick, path_png)

% read simulation tree from newick file
simulation_tree = phytreeread(path_simulation_newick);

% read reconstructed tree from newick file
reconstructed_tree = phytreeread(path_reconstructed_newick);

% reorder leaves in reconstructed tree to match leaf order in simulation tree
reconstructed_tree_reordered = reorder(reconstructed_tree, simulation_tree);

% plot
plot(reconstructed_tree_reordered);

% set title
title('Reconstructed (Reordered)');

% save to png
saveas(gcf, path_png, 'png');
