function [] = run_simul(path_working, config_json)
%% options

% `path_config` must be set from the calling script

% declare as global variable
global simul_options;

% load config.json and store into `simul_options`
simul_options = jsondecode(fileread(fullfile(path_working, config_json)));

%% clean up from any previous work
close all;

%% initialize

% set output path
path_output = fullfile(path_working, simul_options.pathRelativeOutput);

% create output path if not exists already
if ~exist(path_output, 'dir')
    mkdir(path_output);
end

% construct path for mutation table, newick, and png
path_mutation_table = fullfile(path_output, 'mutation_table.txt');
path_newick_without_distance = fullfile(path_output, 'simulation.newick');
path_newick_with_distance = fullfile(path_output, 'simulation.distance.newick');
path_tree_png_without_distance = fullfile(path_output, 'simulation.png');
path_tree_png_with_distance = fullfile(path_output, 'simulation.distance.png');

%% configuration

% use biallelic=false if not specified in the config
% (for backward compatibility)
if ~isfield(simul_options, 'biallelic')
    simul_options.biallelic = false;
end

% use biallelicInit=randperm if not specified in the config
% (for backward compatibility)
if ~isfield(simul_options, 'biallelicInit')
    simul_options.biallelicInit = 'randperm';
end

% use mutation speed 1.0 if not specified in the config
% (for backward compatibility)
if ~isfield(simul_options, 'mutationSpeed')
    simul_options.mutationSpeed = 1.0;
end

% use simulation.xml if not specified in the config
% (for backward compatibility)
if ~isfield(simul_options, 'programFile')
    simul_options.programFile = 'simulation.xml';
end

% disable WGA bias if not specified in the config
% (for backward compatibility)
if ~isfield(simul_options, 'wgaBias')
    simul_options.wgaBias = false;
end

% set allelic dropout threshold to NaN if not specified in the config
% (for backward compatibility)
if ~isfield(simul_options, 'adoFactor')
    simul_options.adoFactor = NaN;
end

% set defai;t mutation noise threshold if not specified in the config
% (for backward compatibility)
if ~isfield(simul_options, 'mutationNoiseThreshold')
    simul_options.mutationNoiseThreshold = 0.00194622849;
end

% monoallelic/biallelic support
if simul_options.biallelic
    % 1: paternal, 2: maternal
    alleles = 1:2;
else
    alleles = 1;
end

% load microsatellite mutation transition table
% declare as global variable so that it can be accessed from eSTGt
global ms_mutation_transition_prob;
global ms_idx_rptlen_mapping;
load('ms_mutation_transition_prob');

% min, max of ms repeat length in mutation transition table
max_ms_rptlen = max(ms_idx_rptlen_mapping);
min_ms_rptlen = min(ms_idx_rptlen_mapping);

% adjust ms mutation transition probabilities
ms_mutation_transition_prob = adjust_ms_mutation_transition_prob(...
    ms_mutation_transition_prob, ...
    simul_options.mutationSpeed ...
);
assert( isequal(size(ms_mutation_transition_prob), [max_ms_rptlen - min_ms_rptlen + 1, max_ms_rptlen - min_ms_rptlen + 1]) );

% parse eSTGt rules from the program file
rules = ParseeSTGProgram(simul_options.programFile);

% ensure reproducibility by using the specific seed to initialize randomizer
% the init as eSTGt
random_stream = RandStream('mcg16807', 'Seed', rules.Seed);
RandStream.setGlobalStream(random_stream);

% get the number of microsatellite loci from the file
% or use `size(om6_ms, 1)`;
if simul_options.biallelic
    num_of_ms1_loci = rules.Prod{1,1}.InternalStates.MS1.DupNum;
    num_of_ms2_loci = rules.Prod{1,1}.InternalStates.MS2.DupNum;

    if num_of_ms2_loci ~= num_of_ms2_loci
        error('Num of microsatellite loci must be identical in MS1 and MS2');
        return;
    end

    num_of_ms_loci = num_of_ms1_loci;
else
    num_of_ms_loci = rules.Prod{1,1}.InternalStates.MS.DupNum;
end

