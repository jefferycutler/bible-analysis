######################################################
# loadVerses.py
#  Program to load all the verse files found in a folder
#    This will scan an input wildcard for all files
#    and try to bulk load them into a mysql database
######################################################

import argparse
import configparser 
import glob
import mysql.connector

#############################################
## get our config details, db config etc
parser = argparse.ArgumentParser(description=
        'pytnon Bulk loader to mysql to load bible verses')
parser.add_argument('--cfg',help='input config ini file',required=True)
args = parser.parse_args()

config=configparser.ConfigParser()
config.read(args.cfg)

## set some defaults if they don't exist
srcdelim=config.get('srcdata','delim',fallback='|')
srcenclose=config.get('srcdata','enclose',fallback='"')

#############################################
## setup our mysql connection
db=mysql.connector.connect(host=config['mysql']['host'],
                             user=config['mysql']['user'],
                             password=config['mysql']['password'],
                             database=config['mysql']['database'],
                             allow_local_infile=True,
                             autocommit=True )
cursor=db.cursor()        

loadsql="""load data local infile %s 
            into table bible_verse 
            fields terminated by %s optionally enclosed by %s 
            lines terminated by '\r\n'
            ignore 1 lines 
            (trns_abbr, book, chapter, verse, vtext ) ;"""


#############################################
## load each input file found
for file in glob.glob(config['srcdata']['inputmask']):
    print(f'** Loading file {file}')
    try:
        cursor.execute(loadsql,(file,srcdelim,srcenclose))
        
    except mysql.connector.Error as err:
        print('*** ERROR OCCURED LOADING FILE {}'.format(err))

cursor.close()
