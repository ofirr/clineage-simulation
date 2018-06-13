function [] = highlight_differences2(path_simulation_tree, path_reconstructed_tree)
% calculate distance from root to each leaf and compare

    % read simulation tree from newick file
    simulation_tree = phytreeread(path_simulation_tree);

    % read reconstructed tree from newick file
    reconstructed_tree = phytreeread(path_reconstructed_tree);

    % reorder leaves in reconstructed tree to match leaf order in simulation tree
    reconstructed_tree_reordered = reorder(reconstructed_tree, simulation_tree);

    % plot simulation tree
    t1 = plot(simulation_tree);
    beautify_tree(t1, 'Simulation');

    % plot reconstructed tree
    t2 = plot(reconstructed_tree_reordered);
    beautify_tree(t2, 'Reconstructed (Reordered)');

    % get leaf names from simulation and reconstructed tree
    names1 = get_leaf_names(simulation_tree);
    names2 = get_leaf_names(reconstructed_tree_reordered);

    % calculate the number of hops required to go from the root to a given
    % leaf. Do this for both simulation and reconstruction tree
    [hops1, paths1] = get_hops_to_root(simulation_tree, names1);
    [hops2, paths2] = get_hops_to_root(reconstructed_tree_reordered, names2);

    for idx = 1:length(names1)

        leaf_name = names1{idx};

        % leaf that exists in simulation doesn't exist in reconstruction
        if ~isfield(hops2, leaf_name)
            %fixme: do something
            continue
        end

        % if the number of hops required to go from the root to a given
        % node differs between simulation and reconsutrction tree, let's
        % highlight the leaf node
        if hops1.(leaf_name) ~= hops2.(leaf_name)
            highlight(t1, paths1, leaf_name);
            highlight(t2, paths2, leaf_name);
        end

    end

    % save to png
    saveas(t1.axes, [path_simulation_tree '.png'], 'png');
    saveas(t2.axes, [path_reconstructed_tree '.png'], 'png');


    function [hops, paths] = get_hops_to_root(tree, leaf_names)

        % https://www.mathworks.com/help/bioinfo/ref/graphpred2path.html

        % the idea is to convert the tree to a graph and find the path from
        % the root to the leaf we're interested in
        [CM, labels, dist] = getmatrix(tree);
        root_loc = size(CM, 1);

        hops = struct();
        paths = struct();

        for idx1 = 1:length(leaf_names)

            leaf_name = leaf_names{idx1};

            x_loc_idx = find( strcmp(leaf_name, labels) );
            [T, PRED] = graphminspantree(CM, root_loc);

            path_to_leaf = graphpred2path(PRED, x_loc_idx);
            % starting from 2 because the first one doesn't count
            paths.(leaf_name) = path_to_leaf(2:end);

            % -1 because the first one in the path doesn't count
            hops.(leaf_name) = length(path_to_leaf) - 1;

        end

    end

    function highlight(tree, paths, leaf_name)

        line_width = 5;
        bg_color = 'yellow';

        % find the index of the leaf that we're interested in
        % -1 means not found
        idx = find_idx_by_leaf_name(tree, leaf_name);

        if idx ~= -1
            % make the branch line thicker
            set(tree.BranchLines(paths.(leaf_name)), 'LineWidth', line_width);

            % make the leaf name highlighted
            set(tree.terminalNodeLabels(idx), 'Background', bg_color, 'FontWeight', 'bold');
        end

    end

    function [] = beautify_tree(tree, fig_title)

        marker_size = 10;
        marker_face_color = 'red';

        % change size and face color of the leaf dots
        set(tree.LeafDots, 'MarkerSize', marker_size, 'MarkerFaceColor', marker_face_color);

        % change size of the branch dots
        set(tree.BranchDots, 'MarkerSize', marker_size);

        % change figure title
        title(fig_title);

    end

    function [idx] = find_idx_by_leaf_name(tree, leaf_name)

        idx = -1;

        % iterate through and find the index of the leaf
        for ii = 1:length(tree.leafNodeLabels)
            if strcmp( tree.leafNodeLabels(ii).String, leaf_name )
                idx = ii;
                break
            end
        end

    end

    function [names] = get_leaf_names(tree)

        % get all names (branches + leaves)
        all_names = get(tree, 'NodeNames');

        % get indexes of leaf names only (e.g. Run1_C_10)
        % this will filter out branches (e.g. Branch 4)
        idx = ~cellfun('isempty', regexp(all_names, "^Run") );

        % only keep names of leaves (filtering out branches)
        names = all_names(idx);
    end

end
