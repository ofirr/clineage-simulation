% clean up from any previous work
clear;
clc;

% constants
% this must be the same as one declared in `simulation.xml`
NUM_OF_MS_LOCI = 10;

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

% load simulation.xml
ProgramFile = 'simulation.xml';

% run eSTGt
Rules = ParseeSTGProgram(ProgramFile);
[ Runs, RunsData ] = RunSim(Rules, Rules.Seed, Rules.SimTime);

% get the indexes of the leaves by extracting the last row of the LiveNodes
leaves_idx = Runs.LiveNodes{end};

% create a mutation table
% row: cell ID
% column: ms ID
% cell: ms repeat length
mutation_table = NaN( length(leaves_idx), NUM_OF_MS_LOCI );

for col = 1:NUM_OF_MS_LOCI
        
    for row = 1:length(leaves_idx)
        
        leaf_id = leaves_idx(row);
        mutation_table(row, col) = Runs.Nodes{1,1}(leaf_id).InternalStates.MS(col);
       
    end
    
end

% create a row/column header for mutation table
column_header = 'LOC_' + string(1:NUM_OF_MS_LOCI);
column_header = cellstr(column_header);
row_header = { Runs.Nodes{1}(leaves_idx).Name };

% create a mutation table with column header, row header
mutation_table_full = array2table(...
    mutation_table, ...
    'VariableNames', column_header, ...
    'RowNames', row_header ...
);

% set dimension name for mutation table
% this will allow to do `mutation_table_full.Cells`
% this will set (0,0) to `Cells` when outputted to a file
mutation_table_full.Properties.DimensionNames{1} = 'Cells';

% display to screen
disp(mutation_table_full);

% write mutation table to a file
path_mutation_table = fullfile(path_output, 'mutation_table.txt');
writetable(...
    mutation_table_full, ...
    path_mutation_table, ...
    'WriteVariableNames', true, ...
    'WriteRowNames', true, ...
    'Delimiter', 'tab' ...
);

% generate tree
root_node = Runs(1).Nodes{1}(1);
T = generateTree(Rules, Runs(1).Nodes, root_node, Runs(1).NameInds, Runs(1).Name);

% save newtick file
path_newick = fullfile(path_output, 'tree.newick');
phytree_obj = T.tree;
phytreewrite(path_newick, phytree_obj)

% make distinguishable colors
colors = distinguishable_colors(100, 'w');

% draw tree
plot_generated_tree(T.tree, colors, Rules.AllNames);

% set plot title with seed number and simulation time
ha = gca;
ha.Title.String = sprintf('Seed: %d / SimTime: %d', Rules.Seed, Rules.SimTime);

% get the current figure object and save to a file
path_tree_png = fullfile(path_output, 'tree.png');
saveas(gcf, path_tree_png, 'png');
