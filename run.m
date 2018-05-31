%% clean up from any previous work
clear;
clc;

%% initialize

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

%% simulation

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

%% create tree

% create tree
create_tree(...
    rules, ...
    my_run, ...
    path_newick, ...
    path_tree_png ...
);

%% create mutation table

% create mutation table purely based on eSTGt without any post modification
mutation_table = create_mutation_table(...
    my_run, ...
    num_of_ms_loci, ...
    ms_repeat_lengths ...
);

% display to screen
pretty_print(my_run, mutation_table);

% get number of samples, number of microsatellite loci
num_of_samples = size(mutation_table, 1);
num_of_ms_loci = size(mutation_table, 2);

% mutation noise threshold
mutation_noise_threshold = 0.00194622849;

% generate mutation noise table
%  0: don't change
%  1: increment microsatellite repeat length by 1
% -1: decrement microsatellite repeat length by 1
mutation_noise_table = generate_mutation_noise_table(...
    num_of_samples, ...
    num_of_ms_loci, ...
    mutation_noise_threshold ...
);

% add mutation noises
mutation_table = mutation_table + mutation_noise_table;

% display to screen
pretty_print(my_run, mutation_table);

% load allelic dropout probability table
load('allelic_dropout_prob');

% get allelic dropout truth table
% 0: don't drop, 1: drop
ado_truth_table = generate_ado_truth_table(...
    num_of_samples, ...
    num_of_ms_loci, ...
    Dropout ...
);

% apply allelic dropout to the mutation table
% dropped-out will be marked as NaN
mutation_table(ado_truth_table) = NaN;

pretty_print(my_run, mutation_table);

% get mutation table with column/row header
mutation_table_with_header = convert_to_mutation_table_with_header(my_run, mutation_table);

% write mutation table to a file
writetable(...
    mutation_table_with_header, ...
    path_mutation_table, ...
    'WriteVariableNames', true, ...
    'WriteRowNames', true, ...
    'Delimiter', 'tab' ...
);
