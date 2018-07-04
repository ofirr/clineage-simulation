#!/bin/bash

path_root='/home/chun/projects/clineage-simulation/analysis/many-seeds/'

seeds=`find ${path_root} -maxdepth 1 -name "seed-*" -type d`

for path_project in $seeds
do

    echo ${path_project}

    title=`echo ${path_project} | awk -F'/' '{print $(NF)}'`

    python make_html_report.py \
        --title ${title} \
        --project ${path_project} \
        --config config.list \
        --exclude-mutation-table

done
