function [] = highlight_different_edge_lengths(path_simulation_tree, path_reconstructed_tree)

    % read simulation tree from newick file
    simulation_tree = phytreeread(path_simulation_tree);

    % read reconstructed tree from newick file
    reconstructed_tree = phytreeread(path_reconstructed_tree);

    % reorder leaves in reconstructed tree to match leaf order in simulation tree
    reconstructed_tree_reordered = reorder(reconstructed_tree, simulation_tree);

    % plot simulation tree
    t1 = plot(simulation_tree);
    title('Simulation');

    % plot reconstructed tree
    t2 = plot(reconstructed_tree_reordered);
    title('Reconstructed (Reordered)');

    
    % get names and edge lenghts of leaf nodes for simulation and reconstructed tree
    [edge_lengths1, names1] = get_names_edge_lengths(simulation_tree);
    [edge_lengths2, names2] = get_names_edge_lengths(reconstructed_tree_reordered);

    % edge length comparison table
    % col1: leaf name
    % col2: edge length in simulation tree
    % col3: edge length in reconstructed tree
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

        leaf_name = mm(mm_idx, 1);

        % thick edge for simulation tree
        highlight(t1, leaf_name);

        % thick edge for reconstructed tree
        highlight(t2, leaf_name);
    end

    % save to png
    saveas(t1.axes, [path_simulation_tree '.png'], 'png');
    saveas(t2.axes, [path_reconstructed_tree '.png'], 'png');
    

    function highlight(tree, leaf_name)

        line_width = 5;
        bg_color = 'yellow';

        idx = find_idx_by_leaf_name(tree, leaf_name);
        if idx ~= -1
            set(tree.BranchLines(idx), 'LineWidth', line_width);
            set(tree.terminalNodeLabels(idx), 'Background', bg_color, 'FontWeight', 'bold');
        end

    end

    function [idx] = find_idx_by_leaf_name(tree, leaf_name)

        idx = -1;

        for ii = 1:length(tree.leafNodeLabels)
            if strcmp( tree.leafNodeLabels(ii).String, leaf_name )
                idx = ii;
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

end
