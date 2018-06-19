#!/bin/bash

path_project="/home/chun/projects/clineage-simulation/analysis/tmc/seed-002/"

for i in {1..20}
do
    num=`printf "%02d\n" $i`
	./sge-submit.sh \
		-p ${path_project} \
		-c config-${num}.json
done
