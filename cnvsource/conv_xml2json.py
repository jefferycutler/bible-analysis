######################################################
# conv_xml2json.py
#  Program to convert bible verse xml files to json
#   This takes the same input file as conv_xml2csv.
#

import argparse
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import json
import os.path
import xml.etree.ElementTree as ET

#############################################
## define our argument parser
parser = argparse.ArgumentParser(description=
  'Conversion script to convert bible verses xml file to json file')
parser.add_argument('--infile',help='input xml file path with bible verses',
                               default='bible.xml')
parser.add_argument('--outfile',help='output json file path', 
                                default='bible.json')
parser.add_argument('--gcpkey',help='path to GCP Service key',
                               required=True) 
parser.add_argument('--abbr',help='Translation Abbr code of book',
                             required=True) 
args = parser.parse_args()

#############################################
## verify the input file really exists
if not os.path.isfile(args.infile):
    print('!!!! PROBLEM - INPUT FILE NOT VALID !!!')
    exit(1)

#############################################
# Instantiates a GCP NL API client
client = language.LanguageServiceClient.from_service_account_json(args.gcpkey)

#############################################
## Open the file for our json output
f = open(args.outfile, "w", encoding="utf-8")

#############################################
## parse the input xml file
tree=ET.parse(args.infile)
root=tree.getroot()
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
        # get the sentiment analysis
        document = types.Document(content=child.text,
                     type=enums.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(document=document).document_sentiment

        # now get the entity analysis
        document = types.Document(content=child.text,
                     type=enums.Document.Type.PLAIN_TEXT)
        response = client.analyze_entities(document=document)
        entitylist=[]
        for entity in response.entities:
            entitylist.append({'ename' : entity.name,
                               'etype' : enums.Entity.Type(entity.type).name,
                               'salience' : entity.salience,
                               'wiki_url' : entity.metadata['wikipedia_url'] })

        record={'trns_abbr': args.abbr,
                'book': child.attrib['b'],
                'chapter': child.attrib['b'], 
                'verse': int(child.attrib['v'].split('-')[0]), 
                'vtext': child.text,
                'sentiment_magnitude': sentiment.score,
                'sentiment_score': sentiment.magnitude,
                'entity': entitylist }
        json.dump(record,f)
        f.write('\r\n')

## Be polite and close files
f.close()


