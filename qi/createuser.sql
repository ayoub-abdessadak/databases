CREATE USER IF NOT EXISTS
"verzorger" IDENTIFIED BY "Welkom01";
GRANT SELECT ON Persoon TO "verzorger";
FLUSH PRIVILEGES;