close all;

path_working = '../../analysis/tmc/case-07/';

% read simulation tree from newick file
simulation_tree = phytreeread(fullfile(path_working, 'simulation.newick'));

% read reconstructed tree from newick file
reconstructed_tree = phytreeread(fullfile(path_working, 'reconstructed.newick'));

% reorder leaves in reconstructed tree to match leaf order in simulation tree
reconstructed_tree_reordered = reorder(reconstructed_tree, simulation_tree);

% plot
t2 = plot(reconstructed_tree_reordered);

% set title
title('Reconstructed (Reordered)');

t1 = plot(simulation_tree);
title('Simulation');

[edge_lengths1, names1] = get_names_edge_lengths(simulation_tree);
[edge_lengths2, names2] = get_names_edge_lengths(reconstructed_tree);

mm = {};
mm(:, 1) = cellstr(names1);
mm(:, 2) = num2cell(edge_lengths1);

for idx2 = 1:length(names2)
    new_idx = find(names1 == names2(idx2));
    mm(new_idx, 3) = { edge_lengths2(idx2) };
end

for mm_idx = 1:size(mm, 1)
    
    % skip if the edge length in simulation and reconstructed is the same
    if mm{mm_idx, 2} == mm{mm_idx, 3}
        continue
    end
    
    % given a cell name, edge length between simulaiton and reconstructed
    % is different
    
    line_width = 5;
    
    % thick edge for simulation tree
    for ii = 1:length(t1.leafNodeLabels)
        if strcmp( t1.leafNodeLabels(ii).String, mm(mm_idx, 1) )
            set(t1.BranchLines(ii), 'LineWidth', line_width);
            break
        end
    end
    
    % thick edge for reconstructed tree
    for ii = 1:length(t2.leafNodeLabels)
        if strcmp( t2.leafNodeLabels(ii).String, mm(mm_idx, 1) )
            set(t2.BranchLines(ii), 'LineWidth', line_width);
            break
        end
    end
end

function [edge_lens, names] = get_names_edge_lengths(tree)
    
    edge_lens = get(tree, 'Distances');
    all_names = get(tree, 'NodeNames');
    %leaf_names = get(tree, 'LeafNames');

    % get indexes of leaf names only (e.g. Run1_C_10)
    % this will filter out branches (e.g. Branch 4)
    idx = ~cellfun('isempty', regexp(all_names, "^Run") );
    
    % only keep edge lengths of leaves (filtering out branches)
    edge_lens = edge_lens(idx);
    
    % only keep names of leaves (filtering out branches)
    names = string(all_names(idx));
end

