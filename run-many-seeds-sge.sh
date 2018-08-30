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

    -r  path to simulation root where seed-* are placed
    -s  simulate tree only (no reconstruction)

EOF
}

simulate_tree_only='';

while getopts "r:sh" OPTION
do
    case $OPTION in
        r) path_root=$OPTARG ;;
        s) simulate_tree_only='-s' ;;
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
            -c ${case} ${simulate_tree_only}
    done

done

echo "<<< Project Name: ${project_name}"
