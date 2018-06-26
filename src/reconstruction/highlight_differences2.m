function [] = highlight_differences2(...
    path_simulation_tree, ...
    path_reconstructed_tree, ...
    path_sisters_count, ...
    path_diff_metrics ...
)
% calculate distance from root to each leaf and compare

    % when set to true, it will output very simple plan trees
    add_beautification = true;

    % read simulation tree from newick file
    simulation_tree = phytreeread(path_simulation_tree);

    % read reconstructed tree from newick file
    reconstructed_tree = phytreeread(path_reconstructed_tree);
    
    % reorder leaves in reconstructed tree to match leaf order in simulation tree
    reconstructed_tree_reordered = reorder(reconstructed_tree, simulation_tree);    

    % plot simulation tree
    t1 = plot(simulation_tree);
    beautify_tree(t1, 'Simulation', add_beautification);

    % plot reconstructed tree
    t2 = plot(reconstructed_tree_reordered);
    beautify_tree(t2, 'Reconstructed (Reordered)', add_beautification);
    
    if add_beautification == false
        return;
    end

    % get leaf names from simulation and reconstructed tree
    names1 = get_leaf_names(simulation_tree);
    names2 = get_leaf_names(reconstructed_tree_reordered);

    % calculate the number of hops required to go from the root to a given
    % leaf. Do this for both simulation and reconstruction tree
    [hops1, paths1] = get_hops_to_root(simulation_tree, names1);
    [hops2, paths2] = get_hops_to_root(reconstructed_tree_reordered, names2);

    counter = struct('total', length(names1), 'diff', 0, 'missing', 0);
        
    for idx = 1:length(names1)

        leaf_name = names1{idx};

        % leaf that exists in simulation doesn't exist in reconstruction
        if ~isfield(hops2, leaf_name)
            % use a different color for this absent leaf
            mark_as_absent(t1, leaf_name);
            
            % increment diff count
            counter.missing = counter.missing + 1;
            continue
        end

        % if the number of hops required to go from the root to a given
        % node differs between simulation and reconsutrction tree, let's
        % highlight the leaf node
        if hops1.(leaf_name) ~= hops2.(leaf_name)
            highlight(t1, paths1, leaf_name);
            highlight(t2, paths2, leaf_name);
            
            % increment diff count
            counter.diff = counter.diff + 1;
        end

    end
    
    fileID = fopen(path_sisters_count);
    sisters = textscan(fileID, '%s %d', 'Delimiter', ',', 'HeaderLines', 1);
    fclose(fileID);
    sisters = { sisters{1}{sisters{2} > 1} };
    for jj = 1:length(sisters)
        mark_as_not_binary(t2, sisters(jj));
    end

    % save to png
    saveas(t1.axes, [path_simulation_tree '.png'], 'png');
    saveas(t2.axes, [path_reconstructed_tree '.png'], 'png');
        
    fh = fopen(path_diff_metrics, 'wt');
    fwrite(fh, jsonencode(counter));
    fwrite(fh, newline);
    fclose(fh);

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

    function [] = highlight(tree, paths, leaf_name)

        line_width = 4;
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

    
    function [] = mark_as_not_binary(tree, leaf_name)

        color = 'red';

        % find the index of the leaf that we're interested in
        % -1 means not found
        idx = find_idx_by_leaf_name(tree, leaf_name);

        if idx ~= -1
            % make the leaf name highlighted
            set(tree.terminalNodeLabels(idx), 'Color', color, 'FontWeight', 'bold');
        end

    end


    function [] = mark_as_absent(tree, leaf_name)

        fg_color = 'white';
        bg_color = [0.5 0.5 0.5];

        % find the index of the leaf that we're interested in
        % -1 means not found
        idx = find_idx_by_leaf_name(tree, leaf_name);

        if idx ~= -1
            % make the leaf name highlighted
            set(tree.terminalNodeLabels(idx), ...
                'Background', bg_color, ...
                'Color', fg_color, ...
                'FontWeight', 'bold' ...
            );
        end

    end

    function [] = beautify_tree(tree, fig_title, add_beautification)

        if add_beautification
            marker_size = 7;
            marker_face_color = 'red';

            % change size and face color of the leaf dots
            set(tree.LeafDots, 'MarkerSize', marker_size, 'MarkerFaceColor', marker_face_color);

            % change size of the branch dots
            set(tree.BranchDots, 'MarkerSize', marker_size);
        end

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
