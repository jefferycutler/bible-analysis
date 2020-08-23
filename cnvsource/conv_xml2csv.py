######################################################
# conv_xml2csv.py
#  Program to convert bible verse xml files to csv
#   Source xml should be contain a structure like this
#      <verseFile>
#        <v b=book c=chapter# v=verse#>verse text</v>
#

import argparse
import csv 
import os.path
import xml.etree.ElementTree as ET

#############################################
## define our argument parser
parser = argparse.ArgumentParser(description=
  'Conversion script to convert bible verses xml file to csv')
parser.add_argument('--infile',help='input xml file path with bible verses',
                               required=True)
parser.add_argument('--outfile',help='output csv file path', required=True)
args = parser.parse_args()

#############################################
## verify the input file really exists
if not os.path.isfile(args.infile):
    print('!!!! PROBLEM - INPUT FILE NOT VALID !!!')
    exit(1)

#############################################
## parse the input xml file
tree=ET.parse(args.infile)
root=tree.getroot()

## prepare our output csv file
csvfile=open(args.outfile,'w')
csvfields=['book','chapter','verse','text']
csvwriter=csv.DictWriter(csvfile,fieldnames=csvfields,
                                 quoting=csv.QUOTE_NONNUMERIC)
csvwriter.writeheader()

## for every verse in the file
print(f'Parsing input {args.infile} to {args.outfile}')
for child in root:
    
    csvwriter.writerow({'book': child.attrib['b'],
                        'chapter': int(child.attrib['c']),
                        'verse': int(child.attrib['v']),
                        'text': child.text })

# be polite and close file 
csvfile.close()
print('All done, have a nice day!')
