
reconstructed_tree = phytreeread('../outputs/reconstructed.newick');

colors = distinguishable_colors(100, 'w');

% fixme: {'C'}
plot_generated_tree(reconstructed_tree, colors, {'C'});

% save as png file
saveas(gcf, '../outputs/reconstructed.png', 'png');

% find a node with the label 'root'
% this returns a vector
indexes = getbyname(reconstructed_tree, 'root');
root_pruned_tree = prune(reconstructed_tree, indexes);
plot(root_pruned_tree);
title('Reconstructed');