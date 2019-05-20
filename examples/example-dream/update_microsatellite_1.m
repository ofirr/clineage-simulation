function [ newMS ] = update_scar_1( MS )
% updates the microsatellite repeat number

    % 1 for paternal
    % 2 for maternal
    newMS = update_scar(MS, 1);

end
