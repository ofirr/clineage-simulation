#!/bin/bash

path_project='./examples/example-01'

python run_end_to_end.py \
  --env config.math102-lx.env \
  --project ${path_project}

python make_html_report.py \
  --project ${path_project}
