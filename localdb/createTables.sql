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
-- For sentiment anlaysis
CREATE TABLE bible_verse_sentiment (   
    trns_abbr varchar(20) NOT NULL,   
    book varchar(20) NOT NULL,   
    chapter int NOT NULL,   
    verse int NOT NULL,   
    api_call_dt datetime not null,   
    sentiment_magnitude double,   
    sentiment_score double,  
    PRIMARY KEY (trns_abbr,book,chapter,verse,api_call_dt) 
) ;

----------------------------------------------
-- For Entity Analysis
CREATE TABLE bible_verse_entity (
  trns_abbr varchar(20) NOT NULL,
  book varchar(20) NOT NULL,
  chapter int NOT NULL,
  verse int NOT NULL,
  api_call_dt datetime not null,
  entity_name varchar(100),
  entity_type varchar(100),
  entity_salience double, 
  PRIMARY KEY (trns_abbr,book,chapter,verse,api_call_dt)
) ;

----------------------------------------------
-- Views to show unmatched verses (no api calls)
create or replace view bible_verse_no_entity as
select bv.trns_abbr
      ,bv.book
      ,bv.chapter
      ,bv.verse
      ,bv.vtext
from bible_verse bv
  left join bible_verse_entity bve
    on (bv.trns_abbr = bve.trns_abbr 
        and bv.book = bve.book
        and bv.chapter = bve.chapter
        and bv.verse = bve.verse )
where bve.api_call_dt is null ;

create or replace view bible_verse_no_sentiment as
select bv.trns_abbr
      ,bv.book
      ,bv.chapter
      ,bv.verse
      ,bv.vtext
from bible_verse bv
  left join bible_verse_sentiment bvs
    on (bv.trns_abbr = bvs.trns_abbr 
        and bv.book = bvs.book
        and bv.chapter = bvs.chapter
        and bv.verse = bvs.verse )
where bvs.api_call_dt is null
