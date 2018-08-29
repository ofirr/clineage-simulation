#!/bin/bash

if [ ! -x "$(command -v qsub)" ]
then
    echo "qsub not found. Aborted."
    exit 1
fi

# default project name
project_name='simulation'

usage()
{
cat << EOF
USAGE: `basename $0` [options]

    -p	path to project (e.g. ./examples/example-02)
    -c	config file (e.g. config.json)
    -s	simulate tree only (no reconstruction)
    -n	project name (default: "${project_name}")

EOF
}

simulate_tree_only='';

while getopts "n:p:c:sh" OPTION
do
    case $OPTION in
        n) project_name=$OPTARG ;;
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

# set unique job name
job_name="job-`uuidgen`"

out=`qsub \
    -N ${job_name} \
    -q all2.q \
    -cwd \
    ./sge-run-simul.sh ${path_project} ${config_file} ${simulate_tree_only}`

# extract SGE job ID from the qsub output
# e.g. Your job 7588748 ("simulation") has been submitted
job_id=`echo ${out} | awk -F' ' '{print $3}'`

echo ${job_id}

# record
echo "${job_id},${path_project},${config_file}" >> ${project_name}.job-info
