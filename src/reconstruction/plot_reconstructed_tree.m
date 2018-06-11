function [] = plot_reconstructed_tree(path_newick, path_png)

% read from newick file
reconstructed_tree = phytreeread(path_newick);

% plot
plot(reconstructed_tree);

% set title
title('Reconstructed');

% save to png
saveas(gcf, path_png, 'png');
