#!/bin/bash

path_project='./examples/example-02'

python run_end_to_end.py \
  --env config.math102-lx.env \
  --project ${path_project} \
  --config config.json

python make_html_report.py \
  --title example-02 \
  --project ${path_project} \
  --config config.json

