function [] = plot_reconstructed_tree(path_working, newick_filename, png_filename)

% read from newick file
reconstructed_tree = phytreeread(fullfile(path_working, newick_filename));

% plot
plot(reconstructed_tree);

% set title
title('Reconstructed');

% save to png
saveas(gcf, fullfile(path_working, png_filename), 'png');
