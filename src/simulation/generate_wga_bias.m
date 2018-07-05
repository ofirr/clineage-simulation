function [wga_bias_proportion_table] = generate_wga_bias(num_of_samples, num_of_ms_loci)

% generate a n-by-m matrix with random numbers between 0 and 1
% where n is the number of ms loci, m is the number of samples
% 0.5 means uniform across paternal and maternal
paternal = rand(num_of_ms_loci, num_of_samples);
% maternal = 1 - paternal;

wga_bias_proportion_table = paternal;
