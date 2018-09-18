#!/bin/bash

path_project='./examples/example-02b'

python simulator.py \
  --env config.math102-lx.env \
  --project ${path_project} \
  --config config.list

python make_html_report.py \
  --title example-02b \
  --project ${path_project} \
  --config config.list \
  --exclude-mutation-table

