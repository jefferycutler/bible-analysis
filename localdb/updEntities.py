############################################################################
# updEntities.py
#  Find verses in DB that we have not gotten Entitity anlayis for yet 
#  and use GCP API to get entity analysis
#
#  You will need to provide a config file that contains
#    your mysql db connection info as well as some GCP settings
############################################################################

import argparse
import configparser 
from datetime import datetime
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import mysql.connector
import os.path

############################################
## get our config details, db config etc
parser = argparse.ArgumentParser(description=
        'INI file containing config for bible-analyis programs')
parser.add_argument('--cfg',help='input config ini file',
                             default='bible-analysis.ini')
args = parser.parse_args()

# make sure we can read a config file
if os.path.isfile(args.cfg):
    config=configparser.ConfigParser()
    config.read(args.cfg)
else:
    print(f'*** ERROR: Something went wrong reading the config file {args.cfg}')
    print( '*** ERROR: Do you use the --cfg parameter properly ')
    exit(1)

# get the number of times to call the api with a default of 3 times
apicalls=config.getint('gcp','api_ent_calls',fallback=3)

#############################################
# Instantiates a GCP NL API client
client = language.LanguageServiceClient.from_service_account_json(
              config['gcp']['servicekey'] )

#############################################
## setup our mysql connection
db=mysql.connector.connect(host=config['mysql']['host'],
                             user=config['mysql']['user'],
                             password=config['mysql']['password'],
                             database=config['mysql']['database'],
                             autocommit=True )
cursor=db.cursor()        

fetchsql=f"select * from bible_verse_no_entity limit {apicalls} ;"
savesql= \
  "insert into bible_verse_entity values (%s,%s,%s,%s,%s,%s,%s,%s,%s );"

rcursor=db.cursor(buffered=True) ## our read cursor
wcursor=db.cursor()              ## our write cursor     

#############################################
## For every record returned, get entity info and save
rcursor.execute(fetchsql,)
for row in rcursor:
    # first get the sentiment analysis from GCP NL API
    print('*********************')
    print(f"Entity for book {row[1]} chapter {row[2]} verse {row[3]}")
    document = types.Document(content=row[4],
                   type=language.enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document=document)
    
    # for every entity found save a record to the DB
    for entity in response.entities:
        print('****')
        print('    name:{0}'.format(entity.name) )
        print('    type:{0}'.format(enums.Entity.Type(entity.type).name) )
        print('salience:{0}'.format(entity.salience) )
        print('wiki URL:{0}'.format(entity.metadata['wikipedia_url']) )

        ## now save that to mysql
        payload=(row[0],row[1],row[2],row[3],datetime.now(),entity.name,
            enums.Entity.Type(entity.type).name, entity.salience,
             entity.metadata['wikipedia_url'] )
        wcursor.execute(savesql,payload)

# Be polite close your cursors and connections
rcursor.close()
wcursor.close()
db.close()

