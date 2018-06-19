#!/bin/bash

seeds="875887 431414 910648 181848 263803 145539 136069 869293 579705 549861"

for seed in ${seeds}
do
    python generate.py --seed ${seed}
done
