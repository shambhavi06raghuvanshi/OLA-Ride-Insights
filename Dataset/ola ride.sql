USE ola_project;

SHOW TABLES;
DESCRIBE ola_cleaned;

USE ola_project;

SELECT 'ola_cleaned' AS table_name, COUNT(*) AS total_rows
FROM ola_cleaned

UNION ALL

SELECT 'ola_rides', COUNT(*)
FROM ola_rides;