function [ado_truth_table] = generate_ado_truth_table(num_of_samples, num_of_ms_loci, dropout_prob, dropout_factor)

% dropout_prob.P = the probability of obtaining a signal in each sample
% dropout_prob.Q = = the probability of obtaining a signal in each locus

sample_idx = randi([1 length(dropout_prob.P)], 1, num_of_samples);
P = dropout_prob.P(sample_idx);

ms_loci_idx = randi([1 length(dropout_prob.Q)], 1, num_of_ms_loci);
Q = dropout_prob.Q(ms_loci_idx);

% generate threshold values (randomized)
threshold = rand(num_of_ms_loci, num_of_samples);

% compute signal values
% dropout_factor (dof)
% =1: use P & Q as is
% <1: drop more than as is
% >1: drop less than as is
signal_prob = Q'*P * dropout_factor;

% signal that is less than threshold will be marked as dropout
% 1 means drop
% 0 means keep
ado_truth_table = signal_prob < threshold;
