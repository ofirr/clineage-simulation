#!/bin/bash

usage()
{
cat << EOF
USAGE: `basename $0` [options]

    -r  absolute path to simulation root where seed-* are placed

EOF
}

while getopts "r:h" OPTION
do
    case $OPTION in
        r) path_root=$OPTARG ;;
        h) usage; exit 1 ;;
        *) usage; exit 1 ;;
    esac
done

if [ -z "$path_root" ]
then
    usage
    exit 1
fi

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