% setting `InitVal` to -1 will signal that ms repeat length for each loci
% should be initialized before introducing mutation
if simul_options.biallelic
    rules.Prod{1,1}.InternalStates.MS1.InitVal = -1;
    rules.Prod{1,1}.InternalStates.MS2.InitVal = -1;
else
    rules.Prod{1,1}.InternalStates.MS.InitVal = -1;
end

% load om6 microsatellite ids and repeat numbers
% declare as global variable so that it can be accessed from eSTGt
global om6_ms;

% read from csv, skip the first row (header)
om6_ms = csvread('om6_ms_only_ac_28x28.csv', 1, 0);

% om6_ms might have enough loci to cover the requested length
% figure out how many is required
num_copies = round( num_of_ms_loci / size(om6_ms, 1) ) + 1;

% concatenate om6_ms + om6_ms + ... (`num_copies` times)
om6_ms_n_copied = repmat(om6_ms, num_copies, 1);

% update oms6_ms
om6_ms = om6_ms_n_copied(1:num_of_ms_loci, :);

% this will be used to initialize the root cell
global om6_ms_alleles;
om6_ms_alleles = cell(alleles);
if simul_options.biallelic

    switch simul_options.biallelicInit

        case 'randperm'
            % we shuffle both paternal, maternal
            om6_ms_alleles(1) = { om6_ms(randperm(num_of_ms_loci), :) };
            om6_ms_alleles(2) = { om6_ms(randperm(num_of_ms_loci), :) };

        case 'diffdist'
            % for paternal, we shuffle
            om6_ms_alleles(1) = { om6_ms(randperm(num_of_ms_loci), :) };
            % for maternal, we use repeat length difference distribution
            
            % read probability distrubition from a file
            % use only the first column
            pm_allele_diff_prob = csvread('pm_allele_diff_prob.csv', 1, 1);

            % difference between allele1 and allele2's repeat length
            % (without direction)
            diff_allel1_allele2 = datasample(...
                1:length(pm_allele_diff_prob), ...
                num_of_ms_loci, ...
                'Replace', true, ...
                'Weights', pm_allele_diff_prob ...
            );

            % -1 to make 0 means no change
            diff_allel1_allele2 = diff_allel1_allele2 - 1;

            % random direction (0 or 1)
            direction = randi([0, 1], 1, num_of_ms_loci);
            % change 0 to -1
            direction( direction == 0 ) = -1;

            % difference between allele1 and allele2's repeat length
            % (with direction)
            diff_allel1_allele2 = diff_allel1_allele2 .* direction;

            % take allele1 and add difference, which gives us allele2
            om6_ms_alleles(2) = om6_ms_alleles(1);
            allele2 = om6_ms_alleles{1}(:,2) + diff_allel1_allele2';
            % repeat length must be e.g. between 5 and 32
            allele2(allele2 > max_ms_rptlen) = max_ms_rptlen;
            allele2(allele2 < min_ms_rptlen) = min_ms_rptlen;
            om6_ms_alleles{2}(:,2) = allele2;

        otherwise
            error('Unknown biallelic init method used');
    end
else
    % for mono-allelic case, no shuffling to maintain backward compatibility
    om6_ms_alleles(1) = { om6_ms };
end

