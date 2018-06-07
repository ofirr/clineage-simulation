#!/bin/bash

treecmp="./TreeCmp/bin/treeCmp.jar"

#  Metrics for rooted trees
metrics_r="mc rc ns tt mp mt co"

# metrics for unrooted trees
metrics_ur="ms rf pd qt um"

# execute TreeCmp
java -jar ${treecmp} \
  -r ./outputs/simulation.newick \
  -d ${metrics_r} \
  -i ./outputs/reconstructed.newick \
  -o ./outputs/scores.out \
  -P -N -I
