/* 
Script for creating all tables of the database 
Creation of tables : DOCUMENT, APPEAR, WORD
*/

-- Drop tables before creation 
DROP TABLE APPEAR;
DROP TABLE WORD;
DROP TABLE DOCUMENT;

-- Drop sequences before creation 
DROP SEQUENCE SEQ_DOCUMENT;
DROP SEQUENCE SEQ_WORD;


-- Creation of table :  DOCUMENT 
CREATE TABLE DOCUMENT (
  id_doc INT,
  ATMOSPHERE INT,
  BAGGAGE INT,
  CABIN_CREW INT,
  COMFORT INT,
  EMPTY INT,
  FOOD INT,
  NOT_FLIGHT INT,
  PRICE INT,
  PUNCTUALITY INT,
  CONSTRAINT pk_document PRIMARY KEY (id_doc)
);
   
-- Creation of table :  WORD 
CREATE TABLE WORD (
  id_word INT ,
  word VARCHAR(50),
  CONSTRAINT pk_word PRIMARY KEY (id_word)
);
  
-- Creation of table :  APPEAR
CREATE TABLE APPEAR (
	id_doc INT,
	id_word INT,
	tfidf FLOAT,
	CONSTRAINT pk_appear PRIMARY KEY (id_doc,id_word),
	CONSTRAINT fk_id_doc
        FOREIGN KEY (id_doc)
        REFERENCES DOCUMENT (id_doc),
	CONSTRAINT fk_id_word
        FOREIGN KEY (id_word)
        REFERENCES Word (id_word));

-- Creation sequences
CREATE SEQUENCE SEQ_DOCUMENT START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_WORD START WITH 1 INCREMENT BY 1;


Commit;