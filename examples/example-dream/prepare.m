% based on ex-vivo

% column: after mutation
% row:    before mutation


% 28X28
% e.g. probability of mutation causing 0 to become 1
%      ms_mutation_transition_prob(1, 2) --> 0.10 (10.0%)
ms_mutation_transition_prob = [
    0.90	0.10
    0.00	1.00
];

% mapping between index and ms repeat length
% e.g. repeat length 5 is mapped to index 1
ms_idx_rptlen_mapping = [:];

% save as mat file
save(...
    'scar_irreversible_mutation_transition_prob.mat', ...
    'scar_irreversible_mutation_transition_prob', 'ms_idx_rptlen_mapping' ...
);
