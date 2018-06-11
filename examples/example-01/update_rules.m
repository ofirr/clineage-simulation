function [ Rules ] = update_rules( Rules, T, X )
% updates rules during the transition

    global simul_options;

    for i = 1:length(X)
        Pop.( Rules.AllNames{i} ) = X(i);
    end

    for i = 1:length(Rules.StartNames)
        I.( Rules.StartNames{i} ) = i;
    end

    % early stop if the population of C is greater than `earlyStopPopulation`
    % early stop only if `earlyStopPopulation` is defined and not zero
    if isfield(simul_options, 'earlyStopPopulation')
        if simul_options.earlyStopPopulation ~= 0
            if Pop.C > simul_options.earlyStopPopulation
                Rules.Prod{I.C}.Rate = 0;
            end
        end
    end
end
