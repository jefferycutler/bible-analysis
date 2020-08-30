---------------------------------------------------------------
-- This script creates the tables needed for the 
--  bible analysis on a local DB 

----------------------------------------------
-- The core table that holds all verses
CREATE TABLE `bible_verse` (
  `trns_abbr` varchar(20) NOT NULL,
  `book` varchar(20) NOT NULL,
  `chapter` int NOT NULL,
  `verse` int NOT NULL,
  `vtext` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`trns_abbr`,`book`,`chapter`,`verse`)
) ;

----------------------------------------------
-- For Entity Analysis
CREATE TABLE bible_verse_sentiment (   
    trns_abbr varchar(20) NOT NULL,   
    book varchar(20) NOT NULL,   
    chapter int NOT NULL,   
    verse int NOT NULL,   
    vtext varchar(2000) DEFAULT NULL,   
    sentiment_dt datetime not null,   
    sentiment_magnitude decimal(5,3),   
    sentiment_score decimal(5,3),  
    PRIMARY KEY (trns_abbr,book,chapter,verse,sentiment_dt) 
) ;

----------------------------------------------
-- For sentiment anlaysis
CREATE TABLE bible_verse_entity (
  trns_abbr varchar(20) NOT NULL,
  book varchar(20) NOT NULL,
  chapter int NOT NULL,
  verse int NOT NULL,
  vtext varchar(2000) DEFAULT NULL,
  entity_dt datetime not null,
  entity_name varchar(100),
  entity_type varchar(100),
  entity_salience float, 
  PRIMARY KEY (trns_abbr,book,chapter,verse,entity_dt)
) ;