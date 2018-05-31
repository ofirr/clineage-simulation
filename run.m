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

% construct path for mutation table, newick, and png
path_mutation_table = fullfile(path_output, 'mutation_table.txt');
path_newick = fullfile(path_output, 'tree.newick');
path_tree_png = fullfile(path_output, 'tree.png');

% load microsatellite mutation transition table
% global varaible so that it can be accessed from eSTGt
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

% create mutation table
mutation_table = create_mutation_table(...
    my_run, ...
    num_of_ms_loci, ...
    path_mutation_table ...
);

% display to screen
disp(mutation_table);

% create tree
create_tree(...
    rules, ...
    my_run, ...
    path_newick, ...
    path_tree_png ...
);
