#!/bin/bash

usage()
{
cat << EOF
USAGE: `basename $0` [options]

    -p	path to example project (e.g. ./examples/example-01)
    -c	config file (e.g. config.json)

EOF
}

while getopts "p:c:sh" OPTION
do
    case $OPTION in
        p) path_project=$OPTARG ;;
        c) config_file=$OPTARG ;;
        h) usage; exit 1 ;;
        *) usage; exit 1 ;;
    esac
done

if [ -z "$path_project" ] || [ -z "$config_file" ]
then
    usage
    exit 1
fi

python simulator.py \
  --env config.math102-lx.env \
  --project ${path_project} \
  --config ${config_file}

python make_html_report.py \
  --project ${path_project} \
  --config ${config_file}
