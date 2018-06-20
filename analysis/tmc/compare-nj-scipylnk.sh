#!/bin/bash

usage()
{
cat << EOF
USAGE: `basename $0` [options]

    -s    seed

EOF
}

while getopts "s:h" OPTION
do
    case $OPTION in
        s) seed=$OPTARG ;;
        h) usage; exit 1 ;;
        *) usage; exit 1 ;;
    esac
done

if [ -z "$seed" ]
then
    usage
    exit 1
fi

for nn in {3..14}
do

    path_project="/home/chun/projects/clineage-simulation/analysis/tmc/seed-${seed}/n-`printf '%03d' $nn`"

    echo ${path_project}

    for ii in {1..20}
    do

      	num=`printf "%02d\n" $ii`

        python ./scipylnk-nj-compare.py \
            --seed ${seed} \
            --n ${nn} \
            --case ${ii}

    done

done

