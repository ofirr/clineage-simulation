#!/bin/bash

if [ ! -x "$(command -v qsub)" ]
then
    echo "qsub not found. Aborted."
	exit 1
fi

path_project="/home/chun/projects/clineage-simulation/analysis/tmc-dev"

for i in {1..20}
do
    num=`printf "%02d\n" $i`
	./sge-submit.sh \
		-p ${path_project} \
		-c config-${num}.json
done
