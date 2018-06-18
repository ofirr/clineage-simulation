#!/bin/bash

for nn in {1..14}
do

  path_project="/home/chun/projects/clineage-simulation/analysis/tmc/tmc-`printf '%03d' $nn`"

  echo ${path_project}

  for ii in {1..20}
  do

    num=`printf "%02d\n" $ii`

    ./sge-submit.sh \
      -p ${path_project} \
      -c config-${num}.json

  done

done
