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
    ms_repeat_lengths ...
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

% load allelic dropout probability table
load('allelic_dropout_prob');

% get number of samples, number of microsatellite loci
num_of_samples = size(mutation_table, 1);
num_of_ms_loci = size(mutation_table, 2);

% get allelic dropout truth table
% 0: don't drop, 1: drop
ado_truth_table = generate_ado_truth_table(...
    num_of_samples, ...
    num_of_ms_loci, ...
    Dropout ...
);

% apply allelic dropout to the mutation table
% dropped-out will be marked as NaN
mutation_table{:,:}(ado_truth_table) = NaN;

disp(mutation_table);

% write mutation table to a file
writetable(...
    mutation_table, ...
    path_mutation_table, ...
    'WriteVariableNames', true, ...
    'WriteRowNames', true, ...
    'Delimiter', 'tab' ...
);

