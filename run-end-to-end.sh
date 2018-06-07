#!/bin/bash

# run simulation
./simulate.sh

# reconstruct tree using mutation table
python reconstruct.py

# compare reconstructed tree against simulation tree
./compare.sh
