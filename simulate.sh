#!/bin/bash

path_matlab='/usr/wisdom/matlabR2017a/bin'
path_matlab='/Applications/MATLAB_R2017b.app/bin'

path_eSTGt='~/projects/eSTGt/eSTGt'

path_config='/Users/dchun/projects/clineage-simulation/src/config.json'

${path_matlab}/matlab \
    -nodisplay \
    -nosplash \
    -nodesktop \
    -r "addpath('${path_eSTGt}'); cd('src'); run_simul('${path_config}'); exit;"
