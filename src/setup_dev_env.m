%% code path

addpath('./reconstruction');
addpath('./simulation');

%% path to eSTGt (Windows)

addpath('C:\Users\chun\projects\eSTGt\eSTGt');

%% path to eSTGt (Mac)

addpath('/Users/dchun/projects/eSTGt/eSTGt/');

%% Reconstruction

path_working='../analysis/tmc/case-09/';
%path_working='../examples/example-01/outputs';

path_simulation_tree = fullfile(path_working, 'simulation.newick');
path_reconstructed_tree = fullfile(path_working, 'reconstructed.newick');
path_diff_metrics = fullfile(path_working, 'diff-score.json');

%% Simulation

path_working='../examples/example-01';

addpath(path_working);
