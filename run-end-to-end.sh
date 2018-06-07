#!/bin/bash

# run simulation
./simulate.sh

# reconstruct tree using mutation table
python reconstruct.py

# compare reconstructed tree against simulation tree
./compare.sh

# reformat the output of tree comparison and display
python report.py
