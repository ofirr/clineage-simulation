function [new_prob_matrix] = adjust_ms_mutation_transition_prob(old_prob_matrix, speed)
% speed 1: intact
% speed <1: slower mutation rate
% speed >1: faster mutation rate

% fix: one row in Noa's table sums up to greater 1.0
old_prob_matrix(end - 1, end - 2) = old_prob_matrix(end - 1, end - 2) - 0.0490;

% table size
vec_size = size(old_prob_matrix);

% non-diagonal elements multiplied by speed
nondiag = (1 - eye(vec_size)) * speed;

% non-diagonal elements
new_prob_matrix = old_prob_matrix .* nondiag;

% sum up probabilities in each row
sum_each_row = sum(new_prob_matrix, 2);

% 1 - probabilities in each row which will be used to update the diagonal
% elements
new_diag_values = 1 - sum_each_row;

% find indexes for diagonal elements in the matrix
idx_diag = find( eye(vec_size) == 1 );

% update the diagonal elements in the matrix
new_prob_matrix(idx_diag) = new_diag_values;

% ensure that the sum of probabilities in each row is 1.0
sum_new_each_row = sum(new_prob_matrix, 2);
assert( sum(sum_new_each_row) == 30 );
