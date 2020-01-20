Inter promotion project of 2020
Passenger voice
Group 3 : Dashboard

Production README
======================================================================

Contents Of This Release
------------------------
Latest version of the dashboard linked to an oracle database.


Github Files
------------
g3_script_creation_tables_mysql.sql 
	-> creation of the original database tables with mysql dbms
g3_script_insertion_bd_mysql.ipynb
	-> data insertion into mysql original database tables
g3_creation_table_qualite_bd_oracle_sql.sql
	-> creation of the original database tables with oracle dbms
g3_creation_table_qualite_tfidf.sql
	-> creation of the tfidf tables with oracle dbms
g3_creation_table_qualite_user.sql
	-> creation of the user actions tables with oracle dbms
g3_insertion_bd_tfidf.ipynb
	-> data insertion into oracle tfidf tables
g3_script_insertion_bd_oracle.ipynb
	-> data insertion into oracle original database tables
LAYOUT SEATGURU file
	-> contains aircraft plans
data_aircraft.json
	-> contains data about aircraft plans
version3_1.py
	-> main script to execute
Find_Areas.py
	-> script containing functions for aircraft plans
resultat.png
	-> image for the wordcloud



Installation
------------
Before continuing you need to execute the following commands
to download the associated python modules:
	- pip install base64
	- pip install WordCloud
	- pip install cx_Oracle
	- pip install dash


Important Notes
---------------
You have to run this release in the terminal, using the "python version3_1.py" command
in the directory this file is in.
Then, open a browser and go to "localhost:8050".
If you want to execute the script on another server, you have to change the connection parameters in version3_1.py 


