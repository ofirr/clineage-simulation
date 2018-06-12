%
% change directory to ./src/simulation/dev first
%

clear;
close all;

path_user_defined_simul = '../../analysis/tmc/';
% path_working = '../../../examples/example-01';
% addpath('C:\Users\chun\projects\eSTGt\eSTGt');
addpath('/Users/dchun/projects/eSTGt/eSTGt/');
addpath('../simulation');
addpath(path_user_defined_simul);

% single_test();
generate_tmc_multi_cases();

function [] = write_cfg_json(cfg_json_filename, cfg_struct)

    file_id = fopen(cfg_json_filename, 'w');
    fwrite(file_id, jsonencode(cfg_struct));
    fclose(file_id);

end

function [] = single_test()

    cfg.title = "Dev Test";
    cfg.pathRelativeOutput = "outputs";
    cfg.addMutations = true;
    cfg.addAllelicDropOuts = false;
    cfg.addNoises = false;
    cfg.earlyStopPopulation = 9;

    cfg_json_filename = 'dev-test.json';
    write_cfg_json(cfg_json_filename, cfg);

    run_simul('.', cfg_json_filename)

end

function [] = generate_tmc_multi_cases()

    for case_num = 8:20
        
        cfg.title = "Dev Test";
        cfg.pathRelativeOutput = sprintf('case-%02d', case_num);
        cfg.addMutations = true;
        cfg.addAllelicDropOuts = false;
        cfg.addNoises = false;
        cfg.earlyStopPopulation = case_num + 2;

        cfg_json_filename = sprintf('config-%02d.json', case_num);
        write_cfg_json(cfg_json_filename, cfg);
        
        run_simul('.', cfg_json_filename)

        simulation_tree = phytreeread(fullfile(cfg.pathRelativeOutput, 'simulation.newick'));
        
        num_leaves = get(simulation_tree, 'NumLeaves');
        
        cfg.title = sprintf("%d leaves", num_leaves);
        write_cfg_json(cfg_json_filename, cfg);
        
    end

end

