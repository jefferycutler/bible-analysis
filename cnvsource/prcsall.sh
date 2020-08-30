#!/bin/bash
#####################################################################
# Script to loop around each xml file in the rawdata folder
#  and convert to csv using the python script
#####################################################################
infldr=./rawdata
outfldr=./csvout

for infile in ${infldr}/*.xml; do

    ## create the output file name
    outcsv="${outfldr}/$(basename $infile xml )csv"

    ## the translation abbreviation is part of the file name
    abbr=$(basename -- ${outcsv} | awk -F'[-_]' '{print $2}' )

    #echo "--infile ${infile} --outfile ${outcsv} --abbr ${abbr}" #debug line
    python3 conv_xml2csv.py --infile ${infile} --outfile ${outcsv} --abbr ${abbr}

done
