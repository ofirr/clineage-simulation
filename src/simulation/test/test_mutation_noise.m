num_of_samples = size(mutation_table, 1);
num_of_ms_loci = size(mutation_table, 2);

NoiseMS = 0.00194622849;
NoiseMS = 0.5;

MSNoise = getMSNoise(num_of_samples, num_of_ms_loci,NoiseMS);

function MSNoise = getMSNoise(NumSamp,NumLoc,p)
MSNoise = (rand(NumLoc,NumSamp) < p);
tmp = 1-2*(rand(NumLoc,NumSamp) < 0.5);
MSNoise = MSNoise.*tmp;

end