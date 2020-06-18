function [phytree_obj] = create_tree( ...
    rules, ...
    my_run, ...
    path_newick_without_distance, path_newick_with_distance, ...
    path_png_without_distance, path_png_with_distance ...
)

    % get the root node
    root_node = my_run.Nodes{1}(1);

    % generate tree
    T = generateTree(rules, my_run.Nodes, root_node, my_run.NameInds, my_run.Name);
    fprintf("After generateTree\n");
    phytree_obj = T.tree;

    % reroot if necessary
    %phytree_obj = reroot(T.tree, getbyname(T.tree, root_node.Name, 'Exact', true));

    % save as newtick
    phytreewrite(...
        path_newick_without_distance, ...
        phytree_obj, ...
        'Distances', 'false', ...
        'BranchNames', 'false' ...
    );

    phytreewrite(...
        path_newick_with_distance, ...
        phytree_obj, ...
        'Distances', 'true', ...
        'BranchNames', 'false' ...
    );
    fprintf("After phytreewrites\n");
    % plot_tree(path_newick_without_distance, path_png_without_distance, rules);
    % plot_tree(path_newick_with_distance, path_png_with_distance, rules);
    % fprintf("After plot_trees\n");
    function [] = plot_method_01(tree, node_names)
    % plot tree using eSTGt plotter
    % this doesn't add labels currently
    
        % make distinguishable colors
        colors = distinguishable_colors(100, 'w');

        % draw tree
        plot_generated_tree(tree, colors, node_names);
        
    end

    function [] = plot_method_02(path_newick)
    % plot tree using MATLAB built-in function
        
        tree = phytreeread(path_newick);
        plot(tree);
        
    end
        
    function [] = plot_tree(path_newick, path_png, rules)
        
        % use plot2 for now because it gives us the labels
        plot_method_02(path_newick);    

        % set plot title with seed number and simulation time
        ha = gca;
        ha.Title.String = sprintf('Simulation - Seed: %d / SimTime: %d', rules.Seed, rules.SimTime);

        % save as png file
        saveas(gcf, path_png, 'png');

    end

end
