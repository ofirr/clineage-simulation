#!/bin/bash

for nn in {1..14}
do

  path_project="/home/chun/projects/clineage-simulation/analysis/tmc/tmc-`printf '%03d' $nn`"

  echo ${path_project}

  python make_html_report.py \
    --project ${path_project} \
    --config config.list \
    --exclude-mutation-table

done
