#!/bin/bash

usage()
{
cat << EOF
USAGE: `basename $0` [options]

	-b	path to program (e.g. /home/chun/projects/clineage-simulation)
	-p	path to project (e.g. ./examples/example-02)
	-c	config file (e.g. config.json)

EOF
}

while getopts “b:p:c:h” OPTION
do
    case $OPTION in
    	b) path_program=$OPTARG ;;
		p) path_project=$OPTARG ;;
		c) config_file=$OPTARG ;;
		h) usage; exit 1 ;;
		*) usage; exit 1 ;;
	esac
done

if [ -z "$path_program" ] || [ -z "$path_project" ] || [ -z "$config_file" ]
then
    usage
    exit 1
fi

qsub \
	-N test \
	-q all2.q \
	-cwd \
	./sge-run-simul.sh ${path_program} ${path_project} ${config_file}
