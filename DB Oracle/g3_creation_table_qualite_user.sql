/* 
Script for creating all tables of the database 
Creation of tables : USER_ACTION
*/

-- Drop table before creation 
DROP TABLE USER_ACTION;

-- Drop sequence before creation 
DROP SEQUENCE SEQ_SESSION;


-- Creation of table :  DOCUMENT 
CREATE TABLE USER_ACTION (
  id_session INT  CONSTRAINT pk_session PRIMARY KEY,
  action VARCHAR(1000),
  date_time DATE
  );
  
-- Creation sequence
CREATE SEQUENCE SEQ_SESSION START WITH 1 INCREMENT BY 1;
