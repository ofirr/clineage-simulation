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

    -r  absolute path to simulation root where seed-* are placed
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

        while true
        do
            counter=`qstat -q 32g2.q | tail -n +3 | wc -l`
            if [ $counter -le 20 ] || [ $counter -eq 20 ]
            then
                break
            fi
            sleep 60
            echo "waiting until the queue frees up..."
        done

        echo "${path_project}/${case}"
        ./sge-submit.sh \
            -n ${project_name} \
            -p ${path_project} \
            -q 32g2.q \
            -c ${case} ${simulate_tree_only}

        # you need to wait until sge completes submission
        sleep 10

    done

done

echo "<<< Project Name: ${project_name}"
