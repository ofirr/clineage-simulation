function [ newMS ] = update_microsatellite( MS )
% updates the microsatellite repeat number

    Mu = 1/1000; % the mutation rate (10^-3)

    n = length(MS);
    MutateVector = binornd(1,Mu,1,n);
    MutDirection = binornd(MutateVector, 1/2);
    newMS = MS + (2*MutDirection - MutateVector);

end