% convert from actual ms repeat lengths to indexes
% this is required by ms_mutation_transition_prob
% e.g. repeat length 5 is mapped to index 1
for idx1 = 1:length(ms_idx_rptlen_mapping)
    idx2 = find(om6_ms(:, 2)' == ms_idx_rptlen_mapping(idx1));
    om6_ms(idx2, 3) = idx1;
end

%% simulation

% run simulation
[ runs, RunsData ] = RunSim(rules, rules.Seed, rules.SimTime);

% the very first run (we only have one run in fact)
my_run = runs(1);

fprintf("End Time: %f\n", my_run.T(end));
% fprintf("End Population: %d\n", my_run.X(end));
fprintf("End Population: %d\n", sum(my_run.X(end, :)));

%% create tree

% create tree
phytree_obj = create_tree(...
    rules, ...
    my_run, ...
    path_newick_without_distance, ...
    path_newick_with_distance, ...
    path_tree_png_without_distance, ...
    path_tree_png_with_distance ...
);
fprintf("After create_tree\n");
%% add dropouts and noises

mutation_tables = cell(alleles);

fprintf("After mutation_tables\n");

% fixme: make configurable in config.json
has_root = true;

for allele = 1:length(alleles)

    % create mutation table purely based on eSTGt without any post modification
    mutation_table = create_mutation_table(...
        my_run, ...
        num_of_ms_loci, ...
        simul_options.biallelic, ...
        allele ...
    );

    % get number of samples, number of microsatellite loci
    num_of_ms_loci = size(mutation_table, 1);
    num_of_samples = size(mutation_table, 2);

    if simul_options.addNoises

        % generate mutation noise table
        %  0: don't change
        %  1: increment microsatellite repeat length by 1
        % -1: decrement microsatellite repeat length by 1
        mutation_noise_table = generate_mutation_noise_table(...
            num_of_samples, ...
            num_of_ms_loci, ...
            simul_options.mutationNoiseThreshold ...
        );

        % add mutation noises
        mutation_table = mutation_table + mutation_noise_table;

    end

    if simul_options.addAllelicDropOuts

        % load allelic dropout probability table
        load('allelic_dropout_prob');

        % get allelic dropout truth table
        % 0: don't drop, 1: drop
        ado_truth_table = generate_ado_truth_table(...
            num_of_samples, ...
            num_of_ms_loci, ...
            Dropout, ...
            simul_options.adoFactor ...
        );

        % apply allelic dropout to the mutation table
        % dropped-out will be marked as NaN (1 becomes NaN)
        mutation_table(ado_truth_table) = NaN;

    end

    % add root cell if necessary
    if has_root
        % om6_ms_alleles{1} : initial repeat lengths for paternal
        % om6_ms_alleles{2} : initial repeat lengths for maternal
        mutation_table(:, num_of_samples + 1) = om6_ms_alleles{allele}(1:num_of_ms_loci, 2);
    end

    % get mutation table with column/row header
    % this returns a cell array
    mutation_table_mono = convert_to_mutation_table_with_header(...
        my_run, ...
        mutation_table, ...
        has_root ...
    );

    % write mutation table to a file
    save_mutation_table( ...
        fullfile(path_output, sprintf('mutation_table.%d.txt', allele)), ...
        mutation_table_mono ...
    );

    % append
    mutation_tables(allele) = { mutation_table };

end

fprintf("After alleles for loop\n");

%% add WGA bias proportions
if simul_options.biallelic
    if simul_options.wgaBias
        % generate WGA bias proportions
        wga_bias_proportions = generate_wga_bias(...
            num_of_samples, ...
            num_of_ms_loci ...
        );
    else
        % 50:50 between paternal and maternal
        wga_bias_proportions = ones(num_of_ms_loci, num_of_samples) - 0.5;
    end

    if has_root
        % add proportion for root cell
        % no biad, thus set to 0.5
        wga_bias_proportions(:, num_of_samples + 1) = ones(num_of_ms_loci, 1) * 0.5;
    end

    % handle allelic dropout case
    ado1 = isnan(mutation_tables{1,1}); % dropouts in paternal
    ado2 = isnan(mutation_tables{1,2}); % dropouts in maternal
    wga_bias_proportions(ado1) = 0.0; % only maternal seen
    wga_bias_proportions(ado2) = 1.0; % only paternal seen
    wga_bias_proportions(ado1 & ado2) = NaN; % both not seen

    % append wga bias proportions
    mutation_tables(end + 1) = { wga_bias_proportions };
end

fprintf("After WGA bias\n");

%% merge
mutation_table = merge_mutation_tables(mutation_tables);

fprintf("After merge\n");
%% save

% get mutation table with column/row header
% this returns a cell array
mutation_table_final = convert_to_mutation_table_for_tmc(...
        my_run, ...
        mutation_table, ...
        has_root ...
    );

% mutation_table_final = convert_to_mutation_table_with_header(...
%         my_run, ...
%         mutation_table, ...
%         has_root ...
%     );

% write mutation table to a file
save_mutation_table(path_mutation_table, mutation_table_final);

% write workspace to a file
save(fullfile(path_output, 'workspace.mat'), 'Variablename', '-v7.3');

fprintf("matlab done\n");