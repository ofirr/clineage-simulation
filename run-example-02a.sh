#!/bin/bash

path_project='./examples/example-02a'

python run_end_to_end.py \
  --env config.math102-lx.env \
  --project ${path_project} \
  --config config.list

python make_html_report.py \
  --title example-02a \
  --project ${path_project} \
  --config config.list
