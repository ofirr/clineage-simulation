#!/bin/bash

path_root='/home/chun/projects/clineage-simulation/analysis/many-seeds/'

seeds=`find ${path_root} -maxdepth 1 -name "seed-*" -type d`

for path_project in $seeds
do

    echo ${path_project}

    ./sge-submit.sh \
        -p ${path_project} \
        -c config.list

done
