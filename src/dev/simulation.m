%
% change directory to ./src/simulation/dev first
%

clear;
close all;

path_user_defined_simul = '../../analysis/tmc/';
% path_working = '../../../examples/example-01';
addpath('C:\Users\chun\projects\eSTGt\eSTGt');
%addpath('/Users/dchun/projects/eSTGt/eSTGt/');
addpath('../simulation');
addpath(path_user_defined_simul);

% single_test();
generate_tmc_multi_cases();

function [] = write_cfg_json(cfg_json_filename, cfg_struct)
% write a cfg structure to a file in JSON format

    file_id = fopen(cfg_json_filename, 'w');
    fwrite(file_id, jsonencode(cfg_struct));
    fclose(file_id);

end

function [] = single_test()

    % construct a cfg structure
    cfg.title = "Dev Test";
    cfg.pathRelativeOutput = "outputs";
    cfg.addMutations = true;
    cfg.addAllelicDropOuts = false;
    cfg.addNoises = false;
    cfg.earlyStopPopulation = 9;

    % write a cfg structure to a file in JSON format
    cfg_json_filename = 'dev-test.json';
    write_cfg_json(cfg_json_filename, cfg);

    % run simulation
    run_simul('.', cfg_json_filename)

end

function [] = generate_tmc_multi_cases()

    ranges = 8:10;
    
    % initialize an array of cfg filenames 
    filenames_to_be_added = strings(length(ranges), 1);
    
    for case_num = ranges;
        
        % construct a cfg structure
        cfg.title = "Dev Test";
        cfg.pathRelativeOutput = sprintf('case-%02d', case_num);
        cfg.addMutations = true;
        cfg.addAllelicDropOuts = false;
        cfg.addNoises = false;
        cfg.earlyStopPopulation = case_num + 2;

        % write a cfg structure to a file in JSON format
        cfg_json_filename = sprintf('config-%02d.json', case_num);
        write_cfg_json(cfg_json_filename, cfg);
        
        % add cfg filenames to the array
        idx = case_num - ranges(1) + 1;
        filenames_to_be_added(idx, :) = string(cfg_json_filename);
        
        % run simulation
        run_simul('.', cfg_json_filename)

        % read simulation tree from generated newick file
        simulation_tree = phytreeread(fullfile(cfg.pathRelativeOutput, 'simulation.newick'));
        
        % get the number of leaves
        num_leaves = get(simulation_tree, 'NumLeaves');
        
        % change the title in cfg with the number of leaves
        cfg.title = sprintf("%d leaves", num_leaves);
        write_cfg_json(cfg_json_filename, cfg);
        
    end
    
    % write cfg filenames to `config.list`
    file_id = fopen('config.list', 'wt');
    for idx = 1:length(filenames_to_be_added)
        fwrite(file_id, filenames_to_be_added(idx, :));
        fwrite(file_id, newline);
    end
    fclose(file_id);

end

