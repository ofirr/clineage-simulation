function [ newMS ] = update_microsatellite( MS, allele )
% updates the microsatellite repeat number

    rand_seed = RandStream('mlfg6331_64');

    % access to simulation options
    global simul_options;

    % access to microsatellite mutation transition table
    global ms_mutation_transition_prob;

    % mapping between index and ms repeat length
    global ms_idx_rptlen_mapping;

    % check if MS has all repeat number -1, which means it requires
    % reinitialization
    if sum( MS ~= -1 ) == 0

        % access to om6 microsatellite ids and repeat numbers read
        global om6_ms_alleles;

        % reinitialize using the ms repeat numbers with biallelic
        % om6_ms_alleles{1} : initial repeat lengths for paternal
        % om6_ms_alleles{2} : initial repeat lengths for maternal
        MS = om6_ms_alleles{allele}(randperm(length(MS)), 2)';

    end

    % don't cause mutations if the option is turned off
    if ~simul_options.addMutations
        newMS = MS;
        return;
    end

    for i = 1:length(MS)

        try
            % convert ms repeat length to index
            idx = find(ms_idx_rptlen_mapping == MS(i));

            % using the index, get probability distribution
            probs = ms_mutation_transition_prob(idx, :);
        catch
            fprintf("error: %d\n", i);
        end

        %fixme: with rand_seed, barely changes

        % get index that corresponds to ms repeat length using probability
        % distribution
        new_idx = datasample(...
            1:length(probs), ...
            1, ...
            'Replace', true, ...
            'Weights', probs ...
        );

        % convert index to ms repeat length
        newMS(i) = ms_idx_rptlen_mapping(new_idx);

    end

end
