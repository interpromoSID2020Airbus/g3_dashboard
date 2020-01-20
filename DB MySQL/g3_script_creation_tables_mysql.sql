/* 
Script for creating all tables of the database 
Creation of tables : AIRLINE, DATE, SEAT, PASSENGER, SERVICE, ROUTE, REVIEW and NOTES
*/

-- Drop tables before creation 
DROP TABLE IF EXISTS `NOTES`;
DROP TABLE IF EXISTS `ROUTE`;
DROP TABLE IF EXISTS `SERVICE`;
DROP TABLE IF EXISTS `PASSENGER`;
DROP TABLE IF EXISTS `SEAT`;
DROP TABLE IF EXISTS `DATE`;
DROP TABLE IF EXISTS `AIRLINE`;

-- Creation of table :  AIRLINE 
CREATE TABLE IF NOT EXISTS `AIRLINE` (
  `airline_name` VARCHAR(100) NOT NULL,
  `boarding` DECIMAL(3,1) NULL CHECK (0 <= `boarding` <= 10),
  `cabin_staff_service` DECIMAL(3,1) NULL CHECK (0 <= `cabin_staff_service` <= 10),
  `comfort` DECIMAL(3,1) NULL CHECK (0 <= `comfort` <= 10),
  `entertainment` DECIMAL(3,1) NULL CHECK (0 <= `entertainment` <= 10),
  `food_and_beverages` DECIMAL(3,1) NULL CHECK (0 <= `food_and_beverages` <= 10),
  `overall_airline_rating` DECIMAL(3,1) NULL CHECK (0 <= `overall_airline_rating` <= 10),
  `mention` VARCHAR(10) NULL CHECK (`mention` IN ('Médiocre', 'Correct', 'Bien', 'Excellent')),
  `number_evaluation` INT NULL,
   CONSTRAINT `pk_airline` PRIMARY KEY (`airline_name`));

-- Creation of table :  DATE
CREATE TABLE IF NOT EXISTS `DATE` (
  `id_date` VARCHAR(8) NOT NULL,
  `day` VARCHAR(2) NULL,
  `month` VARCHAR(2) NULL,
  `year` VARCHAR(4) NULL,
  CONSTRAINT `pk_date` PRIMARY KEY (`id_date`));

-- Creation of table :  SEAT
CREATE TABLE IF NOT EXISTS `SEAT` (
  `id_seat` INT NOT NULL AUTO_INCREMENT,
  `airline_name` VARCHAR(100) NULL,
  `manufacturer_name` VARCHAR(40) NULL,
  `aircraft_type` VARCHAR(80) NULL,
  `category` VARCHAR(10) NULL,
  `seat_type` VARCHAR(15) NULL,
  `seat_position` VARCHAR(10) NULL,
  `flight_type` VARCHAR(10) NULL,
  `count` INT(3) NULL,
  `total_seat` INT(3) NULL,
  `recline` VARCHAR(23) NULL,
  `premium` VARCHAR(1) NULL,
  `pitch_min` FLOAT NULL,
  `pitch_max` FLOAT NULL,
  `width` FLOAT NULL,
  `bedlength_max` FLOAT NULL,
  `bedlength_min` FLOAT NULL,
  `music` VARCHAR(17) NULL,
  `video_type` VARCHAR(10) NULL,
  `power_available` VARCHAR(6) NULL,
  `power_kind` VARCHAR(2) NULL,
  `usb_available` VARCHAR(6) NULL,
  `usb_kind` VARCHAR(10) NULL,
  CONSTRAINT `pk_seat` PRIMARY KEY (`id_seat`));

-- Creation of table :  PASSENGER
CREATE TABLE IF NOT EXISTS `PASSENGER` (
  `id_passenger` INT NOT NULL AUTO_INCREMENT,
  `type_of_lounge` VARCHAR(30) NULL,
  `type_of_traveller` VARCHAR(30) NULL,
  CONSTRAINT `pk_passenger` PRIMARY KEY (`id_passenger`));

-- Creation of table :  SERVICE
CREATE TABLE IF NOT EXISTS `SERVICE` (
  `id_service` INT NOT NULL AUTO_INCREMENT,
  `type_service` VARCHAR(60) NULL,
  `desc_service` VARCHAR(60) NULL,
  CONSTRAINT `pk_service` PRIMARY KEY (`id_service`));

-- Creation of table :  ROUTE
CREATE TABLE IF NOT EXISTS `ROUTE` (
  `id_route` INT NOT NULL AUTO_INCREMENT,
  `origine` VARCHAR(80) NULL,
  `destination` VARCHAR(80) NULL,
  `via` VARCHAR(45) NULL,
  CONSTRAINT `pk_route` PRIMARY KEY (`id_route`));

-- Creation of table :  NOTES
CREATE TABLE IF NOT EXISTS `NOTES` (
  `id_notes` INT NOT NULL AUTO_INCREMENT,
  `#airline_name` VARCHAR(100) NULL,
  `#id_route` INT NULL,
  `#id_seat` INT NULL,
  `#date_visit` VARCHAR(8) NULL,
  `#date_flown` VARCHAR(8) NULL,
  `#id_passenger` INT NULL,
  `#id_service` INT NULL,
  `cabin_staff_service` DECIMAL(2,1) NULL,
  `lounge_staff_service` DECIMAL(2,1) NULL,
  `bar_and_beverages` DECIMAL(2,1) NULL,
  `food_and_beverages` DECIMAL(2,1) NULL,
  `ground_service` DECIMAL(2,1) NULL,
  `catering` DECIMAL(2,1) NULL,
  `cleanliness` DECIMAL(2,1) NULL,
  `lounge_comfort` DECIMAL(2,1) NULL,
  `aisle_space` DECIMAL(2,1) NULL,
  `wifi_and_connectivity` DECIMAL(2,1) NULL,
  `inflight_entertainment` DECIMAL(2,1) NULL,
  `viewing_tv_screen` DECIMAL(2,1) NULL,
  `power_supply` DECIMAL(2,1) NULL,
  `seat_comfort` DECIMAL(2,1) NULL,
  `seat_legroom` DECIMAL(2,1) NULL,
  `seat_storage` DECIMAL(2,1) NULL,
  `seat_recline` DECIMAL(2,1) NULL,
  `seat_width` DECIMAL(2,1) NULL,
  `washrooms` DECIMAL(2,1) NULL,
  `value_for_money` DECIMAL(2,1) NULL,
  `overall_customer_rating` INT(2) NULL,
  `overall_service_rating` DECIMAL(3,1) NULL,
  `overall_airline_rating` DECIMAL(2,1) NULL,
  `recommended` VARCHAR(5) NULL,
  CONSTRAINT `pk_notes` PRIMARY KEY (`id_notes`),
  CONSTRAINT `fk_airline_name`
    FOREIGN KEY (`#airline_name`)
    REFERENCES `AIRLINE` (`airline_name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_id_route`
    FOREIGN KEY (`#id_route`)
    REFERENCES `ROUTE` (`id_route`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_id_seat`
    FOREIGN KEY (`#id_seat`)
    REFERENCES `SEAT` (`id_seat`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_date_visit`
    FOREIGN KEY (`#date_visit`)
    REFERENCES `DATE` (`id_date`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_date_flown`
    FOREIGN KEY (`#date_flown`)
    REFERENCES `DATE` (`id_date`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_id_passenger`
    FOREIGN KEY (`#id_passenger`)
    REFERENCES `PASSENGER` (`id_passenger`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_id_service`
    FOREIGN KEY (`#id_service`)
    REFERENCES `SERVICE` (`id_service`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
