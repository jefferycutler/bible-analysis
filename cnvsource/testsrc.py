######################################################
# conv_xml2csv.py
#  Program to convert bible verse xml files to csv
#   Source xml should be contain a structure like this
#      <verseFile>
#        <v b=book c=chapter# v=verse#>verse text</v>
#

import csv 
import os.path
import xml.etree.ElementTree as ET

inputfile='/home/jeffc/dev/bible-analysis/cnvsource/rawdata/eng-rv_vpl.xml'

#############################################
## parse the input xml file
tree=ET.parse(inputfile)
root=tree.getroot()

## for every verse in the file
for child in root:
    #print(child.attrib['v'])
    if not child.text:
        print('********************')
        print("Book:",child.attrib['b'])
        print("Chapter:",child.attrib['c'])
        print("Verse",child.attrib['v'])
        

    # csvwriter.writerow({'book': child.attrib['b'],
    #                     'chapter': int(child.attrib['c']),
    #                     'verse': int(child.attrib['v']),
    #                     'text': child.text })

