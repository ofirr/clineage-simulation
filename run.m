% clean up from any previous work
clear;
clc;

% path to eSTGt
addpath('C:\Users\chun\projects\eSTGt\eSTGt');

% set output path
path_output = './outputs';

% create output path if not exists already
if ~exist(path_output, 'dir')
    mkdir(path_output);
end

% load microsatellite mutation transition table
% mark it as global varaible so that it can be accessed from eSTGt
global ms_mutation_transition_prob;
load('ms_mutation_transition_prob');

% parse eSTGt rules from the program file
program_file = 'simulation.xml';
rules = ParseeSTGProgram(program_file);

% get the number of microsatellite loci
num_of_ms_loci = rules.Prod{1,1}.InternalStates.MS.DupNum;

% run simulation
[ runs, RunsData ] = RunSim(rules, rules.Seed, rules.SimTime);

% the very first run (we only have one run in fact)
my_run = runs(1);

% get the root node
root_node = my_run.Nodes{1}(1);

% create a mutation table
mutation_table = create_mutation_table(my_run, num_of_ms_loci);

% display to screen
disp(mutation_table);

% write mutation table to a file
path_mutation_table = fullfile(path_output, 'mutation_table.txt');
writetable(...
    mutation_table, ...
    path_mutation_table, ...
    'WriteVariableNames', true, ...
    'WriteRowNames', true, ...
    'Delimiter', 'tab' ...
);

% generate tree
T = generateTree(rules, my_run.Nodes, root_node, my_run.NameInds, my_run.Name);

% save newtick file
path_newick = fullfile(path_output, 'tree.newick');
phytree_obj = T.tree;
phytreewrite(path_newick, phytree_obj)

% make distinguishable colors
colors = distinguishable_colors(100, 'w');

% draw tree
plot_generated_tree(T.tree, colors, rules.AllNames);

% set plot title with seed number and simulation time
ha = gca;
ha.Title.String = sprintf('Seed: %d / SimTime: %d', rules.Seed, rules.SimTime);

% get the current figure object and save to a file
path_tree_png = fullfile(path_output, 'tree.png');
saveas(gcf, path_tree_png, 'png');
