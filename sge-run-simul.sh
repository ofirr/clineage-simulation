#!/bin/bash

#$ -S /bin/bash
#$ -o $HOME/s/$USER/cluster-output/$JOB_ID.stdout
#$ -e $HOME/s/$USER/cluster-output/$JOB_ID.stderr

ulimit -c 10

# activate conda cl environment
source "${HOME}/miniconda3/bin/activate" cl

# owner/group: rwx, others: none
umask 007

path_project=$1
config_json_file=$2
run_flag=$3

# write SGE job info to a file
cat << EOF >> ${path_project}/sge-job-info.txt
$JOB_ID
EOF

# run simulation
python ./simulator.py \
  --env ./config.math102-lx.env \
  --project ${path_project} \
  --config ${config_json_file} \
  --run-flag ${run_flag}

# copy stdout and stderr to project directory
cp $HOME/s/$USER/cluster-output/$JOB_ID.stdout ${path_project}
cp $HOME/s/$USER/cluster-output/$JOB_ID.stderr ${path_project}

echo "DONE."
