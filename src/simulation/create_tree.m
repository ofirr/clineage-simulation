function create_tree(rules, my_run, path_newick, path_png)

    % get the root node
    root_node = my_run.Nodes{1}(1);

    % generate tree
    T = generateTree(rules, my_run.Nodes, root_node, my_run.NameInds, my_run.Name);

    phytree_obj = T.tree;

    % reroot if necessary
    %phytree_obj = reroot(T.tree, getbyname(T.tree, root_node.Name, 'Exact', true));

    % save as newtick
    phytreewrite(...
        path_newick, ...
        phytree_obj, ...
        'Distances', 'false', ...
        'BranchNames', 'false' ...
    );

    % use plot2 for now because it gives us the labels
    %plot1(T.tree, rules.AllNames);
    plot2(path_newick);

    % set plot title with seed number and simulation time
    ha = gca;
    ha.Title.String = sprintf('Simulation - Seed: %d / SimTime: %d', rules.Seed, rules.SimTime);

    % save as png file
    saveas(gcf, path_png, 'png');

    
    function [] = plot1(tree, node_names)
    % plot tree using eSTGt plotter
    % this doesn't add labels currently
    
        % make distinguishable colors
        colors = distinguishable_colors(100, 'w');

        % draw tree
        plot_generated_tree(tree, colors, node_names);
        
    end

    function [] = plot2(path_newick)
    % plot tree using MATLAB built-in function
        
        tree = phytreeread(path_newick)
        plot(tree);
        
    end
    
end