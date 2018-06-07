#!/bin/bash

path_matlab='/usr/wisdom/matlabR2017a/bin'

${path_matlab}/matlab \
    -nodisplay \
    -nosplash \
    -nodesktop \
    -r "addpath('~/projects/clineage-simulation\eSTGt\eSTGt'); cd('src'); run('main.m'); exit;"

