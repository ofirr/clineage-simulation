#!/bin/bash

path_project='./examples/example-02c'

python simulator.py \
  --env config.math102-lx.env \
  --project ${path_project} \
  --config config.json

python make_html_report.py \
  --title example-02c \
  --project ${path_project} \
  --config config.json

