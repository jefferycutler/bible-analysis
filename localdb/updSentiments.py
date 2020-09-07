######################################################
# updSentiments.py
#  Find verses in DB that we have not gotten 
#  sentiment anlayis for yet and use GCP API 
#  to get sentiment and magnitute
######################################################

import argparse
import configparser 
from datetime import datetime
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import mysql.connector

############################################
## get our config details, db config etc
parser = argparse.ArgumentParser(description=
        'INI file containing config for bible-analyis programs')
parser.add_argument('--cfg',help='input config ini file',
                             default='bible-analysis.ini')
args = parser.parse_args()

config=configparser.ConfigParser()
config.read(args.cfg)

# get the number of times to call the api with a default of 3 times
apicalls=config.getint('gcp','api_sen_calls',fallback=3)

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

fetchsql=f"select * from bible_verse_no_sentiment limit {apicalls} ;"
savesql= \
    "insert into bible_verse_sentiment values ( %s, %s, %s, %s, %s, %s, %s );"

rcursor=db.cursor(buffered=True) ## our read cursor
wcursor=db.cursor() ## our write cursor     

#############################################
## For every record returned, get sentiment and save
rcursor.execute(fetchsql,)
for row in rcursor:
    # first get the sentiment analysis from GCP NL API
    print('*********************')
    print(f"Sentiment for book {row[1]} chapter {row[2]} verse {row[3]}")
    document = types.Document(content=row[4],
                   type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

    ## now save that to mysql
    payload=(row[0],row[1],row[2],row[3],datetime.now(),
             sentiment.magnitude,sentiment.score)
    wcursor.execute(savesql,payload)


# Be polite close your cursors and connections
rcursor.close()
wcursor.close()
db.close()

