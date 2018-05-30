function [ Rules ] = update_rules( Rules, T, X )
% updates rules during the transition

    % access to microsatellite mutation transition table
    global ms_mutation_transition_prob;

    disp( ms_mutation_transition_prob(1, 2) );
    return

    CLONE_SIZE = 1000;

    for i=1:length(X)
        Pop.(Rules.AllNames{i})=X(i);
    end

    for i=1:length(Rules.StartNames)
        I.(Rules.StartNames{i})=i;
    end

    disp(Pop);
    disp("-------------------");

    %disp(Rules.Prod{1}.InternalStates.('Gen'));
    %disp(Rules.Prod{1});
    %disp(Rules.Prod{1}.InternalStatesNames{2});
    

    % if simTime > 2
    if T > 2

        % switch
        Rules.Prod{I.P}.Rate = rand();
        Rules.Prod{I.P}.Probs = [0.1 0.1 0.8];

    end

    if Pop.M2 >= 50
        Rules.Prod{I.M2}.Rate = 0.0;
        Rules.Prod{I.M2}.Probs = [0.01 0];
    end

    if Pop.M >= 50
        Rules.Prod{I.M}.Rate = 0.0;
        Rules.Prod{I.M}.Probs = [0.01];
    end    

    if T > 20
        Rules.Prod{I.P2}.Rate = rand();
        Rules.Prod{I.P2}.Probs = [0 0];

        Rules.Prod{I.CTC}.Probs = [0 0.1 0.9];
    end

    % disp(Nodes);
end
