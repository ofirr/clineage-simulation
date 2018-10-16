#!/bin/bash

if [ ! -x "$(command -v qsub)" ]
then
    echo "qsub not found. Aborted."
    exit 1
fi

# default project name
project_name='simulation'
queue_name='all2.q'

usage()
{
cat << EOF
USAGE: `basename $0` [options]

    -p	absolute path to project (e.g. ~/examples/example-02)
    -c	config file (e.g. config.json)
    -s	simulate tree only (no reconstruction)
    -n	project name (default: "${project_name}")
    -q  queue name (default: "${queue_name}")

EOF
}

simulate_tree_only='';

while getopts "n:p:c:q:sh" OPTION
do
    case $OPTION in
        n) project_name=$OPTARG ;;
        p) path_project=$OPTARG ;;
        c) config_file=$OPTARG ;;
        q) queue_name=$OPTARG ;;
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

# make a directory where SGE will place .stdout and .stderr
mkdir -p ${HOME}/s/${USER}/cluster-output

# set unique job name
job_name="job-`uuidgen`"

out=`qsub \
    -N ${job_name} \
    -q ${queue_name} \
    -cwd \
    ./sge-run-simul.sh ${path_project} ${config_file} ${simulate_tree_only}`

# extract SGE job ID from the qsub output
# e.g. Your job 7588748 ("simulation") has been submitted
job_id=`echo ${out} | awk -F' ' '{print $3}'`

echo ${job_id}


# record job info to a file
# fixme: hardcoded path
path_job_info="${HOME}/cluster_output/${project_name}.job-info"
echo "${job_id},${path_project},${config_file}" | tee -a ${path_job_info}
