#!/bin/bash

./simulate.sh

python reconstruct.py

./compare.sh
