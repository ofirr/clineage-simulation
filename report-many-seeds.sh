#!/bin/bash

path_root='/home/chun/projects/clineage-simulation/analysis/many-seeds/'

seeds=`find ${path_root} -name "seed-*" -type d`

for path_project in $seeds
do

    echo ${path_project}

    python make_html_report.py \
        --project ${path_project} \
        --config config.list \
        --exclude-mutation-table

done
