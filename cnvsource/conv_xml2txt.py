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
  'Conversion script to convert bible verses xml file to | delimted files')
parser.add_argument('--infile',help='input xml file path with bible verses',
                               required=True)
parser.add_argument('--outfile',help='output delim file path', required=True)
parser.add_argument('--abbr',help='Translation Abbr code of book',
                             required=True)
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
csvfile=open(args.outfile,'w',encoding='utf-8',newline='\n')
csvfields=['trns_abbr','book','chapter','verse','vtext']
csvwriter=csv.DictWriter(csvfile,fieldnames=csvfields,delimiter='|',
                                 quoting=csv.QUOTE_MINIMAL)
csvwriter.writeheader()

trnsAbbr=args.abbr
## for every verse in the file
print(f'Parsing input {args.infile} to {args.outfile}')
for child in root:
    book=child.attrib['b']
    chapter=int(child.attrib['c'])
    # some verse #s are combined eg: 15-16, take the first int in the verse id
    verse=int(child.attrib['v'].split('-')[0])

    #only write out a record if there is verse text
    if child.text:
      csvwriter.writerow({'trns_abbr': trnsAbbr,
                          'book': book,
                          'chapter': chapter,
                          'verse': verse,
                          'vtext': child.text.strip() })

# be polite and close file 
csvfile.close()
print('All done, have a nice day!')
