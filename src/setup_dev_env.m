%% code path

addpath('./reconstruction');
addpath('./simulation');

%% path to eSTGt (Windows)

addpath('C:\Users\chun\projects\eSTGt\eSTGt');

%% path to eSTGt (Mac)

addpath('/Users/dchun/projects/eSTGt/eSTGt/');

%% path to eSTGt (math102-lx)

addpath('~/projects/clineage-simulation/eSTGt/eSTGt');

%% Reconstruction

path_working='../analysis/tmc-004/case-01/';
%path_working='../examples/example-02/outputs';

path_simulation_tree = fullfile(path_working, 'simulation.newick');
path_reconstructed_tree = fullfile(path_working, 'reconstructed.newick');
path_sisters_count = fullfile(path_working, 'sisters.csv');
path_diff_metrics = fullfile(path_working, 'diff-score.json');

%% Simulation

path_working='../analysis/tmc-004';

addpath(path_working);
