#!/bin/bash

usage()
{
cat << EOF
USAGE: `basename $0` [options]

    -p    project directory
    -s    seed
    -o    output base directory

EOF
}

while getopts "p:s:o:h" OPTION
do
    case $OPTION in
        p) path_project=$OPTARG ;;
        s) seed=$OPTARG ;;
        o) path_output_base=$OPTARG ;;
        h) usage; exit 1 ;;
        *) usage; exit 1 ;;
    esac
done

if [ -z "$path_project" ] || [ -z "$seed" ] || [ -z "$path_output_base" ]
then
    usage
    exit 1
fi

for nn in {3..13}
do

    for ii in {1..20}
    do

      	num=`printf "%02d\n" $ii`

        python ../compare_nj_scipylnk.py \
            --project ${path_project} \
            --seed ${seed} \
            --n ${nn} \
            --case ${ii} \
            --outdir ${path_output_base}

    done

done

