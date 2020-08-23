#!/bin/bash
#####################################################################
# Script to loop around each xml file in the rawdata folder
#  and convert to csv using the python script
#####################################################################
infldr=./rawdata
outfldr=./csvout

for infile in ${infldr}/*.xml; do
    outcsv="${outfldr}/$(basename $infile xml ).csv"
    python3 conv_xml2csv.py --infile ${infile} --outfile ${outcsv}
done
