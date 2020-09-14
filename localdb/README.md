# Bible Analysis Local DB Version
This folder contains the local or "on prem" database version of the
bible analysis application.  The goal is to become familar the Google cloud
API's for Natural Language sentiment and entity analysis.  This application 
assumes english language for the source material.  I don't know how well the
sentiment and entity analysis works for non-enlish sources.  I am not sure I can get the source text for non-english versions.

### Requirements
* Python version 3.x
  * google-cloud-language Python libraries
* Google Developer or Cloud service account with NL API access.
* MySQL database
* Source files in delimited format

## Folder contents
File Name | Description
--------- | ------------
createTables.sql | SQL script create tables and views
loadVerses.py | Python script to load the verse text to bible_verse table.  This is run in the beginning to populate the main bible_verse table.
updEntities.py | Python script to call entity API on verse text.  This will call the GCP NL Entities API and save the results to the bible_verse_entity table.
updSentiments.py | Python script to call sentiment API on verse text.  This will call the GCP NL Sentitments API and save the results to the bible_verse_sentitment table.
bible-analysis.example | example config file for how the app will operate

## Database Design
### Tables

Table Name | Description
---------- | ------------
bible_verse | Contains the verse text from the source data.  The loadVerses.py program populates this table.  This is typically run in the beginning to populate the primary table.
bible_verse_entity | Contains the entity analysis for a verse.  This is a child table to the bible_verse table.  There can be more than one enitity record per parent record.
bible_verse_sentiment | Contains the sentiment analysis for a verse.  This is a child table to the bible_verse table.  Usually there is one record for each parent record.

The common index fields that link the tables.

**trns_abbr** - The abbreviated version of the bible.  KJV would be for the King James Bible.  It is possible to have multiple versions of the bible in the database, say the King James, Good News, and 

**book** - the abbreviated book, for example GEN for Genesis.

**chapter** - The chapter number, an integer

**verse** - The verse number, an integer

These fields are the primary key in the main bible_verse table.  Use these fields to join the primary bible_verse table to the sentiments and entities tables.

### Views
There are two views to facilitate the python API call programs.  

View Name | Description
---------- | ------------
bible_verse_no_entity | Verses that don't have entity records
bible_verse_no_sentiment | Verses that don't have sentiment analysis

When the updEntities.py and updSentiments.py programs run they will refer to these views to find new verses to get analysis for.  The programs were designed to run on small number of records periodically to lower costs.  GCP allows up to 5,000 API calls on the sentiment and entity analysis each before they charge.  If you only look at one version of the bible that would cost roughly $70 USD.  If you analyse 10 versions of the bible (there are more than 60 version) it would cost you $800 USD based on the GCP Pricing Calculator as September 2020.  I am cheap so I will try and stick to the free tier of 5000 API calls a month.









