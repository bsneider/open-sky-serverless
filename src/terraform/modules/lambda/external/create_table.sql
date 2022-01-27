-- CREATE DATABASE IF NOT EXISTS flight;
-- USE flight;
CREATE TABLE IF NOT EXISTS flightlist(
  pk BIGINT NOT NULL AUTO_INCREMENT
  ,callsign     VARCHAR(30) NOT NULL
  ,number       VARCHAR(30)
  ,icao24       VARCHAR(6) NOT NULL
  ,registration VARCHAR(15)
  ,typecode     VARCHAR(20)
  ,origin       VARCHAR(8)
  ,destination  VARCHAR(15) NOT NULL
  ,firstseen    varchar(26) NOT NULL
  ,lastseen     varchar(26) NOT NULL
  ,day          varchar(26) NOT NULL
  ,latitude_1   VARCHAR(30) 
  ,longitude_1  VARCHAR(30) 
  ,altitude_1   VARCHAR(30) 
  ,latitude_2   VARCHAR(30) 
  ,longitude_2  VARCHAR(30) 
  ,altitude_2   VARCHAR(30)
  ,PRIMARY KEY (pk)
);

