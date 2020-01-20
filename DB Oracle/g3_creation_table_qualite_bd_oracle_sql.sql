/*
Script for creating all tables of the database 
Creation of tables : AIRLINE, DATE, SEAT, PASSENGER, SERVICE, ROUTE, REVIEW and NOTES
*/

-- Drop tables before creation 
DROP TABLE NOTES;
DROP TABLE REVIEW;
DROP TABLE ROUTE;
DROP TABLE SERVICE;
DROP TABLE PASSENGER;
DROP TABLE SEAT;
DROP TABLE DATES;
DROP TABLE AIRLINE;

-- Drop sequences before creation 
DROP SEQUENCE SEQ_NOTES;
DROP SEQUENCE SEQ_ROUTE;
DROP SEQUENCE SEQ_SERVICE;
DROP SEQUENCE SEQ_PASSENGER;
DROP SEQUENCE SEQ_REVIEW;
DROP SEQUENCE SEQ_SEAT;


-- Creation of table :  AIRLINE 
CREATE TABLE AIRLINE (
  airline_name VARCHAR(100) CONSTRAINT pk_airlinename PRIMARY KEY,
  boarding FLOAT,
  cabin_staff_service FLOAT,
  comfort FLOAT,
  entertainment FLOAT,
  food_and_beverages FLOAT,
  overall_airline_rating FLOAT,
  mention VARCHAR(10),
  number_evaluation INT
);

-- Creation of table :  DATE
CREATE TABLE DATES (
  id_date VARCHAR(8) CONSTRAINT pk_date PRIMARY KEY,
  day VARCHAR(2),
  month VARCHAR(2),
  year VARCHAR(4)
);

-- Creation of table :  SEAT
CREATE TABLE SEAT (
  id_seat INT CONSTRAINT pk_seat PRIMARY KEY,
  airline_name VARCHAR(100),
  manufacturer_name VARCHAR(40),
  aircraft_type VARCHAR(80),
  category VARCHAR(10),
  seat_type VARCHAR(15),
  seat_position VARCHAR(10),
  flight_type VARCHAR(10),
  count INT,
  total_seat INT,
  recline VARCHAR(23),
  premium VARCHAR(1),
  pitch_min FLOAT,
  pitch_max FLOAT,
  width FLOAT,
  bedlength_max FLOAT,
  bedlength_min FLOAT,
  music VARCHAR(17),
  video_type VARCHAR(10),
  power_available VARCHAR(6),
  power_kind VARCHAR(2),
  usb_available VARCHAR(6),
  usb_kind VARCHAR(10)
);

-- Creation of table :  PASSENGER
CREATE TABLE PASSENGER (
  id_passenger INT CONSTRAINT pk_passenger PRIMARY KEY,
  type_of_lounge VARCHAR(30),
  type_of_traveller VARCHAR(30)
);

-- Creation of table :  SERVICE
CREATE TABLE SERVICE (
  id_service INT CONSTRAINT pk_service PRIMARY KEY,
  type_service VARCHAR(60),
  desc_service VARCHAR(60)
);

-- Creation of table :  ROUTE
CREATE TABLE ROUTE (
  id_route INT CONSTRAINT pk_route PRIMARY KEY,
  origine VARCHAR(150),
  destination VARCHAR(150),
  via VARCHAR(150)
);

-- Creation of table :  REVIEW
CREATE TABLE REVIEW (
  id_review INT CONSTRAINT pk_review PRIMARY KEY,
  comments CLOB,
  label_seat INT,
  label_bed INT,
  label_ife INT,
  label_food INT,
  label_noise INT,
  label_temperature INT,
  label_humidity INT,
  label_cabin_crew INT,
  label_lavatory_space INT,
  label_price INT,
  label_lost_bagage INT,
  label_check_in INT,
  label_ponctuality INT,
  label_attract_aircraft INT,
  label_sav INT,
  label_boarding INT,
  label_general INT
);

-- Creation of table :  NOTES
CREATE TABLE NOTES (
  id_notes INT,
  airline_name VARCHAR(100),
  id_route INT,
  id_seat INT,
  date_visit VARCHAR(8),
  date_flown VARCHAR(8),
  --date_review VARCHAR(8),
  -- id_review INT,
  id_passenger INT,
  id_service INT,
  cabin_staff_service INT,
  lounge_staff_service INT,
  bar_and_beverages INT,
  food_and_beverages INT,
  ground_service INT,
  catering INT,
  cleanliness INT,
  lounge_comfort INT,
  aisle_space INT,
  wifi_and_connectivity INT,
  inflight_entertainment INT,
  viewing_tv_screen INT,
  power_supply INT,
  seat_comfort INT,
  seat_legroom INT,
  seat_storage INT,
  seat_recline INT,
  seat_width INT,
  washrooms INT,
  value_for_money INT,
  overall_customer_rating INT,
  overall_service_rating INT,
  overall_airline_rating INT,
  recommended VARCHAR(45),
  CONSTRAINT pk_notes PRIMARY KEY (id_notes),
  CONSTRAINT fk_airline_name
    FOREIGN KEY (airline_name)
    REFERENCES AIRLINE (airline_name),
  CONSTRAINT fk_route
    FOREIGN KEY (id_route)
    REFERENCES ROUTE (id_route),
  CONSTRAINT fk_seat
    FOREIGN KEY (id_seat)
    REFERENCES SEAT (id_seat),
  CONSTRAINT fk_date_visit
    FOREIGN KEY (date_visit)
    REFERENCES DATES (id_date),
  CONSTRAINT fk_date_flown
    FOREIGN KEY (date_flown)
    REFERENCES DATES (id_date),
  --CONSTRAINT fk_date_review
    --FOREIGN KEY (date_review)
    --REFERENCES DATES (id_date),
  --CONSTRAINT fk_review
    --FOREIGN KEY (id_review)
    --REFERENCES REVIEW (id_review),
  CONSTRAINT fk_passenger
    FOREIGN KEY (id_passenger)
    REFERENCES PASSENGER (id_passenger),
  CONSTRAINT fk_service
    FOREIGN KEY (id_service)
    REFERENCES SERVICE (id_service)
);

-- Creation sequences
CREATE SEQUENCE SEQ_ROUTE START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_SERVICE START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_PASSENGER START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_REVIEW START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_SEAT START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_NOTES START WITH 1 INCREMENT BY 1;


