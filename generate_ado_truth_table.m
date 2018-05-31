function [ado_truth_table] = generate_ado_truth_table(num_of_samples, num_of_ms_loci, dropout_prob)

% dropout_prob.P = the probability of obtaining a signal in each sample
% dropout_prob.Q = = the probability of obtaining a signal in each locus

sample_idx = randi([1 length(dropout_prob.P)], 1, num_of_samples);
P = dropout_prob.P(sample_idx);

ms_loci_idx = randi([1 length(dropout_prob.Q)], 1, num_of_ms_loci);
Q = dropout_prob.Q(ms_loci_idx);

threshold = rand(num_of_samples, num_of_ms_loci);
signal_prob = P'*Q;
ado_truth_table = signal_prob < threshold;
