#!/bin/bash

usage()
{
cat << EOF
USAGE: `basename $0` [options]

    -s    seed

EOF
}

while getopts "s:h" OPTION
do
    case $OPTION in
        s) seed=$OPTARG ;;
        h) usage; exit 1 ;;
        *) usage; exit 1 ;;
    esac
done

if [ -z "$seed" ]
then
    usage
    exit 1
fi

for nn in {3..13}
do

    path_project="/home/chun/projects/clineage-simulation/analysis/tmc/seed-${seed}/n-`printf '%03d' $nn`"

    echo ${path_project}

    python make_html_report.py \
        --title "Report (${seed}-${nn})" \
        --project ${path_project} \
        --config config.list \
        --exclude-mutation-table

done
