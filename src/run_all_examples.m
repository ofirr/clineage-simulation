clear;
clc;

%% code path

addpath('./simulation');

%% path to eSTGt (Windows)

addpath('C:\Users\chun\projects\eSTGt\eSTGt');

%% run all

list = readtable('./all-examples.csv', 'Delimiter', ',');

for row = 1:size(list, 1)
    
    path_working = list.path_working{row};
    config_file = list.config_file{row};
    
    fprintf('\n---------------------------------------------------------------\n');
    fprintf('%-50s %s\n', path_working, config_file);
  
    addpath(path_working);
    
    run_simul(path_working, config_file);
      
    rmpath(path_working);
end

close all;
