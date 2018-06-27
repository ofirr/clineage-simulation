#!/bin/bash

usage()
{
cat << EOF
USAGE: `basename $0` [options]

    -r    root directory
    -o    output base directory

EOF
}

while getopts "r:o:h" OPTION
do
    case $OPTION in
        r) path_root=$OPTARG ;;
        o) path_output_base=$OPTARG ;;
        h) usage; exit 1 ;;
        *) usage; exit 1 ;;
    esac
done

if [ -z "$path_root" ] || [ -z "$path_output_base" ]
then
    usage
    exit 1
fi

seeds=`find ${path_root} -name "seed-*" -type d`

for path_project in $seeds
do

    seed=`echo ${path_project} | awk -F'/' '{print $(NF)}' | cut -c6-`

    echo ${path_project}

    for ii in {1..5}
    do

        python ../compare_nj_scipylnk.py \
            --project ${path_project} \
            --seed ${seed} \
            --case ${ii} \
            --outdir ${path_output_base}

    done

done
