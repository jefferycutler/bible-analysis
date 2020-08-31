######################################################
# loadVerses.py
#  Program to load all the verse files found in a folder
#    This will scan an input wildcard for all files
#    and try to bulk load them into a mysql database
#    using a | delimted file.  
######################################################

import configparser 
import glob
import os.path

dbcfg='/home/jeffc/dev/bible-analysis/localdb/dbconn.ini'

#############################################
## get our config details, db config etc
config=configparser.ConfigParser()
config.read(dbcfg)

loadsql="""load data local infile '{}' 
            into table bible_verse 
            character set UTF8 
            fields terminated by '{}' optionally enclosed by '{}' 
            lines terminted by '\\n' ignore 1 lines 
            (trns_abbr, book, chapter, verse, vtext ) ;"""
        

#############################################
## load each input file found
for file in glob.glob(config['srcdata']['inputmask']):
    print('****************')
    print(loadsql.format(file,config['srcdata']['delim']
                             ,config['srcdata']['enclose']))

