load dropout_prob;

% Dropout.P = the probability of obtaining a signal in each sample
% Dropout.Q = = the probability of obtaining a signal in each locus
num_of_samples = size(mutation_table, 1);
num_of_ms_loci = size(mutation_table, 2);

noise_prob = 0.00194622849;

sample_idx = randi([1 length(Dropout.P)], 1, num_of_samples);
P = Dropout.P(sample_idx);

ms_loci_idx = randi([1 length(Dropout.Q)], 1, num_of_ms_loci);
Q = Dropout.Q(ms_loci_idx);

threshold = rand(num_of_samples, num_of_ms_loci);
signal_prob = P'*Q;
DO = signal_prob < threshold;

disp(DO);
