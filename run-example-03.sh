#!/bin/bash

path_project='./examples/example-03'

python run_end_to_end.py \
  --env config.math102-lx.env \
  --project ${path_project} \
  --config config.list

python make_html_report.py \
  --project ${path_project} \
  --config config.list
