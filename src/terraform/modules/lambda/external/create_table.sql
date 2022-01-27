-- CREATE DATABASE IF NOT EXISTS flight;
-- USE flight;
CREATE TABLE IF NOT EXISTS flightlist(
  pk BIGINT NOT NULL AUTO_INCREMENT
  ,callsign     VARCHAR(30) NOT NULL
  ,number       VARCHAR(30)
  ,icao24       VARCHAR(6) NOT NULL
  ,registration VARCHAR(15)
  ,typecode     VARCHAR(10)
  ,origin       VARCHAR(8)
  ,destination  VARCHAR(15) NOT NULL
  ,firstseen    varchar(26) NOT NULL
  ,lastseen     varchar(26) NOT NULL
  ,day          varchar(26) NOT NULL
  ,latitude_1   VARCHAR(20) 
  ,longitude_1  VARCHAR(20) 
  ,altitude_1   VARCHAR(20) 
  ,latitude_2   VARCHAR(20) 
  ,longitude_2  VARCHAR(20) 
  ,altitude_2   VARCHAR(20)
  ,PRIMARY KEY (pk)
);

