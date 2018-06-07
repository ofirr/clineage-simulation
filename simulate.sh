#!/bin/bash

path_matlab='/usr/wisdom/matlabR2017a/bin'
path_eSTGt='~/projects/eSTGt/eSTGt'

${path_matlab}/matlab \
    -nodisplay \
    -nosplash \
    -nodesktop \
    -r "addpath('${path_eSTGt}'); cd('src'); run('main.m'); exit;"

