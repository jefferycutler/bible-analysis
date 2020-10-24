#!/bin/bash

# create the bq table
bq mk -t organic-vortex-282322:bibleanalysis.bible_verses bq_schema.json