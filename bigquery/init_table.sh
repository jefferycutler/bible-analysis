#!/bin/bash

GCP_PRJ="my_gcp_project"
GCP_DSET="bibleanalysis"
GCP_TBL="bible_verses"
INPUT_FILE="bibleverses.json"

# create the bq table
bq mk -t ${GCP_PRJ}:${GCP_DSET}.${GCP_TBL} bq_schema.json

bq load --source_format=NEWLINE_DELIMITED_JSON --replace ${GCP_PRJ}:${GCP_DSET}.${GCP_TBL} ${INPUT_FILE} bq_schema.json

