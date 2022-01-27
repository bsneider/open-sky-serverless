CREATE TABLE IF NOT EXISTS flightlist(
   callsign     VARCHAR(7) NOT NULL PRIMARY KEY
  ,number       VARCHAR(30)
  ,icao24       VARCHAR(6) NOT NULL
  ,registration VARCHAR(7)
  ,typecode     VARCHAR(4)
  ,origin       VARCHAR(4)
  ,destination  VARCHAR(4) NOT NULL
  ,firstseen    VARCHAR(25) NOT NULL
  ,lastseen     VARCHAR(25) NOT NULL
  ,day          VARCHAR(25) NOT NULL
  ,latitude_1   VARCHAR(19) 
  ,longitude_1  VARCHAR(19) 
  ,altitude_1   NUMERIC(7,1) 
  ,latitude_2   VARCHAR(18) 
  ,longitude_2  VARCHAR(19) 
  ,altitude_2   VARCHAR(17)
);