%
% change directory to ./src/simulation/dev first
%

% addpath('C:\Users\chun\projects\eSTGt\eSTGt');
addpath('/Users/dchun/projects/eSTGt/eSTGt/');

addpath('..')
% addpath('../../../examples/example-01')
addpath('../../../analysis/tmc/')

% run_simul('../../../examples/example-01', 'config.json')
run_simul('../../../analysis/tmc', 'config-04.json')
