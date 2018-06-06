%% clean up from any previous work
close all;
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
path_newick = fullfile(path_output, 'simulation.newick');
path_tree_png = fullfile(path_output, 'simulation.png');

%% simulation

% load microsatellite mutation transition table
% declare as global variable so that it can be accessed from eSTGt
global ms_mutation_transition_prob;
load('ms_mutation_transition_prob');

% load om6 microsatellite ids and repeat numbers
% declare as global variable so that it can be accessed from eSTGt
global om6_ms;
om6_ms = csvread('om6_ms_only_legit_ac.csv', 1, 0);

% convert from actual ms repeat lengths to indexes
% this is required by ms_mutation_transition_prob
% e.g. repeat length 5 is mapped to index 1
for idx1 = 1:length(ms_repeat_lengths)
    idx2 = find(om6_ms(:, 2)' == ms_repeat_lengths(idx1));
    om6_ms(idx2, 3) = idx1;
end

% parse eSTGt rules from the program file
program_file = 'simulation.xml';
rules = ParseeSTGProgram(program_file);

% get the number of microsatellite loci from the file
% overwrite the rule
% rules.Prod{1,1}.InternalStates.MS.DupNum = size(om6_ms, 1);
rules.Prod{1,1}.InternalStates.MS.DupNum = 10;
num_of_ms_loci = rules.Prod{1,1}.InternalStates.MS.DupNum;

% overwrite the rule
rules.Prod{1,1}.InternalStates.MS.InitVal = -1;

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

% get number of samples, number of microsatellite loci
num_of_ms_loci = size(mutation_table, 1);
num_of_samples = size(mutation_table, 2);

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

% add root cell
has_root = true;
mutation_table(:, num_of_samples + 1) = om6_ms(1:num_of_ms_loci, 2);

% get mutation table with column/row header
% this returns a cell array
mutation_table_final = convert_to_mutation_table_for_tmc(...
        my_run, ...
        mutation_table, ...
        has_root ...
    );

% write mutation table to a file
switch class(mutation_table_final)
    
    case 'table'
        
        writetable(...
            mutation_table_final, ...
            path_mutation_table, ...
            'WriteVariableNames', true, ...
            'WriteRowNames', true, ...
            'Delimiter', 'tab' ...
        );
    
    case 'cell'

        % open a file
        file_out = fopen(path_mutation_table, 'w');
        
        % iterate through rows in the mutation table
        for row = 1:size(mutation_table_final, 1)
            % convert a row in the cell array to a string array
            line = string( mutation_table_final(row,:) );
            % replace any missing to a text "NaN"
            line( ismissing(line) ) = "NaN";
            % concatenate with a tab characeter
            line = strjoin( line, '\t' );
            % write to a file
            fprintf(file_out, "%s\n", line);
        end
        
        % close the file
        fclose(file_out);
        
end
