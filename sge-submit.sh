#!/bin/bash

if [ ! -x "$(command -v qsub)" ]
then
    echo "qsub not found. Aborted."
	exit 1
fi

usage()
{
cat << EOF
USAGE: `basename $0` [options]

	-p	path to project (e.g. ./examples/example-02)
	-c	config file (e.g. config.json)
	-s  simulate tree only (no reconstruction)

EOF
}

simulate_tree_only='';

while getopts "p:c:sh" OPTION
do
    case $OPTION in
		p) path_project=$OPTARG ;;
		c) config_file=$OPTARG ;;
		s) simulate_tree_only='--simulate-tree-only' ;;
		h) usage; exit 1 ;;
		*) usage; exit 1 ;;
	esac
done

if [ -z "$path_project" ] || [ -z "$config_file" ]
then
    usage
    exit 1
fi

qsub \
	-N simulation \
	-q all2.q \
	-cwd \
	./sge-run-simul.sh ${path_project} ${config_file} ${simulate_tree_only}
