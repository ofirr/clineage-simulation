#!/bin/bash

if [ ! -x "$(command -v qsub)" ]
then
    echo "qsub not found. Aborted."
	exit 1
fi

path_root='/home/chun/projects/clineage-simulation/analysis/many-seeds/'

seeds=`find ${path_root} -maxdepth 1 -name "seed-*" -type d`

nn="16 17 18 19 20"

for path_project in $seeds
do

    for n in ${nn}
    do
        echo ${path_project} ${n}

        ./sge-submit.sh \
            -p ${path_project} \
            -c config-${n}.json \
            -s
    done

done
