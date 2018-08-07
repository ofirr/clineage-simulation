function [mutation_noise_table] = generate_mutation_noise_table(num_of_samples, num_of_ms_loci, noise_threshold)

% generate a n-by-m matrix with random numbers between 0 and 1
% where n is the number of ms loci, m is the number of samples
% then convert to a binary matrix
% 0: no noise
% 1: add noise
tmp1 = ( rand(num_of_ms_loci, num_of_samples) < noise_threshold );

% generate a n-by-m matrix with random numbers between 0 and 1
% where n is the number of ms loci, m is the number of samples
% then make the half -1, the other half 1
% -1: decrease by one base (if decides to add noise)
% +1: increase by one base (if decides to add noise)
tmp2 = 1 - 2 * (rand(num_of_ms_loci, num_of_samples) < 0.5);

% multiply tmp1 and tmp2
mutation_noise_table = tmp1 .* tmp2;
