#!/bin/bash

#$ -S /bin/bash
#$ -o $HOME/cluster_output/$JOB_ID.stdout
#$ -e $HOME/cluster_output/$JOB_ID.stderr

ulimit -c 10

source "/home/chun/miniconda3/bin/activate" cl

path_program=$1
path_project=$2
config_json_file=$3

# write SGE job info to a file
cat << EOF > ${path_project}/sge-job-info.txt
$JOB_ID
$HOME/cluster_output/$JOB_ID.stdout
$HOME/cluster_output/$JOB_ID.stderr
EOF

cd ${path_program}

# run simulation
python ./run_end_to_end.py \
  --env ./config.math102-lx.env \
  --project ${path_project} \
  --config ${config_json_file}

# copy stdout and stderr to project directory
cp $HOME/cluster_output/$JOB_ID.stdout ${path_project}
cp $HOME/cluster_output/$JOB_ID.stderr ${path_project}

echo "DONE."
