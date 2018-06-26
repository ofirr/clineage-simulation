#!/bin/bash

path_root='/home/chun/projects/clineage-simulation/analysis/many-seeds/'

seeds=`find ${path_root} -name "seed-*" -type d`

for seed in $seeds
do

    path_project="${path_root}/seed-${seed}"

    ./sge-submit.sh \
        -p ${path_project} \
        -c config.list

done
