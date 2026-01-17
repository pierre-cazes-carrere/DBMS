SHOW DATABASES;
USE DBMS;
SHOW TABLES;

SELECT Population FROM `countries of the world` WHERE TRIM(Country) IN ('Sweden', 'Norway', 'Denmark');
  
SELECT Country, `Area (sq. mi.)` FROM `countries of the world`
WHERE CAST(REPLACE(`Area (sq. mi.)`, ',', '') AS UNSIGNED) > 200000
  AND CAST(REPLACE(`Area (sq. mi.)`, ',', '') AS UNSIGNED) < 300000;

SELECT Country FROM `countries of the world`
WHERE TRIM(Country) LIKE 'B%';

SELECT Country FROM `countries of the world`
WHERE TRIM(Country) LIKE 'Al%';

SELECT Country FROM `countries of the world`
WHERE TRIM(Country) LIKE '%y';

SELECT Country FROM `countries of the world`
WHERE TRIM(Country) LIKE '%land';

SELECT Country FROM `countries of the world`
WHERE TRIM(Country) LIKE '%w%';

SELECT Country FROM `countries of the world`
WHERE TRIM(Country) LIKE '%oo%' OR TRIM(Country) LIKE '%ee%';

SELECT Country FROM `countries of the world`
WHERE (LENGTH(TRIM(Country)) - LENGTH(REPLACE(LOWER(TRIM(Country)), 'a', ''))) >= 3;

SELECT Country FROM `countries of the world`
WHERE TRIM(Country) LIKE '_r%';

SELECT Country, Population FROM `countries of the world`
WHERE Population > 142893540
ORDER BY Population DESC;

SELECT Country, `GDP ($ per capita)` FROM `countries of the world`
WHERE Region LIKE '%EUROPE%' 
  AND `GDP ($ per capita)` > 26700;

SELECT Country, Population FROM `countries of the world` 
WHERE TRIM(Country) IN ('United Kingdom', 'Germany');

SELECT Country, Population FROM `countries of the world`
WHERE Population > 60609153 AND Population < 82422299
ORDER BY Population DESC;

SELECT 
  Country, 
  Population, 
  ROUND((Population / 80000000) * 100, 2) AS Population_pourcentage_Allemagne
FROM `countries of the world`
WHERE Region LIKE '%EUROPE%'
ORDER BY Population DESC;

SELECT Region, Country, `Area (sq. mi.)`
FROM `countries of the world` AS c1
WHERE `Area (sq. mi.)` = (
    SELECT MAX(`Area (sq. mi.)`)
    FROM `countries of the world` AS c2
    WHERE c2.Region = c1.Region
);

SELECT Region
FROM `countries of the world`
GROUP BY Region
HAVING MAX(Population) <= 25000000;

SELECT SUM(Population) AS population_totale_monde
FROM `countries of the world`;

SELECT Region, SUM(Population) AS population_totale
FROM `countries of the world`
GROUP BY Region
ORDER BY population_totale DESC;

SELECT Region, SUM(`GDP ($ per capita)` * Population) AS PIB_total
FROM `countries of the world`
GROUP BY Region
ORDER BY PIB_total DESC;

SELECT SUM(`GDP ($ per capita)` * Population) AS PIB_total_Afrique
FROM `countries of the world`
WHERE Region LIKE '%AFRICA%';

SELECT COUNT(*) AS nombre_pays_grands
FROM `countries of the world`
WHERE CAST(REPLACE(`Area (sq. mi.)`, ',', '') AS UNSIGNED) >= 1000000;

SELECT SUM(Population) AS population_baltiques
FROM `countries of the world`
WHERE TRIM(Country) IN ('Estonia', 'Latvia', 'Lithuania');

SELECT Region, COUNT(*) AS nombre_pays
FROM `countries of the world`
GROUP BY Region
ORDER BY nombre_pays DESC;

SELECT Region, SUM(Population) AS population_totale
FROM `countries of the world`
GROUP BY Region
HAVING SUM(Population) >= 100000000
ORDER BY population_totale DESC;


-- 1. Taux de mortalité infantile moyen par région
SELECT Region,
       AVG(`Infant mortality (per 1000 births)`) AS avg_infant_mortality
FROM world
GROUP BY Region
ORDER BY avg_infant_mortality DESC;

-- 2. Pays avec la mortalité infantile la plus basse et la plus élevée
SELECT Country,
       `Infant mortality (per 1000 births)`
FROM world
ORDER BY `Infant mortality (per 1000 births)` ASC
LIMIT 5;

SELECT Country,
       `Infant mortality (per 1000 births)`
FROM world
ORDER BY `Infant mortality (per 1000 births)` DESC
LIMIT 5;

-- 3. Corrélation grossière : pays riches vs mortalité infantile
SELECT Country,
       `GDP ($ per capita)`        AS gdp_per_capita,
       `Infant mortality (per 1000 births)` AS infant_mortality
FROM world
WHERE `GDP ($ per capita)` IS NOT NULL
ORDER BY `GDP ($ per capita)` DESC
LIMIT 20;

-- 4. Pays avec les meilleurs taux de literacy
SELECT Country,
       Region,
       `Literacy (%)` AS literacy
FROM world
WHERE `Literacy (%)` IS NOT NULL
ORDER BY `Literacy (%)` DESC
LIMIT 20;

-- 5. Migration nette moyenne par région
SELECT Region,
       AVG(`Net migration`) AS avg_net_migration
FROM world
GROUP BY Region
ORDER BY avg_net_migration DESC;

-- 6. Pays très agricoles (fort pourcentage de terres arables)
SELECT Country,
       Region,
       Arable,
       Crops
FROM world
ORDER BY Arable DESC
LIMIT 20;

-- 7. Naissances et décès moyens par région
SELECT Region,
       AVG(Birthrate) AS avg_birthrate,
       AVG(Deathrate) AS avg_deathrate
FROM world
GROUP BY Region
ORDER BY avg_birthrate DESC;

-- 8. Pays où la croissance naturelle (birthrate - deathrate) est la plus forte/faible
SELECT Country,
       Region,
       Birthrate,
       Deathrate,
       (Birthrate - Deathrate) AS natural_growth
FROM world
WHERE Birthrate IS NOT NULL
  AND Deathrate IS NOT NULL
ORDER BY natural_growth DESC
LIMIT 10;

SELECT Country,
       Region,
       Birthrate,
       Deathrate,
       (Birthrate - Deathrate) AS natural_growth
FROM world
WHERE Birthrate IS NOT NULL
  AND Deathrate IS NOT NULL
ORDER BY natural_growth ASC
LIMIT 10;


