# bible-analysis
Create dataset with all bible passages and perform NL analysis on each passage

##### Bible Sentiment and Entity Analysis

This project is to read into a database all the passages of the bible and
determine the sentiment and entities in each passage.  My goal is to become 
familar with Google Cloud tools such as ML Natural Lanugage 
API's, Datastore, and Bigquery.  I chose the bible because it's a book 
with a prebuilt indexing system, down to the sentences.  Some of them, like
the King James version are in the public domain.  

# Source Data and Conversion (\cnvsource)
My source for the text was in XML format.  Bulk loading is easier to various
data platforms if the file is in a delimted format.  This folder contains 
the python program I used to convert the XML files to delimited text files.  
MySQL was compaining a lot about the CSV format and some text characters.
I used a vertical bar as the delimiter and the problems went away.

# Local DB Version (\localdb)
This version uses a traditional RDBMS.  I used MySQL as it's easy, open source,
had good support in python and well documented.  I used the Google Natural 
Language sentiment and entity API's.  More details in the read me file in the 
folder.

# BiqQuery Verison (\bigquery)
Similar to the localdb version, this uses GCP's BigQuery as the data platform.
This is still a work in progress.  More information can be found in the read me
file in the folder.

# Datastore Version (\datastore)
Datatore is a NoSQL document database.  I chose this to expand my experience
with NoSQL data platforms.  This is still a work in progress.  More information
can be found in the read me file in the folder.

