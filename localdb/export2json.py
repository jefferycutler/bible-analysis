############################################################################
# export2json.py
#   Export the MySQL database of bible verses and the associated sentiment
#    and entity analysis.  The export output is in JSON format.
#    The JSON output matches what is needed to import to GCP BiqQuery
############################################################################
import argparse
import configparser 
import json
import mysql.connector
import os.path 

############################################
## get our config details, db config etc
parser = argparse.ArgumentParser(description="""
  This program exports the bible verse tables in a MySQL DB
  to a JSON file that can be loaded into GCP BigQuery
  It requires the config file that contains MySQL connection info 
  and assumes the json structure described in the bq_schema.json file
  in the bigquery folder of this project. 
  The program assumes you have generated the sentiment and entity
  analysis and saved it to the MySQL tables.
  """)
parser.add_argument('--cfg',help='input config ini file with DB info',
                             default='bible-analysis.ini')
parser.add_argument('--outfile',help='The output json file to save records to',
                             default='bible-verses.json')
args = parser.parse_args()

# make sure we can read a config file
if os.path.isfile(args.cfg):
    config=configparser.ConfigParser()
    config.read(args.cfg)
else:
    print(f'*** ERROR: Something went wrong reading the config file {args.cfg}')
    print( '*** ERROR: Did you use the --cfg parameter properly ')
    exit(1)


# make sure we can read a config file
if os.path.isfile(args.cfg):
    config=configparser.ConfigParser()
    config.read(args.cfg)
else:
    print(f'*** ERROR: Something went wrong reading the config file {args.cfg}')
    print( '*** ERROR: Do you use the --cfg parameter properly ')
    exit(1)

#############################################
## Setup our connection to MySQL
db=mysql.connector.connect(host=config['mysql']['host'],
                             user=config['mysql']['user'],
                             password=config['mysql']['password'],
                             database=config['mysql']['database'] )

cursor=db.cursor()        
# First query gets the verse and sentiment
sqlquery1=""" SELECT a.trns_abbr as translation
                , a.book as book_id
                , b.long_Name as book
                , a.chapter
                , a.verse
                , a.vtext
                , c.sentiment_magnitude as sentiment_magnitude	
                , c.sentiment_score as sentiment_score
           FROM bible_verse a
             left join bible_book_names b
               on (a.book=b.short_name)
             left join bible_verse_sentiment c
               on (a.trns_abbr=c.trns_abbr
                    and a.book=c.book
                    and a.chapter=c.chapter
                    and a.verse=c.verse ) """
# Second query is because there are multiple enitites records per verse
sqlquery2=""" SELECT entity_name
                    ,entity_type
                    ,entity_salience
                    ,entity_wiki_url
                FROM bible_verse_entity 
               where trns_abbr=%s
                 and book=%s
                 and chapter=%s
                 and verse=%s """

cursor1=db.cursor(buffered=True) # for reading verses
cursor2=db.cursor(buffered=True) # for reading entities

#############################################
## Open the file for our json output
f = open(args.outfile, "w", encoding="utf-8")

#############################################
## Find all verses and export
cursor1.execute(sqlquery1,)
for row in cursor1:
    # now get the entities for that verse
    filter=(row[0],row[1],row[3],row[4])
    cursor2.execute(sqlquery2,filter)
    entitylist=[]
    for entity in cursor2:
        entitylist.append({'ename' : entity[0],
                           'etype' : entity[1],
                           'salience' : entity[2],
                           'wiki_url' : entity[3] })

    # build the json record for output to file
    record={'translation': row[0],
            'book': row[2],
            'chapter': row[3], 
            'verse': row[4], 
            'vtext': row[5],
            'sentiment_magnitude': row[6],
            'sentiment_score': row[7],
            'entity': entitylist }
    json.dump(record,f)
    f.write('\r\n')

## Be polite and close files
cursor1.close()
cursor2.close()
f.close()

