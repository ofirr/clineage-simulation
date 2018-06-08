
reconstructed_tree = phytreeread('../outputs/reconstructed.newick');

colors = distinguishable_colors(100, 'w');

% fixme: {'C'}
plot_generated_tree(reconstructed_tree, colors, {'C'});

% save as png file
saveas(gcf, '../outputs/reconstructed.png', 'png');
