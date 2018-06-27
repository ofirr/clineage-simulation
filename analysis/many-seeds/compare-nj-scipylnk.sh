#!/bin/bash

usage()
{
cat << EOF
USAGE: `basename $0` [options]

    -p    project directory
    -o    output base directory

EOF
}

while getopts "p:o:h" OPTION
do
    case $OPTION in
        p) path_project=$OPTARG ;;
        o) path_output_base=$OPTARG ;;
        h) usage; exit 1 ;;
        *) usage; exit 1 ;;
    esac
done

if [ -z "$path_project" ] || [ -z "$path_output_base" ]
then
    usage
    exit 1
fi

seeds=`find ${path_project} -name "seed-*" -type d`

for seed_dir in $seeds
do

    seed=`echo ${seed_dir} | awk -F'/' '{print $(NF)}' | cut -c6-`

    echo ${seed_dir}

    for ii in {1..5}
    do

        python ../compare_nj_scipylnk.py \
            --project ${path_project} \
            --seed ${seed} \
            --case ${ii} \
            --outdir ${path_output_base}

    done

done
