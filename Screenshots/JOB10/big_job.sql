-- Créer la base de données
CREATE DATABASE IF NOT EXISTS CarbonFootprint;
USE CarbonFootprint;

-- Table Country : données par pays
CREATE TABLE IF NOT EXISTS Country (
    country    VARCHAR(100) PRIMARY KEY,
    coal       DECIMAL(5,2),
    gas        DECIMAL(5,2),
    oil        DECIMAL(5,2),
    hydro      DECIMAL(5,2),
    renewable  DECIMAL(5,2),
    nuclear    DECIMAL(5,2)
);

-- Table World : données par région du monde
CREATE TABLE IF NOT EXISTS World (
    region     VARCHAR(100) PRIMARY KEY,
    coal       DECIMAL(5,2),
    gas        DECIMAL(5,2),
    oil        DECIMAL(5,2),
    hydro      DECIMAL(5,2),
    renewable  DECIMAL(5,2),
    nuclear    DECIMAL(5,2)
);

SELECT
  c.country,
  (c.coal      * 820 +
   c.gas       * 490 +
   c.oil       * 740 +
   c.hydro     *  24 +
   c.renewable *  41 +
   c.nuclear   *  12) AS total_gco2_kwh
FROM Country c
ORDER BY total_gco2_kwh DESC;
