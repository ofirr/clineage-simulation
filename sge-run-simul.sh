#!/bin/bash

#$ -S /bin/bash
#$ -o $HOME/cluster_output/$JOB_ID.stdout
#$ -e $HOME/cluster_output/$JOB_ID.stderr

ulimit -c 10

# fixme: hardcoded chun
source "/home/chun/miniconda3/bin/activate" cl

# owner/group: rwx, others: none
umask 007

path_project=$1
config_json_file=$2
simulate_tree_only=$3

# write SGE job info to a file
cat << EOF >> ${path_project}/sge-job-info.txt
$JOB_ID
EOF

# run simulation
python ./simulator.py \
  --env ./config.math102-lx.env \
  --project ${path_project} \
  --config ${config_json_file} \
  ${simulate_tree_only}

# copy stdout and stderr to project directory
cp $HOME/cluster_output/$JOB_ID.stdout ${path_project}
cp $HOME/cluster_output/$JOB_ID.stderr ${path_project}

echo "DONE."
