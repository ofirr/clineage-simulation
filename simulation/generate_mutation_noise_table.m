function [mutation_noise_table] = generate_mutatino_noise_table(num_of_samples, num_of_ms_loci, noise_threshold)

tmp1 = ( rand(num_of_ms_loci, num_of_samples) < noise_threshold );
tmp2 = 1 - 2 * (rand(num_of_ms_loci, num_of_samples) < 0.5);
mutation_noise_table = tmp1 .* tmp2;
