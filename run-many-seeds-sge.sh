#!/bin/bash

if [ ! -x "$(command -v qsub)" ]
then
    echo "qsub not found. Aborted."
    exit 1
fi

# run everything (tree simulation, genotyping, reconstruction)
run_flag='0 0 0';

usage()
{
cat << EOF
USAGE: `basename $0` [options]

    -r  absolute path to simulation root where seed-* are placed
    -f  run flag (default: "${run_flag}")

EOF
}

while getopts "r:f:h" OPTION
do
    case $OPTION in
        r) path_root=$OPTARG ;;
        f) run_flag=$OPTARG ;;
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

project_name=$(uuidgen)

echo ">>> Project Name: ${project_name}"

for path_project in $seeds
do

    cases=`cat ${path_project}/config.list`

    for case in $cases
    do
        echo "${path_project}/${case}"
        ./sge-submit.sh \
            -n ${project_name} \
            -p ${path_project} \
            -c ${case} \
            -f "${run_flag}"
    done

done

echo "<<< Project Name: ${project_name}"
