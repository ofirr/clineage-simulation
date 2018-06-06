function [ newMS ] = update_microsatellite( MS )
% updates the microsatellite repeat number

    rand_seed = RandStream('mlfg6331_64');

    % access to microsatellite mutation transition table
    global ms_mutation_transition_prob;
    
    % check if MS has all repeat number -1, which means it requires
    % reinitialization
    if sum( MS ~= -1 ) == 0   
        
        % access to om6 microsatellite ids and repeat numbers read
        global om6_ms;
        
        % reinitialize using the ms repeat numbers
        MS = repmat(om6_ms(1:length(MS), 2)', 1);        
        
    end
    
    for i = 1:length(MS)

        try
            probs = ms_mutation_transition_prob(MS(i), :);
        catch
            fprintf("error: %d\n", i);
        end        
        
        %fixme: with rand_seed, barely changes
        new_idx = datasample(...
            1:length(probs), ...
            1, ...
            'Replace', true, ...
            'Weights', probs ...
        );
        
        newMS(i) = new_idx;
        
    end

    return;



    Mu = 1/1000; % the mutation rate (10^-3)

    n = length(MS);
    MutateVector = binornd(1,Mu,1,n);
    MutDirection = binornd(MutateVector, 1/2);
    newMS = MS + (2*MutDirection - MutateVector);

end

