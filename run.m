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

% load simulation.xml
ProgramFile = 'simulation.xml';

% run eSTGt
Rules = ParseeSTGProgram(ProgramFile);
[ Runs, RunsData ] = RunSim(Rules, Rules.Seed, Rules.SimTime);

% generate tree
Node = Runs(1).Nodes{1}(1);
T = generateTree(Rules, Runs(1).Nodes, Node, Runs(1).NameInds, Runs(1).Name);

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
