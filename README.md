# SQL Queries Verzorgingcentrum


## Triggers

De voglende Trigger voegt automatisch een Bewoner_heeft_Zorgverlener rij toe op het moment dat een Bewoner wordt toegevoegd. De toegewezen zorgverlener is de zorgverlener met de minste bewoners.

**SQL Trigger**

```sql
DELIMITER $$
CREATE TRIGGER trigger_bewoner_heeft_zorgverlener 
AFTER INSERT ON Bewoner
FOR EACH ROW
	BEGIN
		DECLARE _zorgverlener_big_code CHAR(20);
		SELECT lt.big_code INTO _zorgverlener_big_code
		FROM Zorgverlener lt
		LEFT JOIN Bewoner_heeft_Zorgverlener jt ON lt.big_code = jt.Zorgverlener_big_code
		GROUP BY lt.big_code
		ORDER BY COUNT(jt.Zorgverlener_big_code) ASC
		LIMIT 1;
		
		INSERT INTO Bewoner_heeft_Zorgverlener(Zorgverlener_big_code, Bewoner_code) VALUES(_zorgverlener_big_code, NEW.code);
	END$$
DELIMITER ;
```

Ik voeg vervolgens een Persoon en dan een Bewoner toe.
**SQL Insertion**
```sql

-- Persoon
INSERT INTO Persoon(persoon_nummer, voornaam, achternaam, geboortedatum, geslacht) 
VALUES (9154, "Ayoub", "ben Abdessadak", "1900-01-01", "man");

-- Bewoner
INSERT INTO Bewoner(code, geboorteplaats, geboorteland, bsn, nationaliteit, overleden, kiesrecht, Persoon_persoon_nummer)
VALUES
(4573, "Groningen", "Nederland", 123456789, "Nederlandse", 0, 1, 9154);

```

Er is automatisch een rij voor het table Bewoner_heeft_Zorgverlener toegevoegd door de trigger.
**SQL Query**
```sql
SELECT * FROM Bewoner_heeft_Zorgverlener WHERE Bewoner_code=4573;
```

**SQL returns**
```bash
+-----------------------+--------------+
| Zorgverlener_big_code | Bewoner_code |
+-----------------------+--------------+
| 95e8b51c-41a3-4b22-b  |         4573 |
+-----------------------+--------------+
1 row in set (0,00 sec)
```

## Stored procedures

De voglende opgeslagen procedure zorgt ervoor dat een diagnose gelijk toegevoegd wordt aan een onderzoek en een ziekte. De regel is dat elke diagnose 1 of meer onderzoeken heeft en 1 of meer ziektes.
**SQL Stored Procedure**
```sql
DROP PROCEDURE IF EXISTS add_diagnose;
DELIMITER $$
CREATE PROCEDURE add_diagnose(code INT, naam VARCHAR(100), datum DATE, beschrijving LONGTEXT, status ENUM("in afwachting", "voorlopig", "bevestigd", "uitgesloten", "chronisch", "herstellend"), arts_code INT, onderzoek INT, ziekte INT)
BEGIN
	INSERT INTO Diagnose(diagnose_code, diagnose_naam, diagnose_datum, diagnose_beschrijving, opmerkingen, diagnose_status, Arts_arts_code) VALUES (code, naam, datum, beschrijving, opmerkingen, status, arts_code);
	INSERT INTO Onderzoek_heeft_Diagnose(Onderzoek_onderzoek_id, Diagnose_diagnose_code) VALUES (onderzoek, code);
        INSERT INTO Diagnose_heeft_Ziekte(Ziekte_ziekte_id, Diagnose_diagnose_code) VALUES (ziekte, code);
END $$
DELIMITER ;
```
**Stored procedure aan roepen**
```sql
CALL add_diagnose(315, "Griep", "2022-12-17", "Last van verkoudheid, verhoogde lichaamstempratuur, kort ademigheid", "in afwachting", 85, 220, 12);
```
**SQL query**
```sql
SELECT * FROM Onderzoek_heeft_Diagnose WHERE Diagnose_diagnose_code=315;
```

**SQL returns**
```bash
+------------------------+------------------------+
| Onderzoek_onderzoek_id | Diagnose_diagnose_code |
+------------------------+------------------------+
|                    220 |                    315 |
+------------------------+------------------------+
1 row in set (0,00 sec)
```
**SQL query**
```sql
SELECT * FROM Diagnose_heeft_Ziekte WHERE Diagnose_diagnose_code=315;
```

**SQL returns**
```bash
+------------------+------------------------+
| Ziekte_ziekte_id | Diagnose_diagnose_code |
+------------------+------------------------+
|               12 |                    315 |
+------------------+------------------------+
1 row in set (0,00 sec)
```

## Stored functions
De volgende opgeslagen functie converteert de dosering die in mg wordt opgeslagen naar gram. 

```sql
DROP FUNCTION IF EXISTS convert_mg_g;

DELIMITER $$

CREATE FUNCTION convert_mg_g (dosering VARCHAR(100))
RETURNS FLOAT
DETERMINISTIC
BEGIN
	DECLARE dosering_mg FLOAT;
    DECLARE __ VARCHAR(100);
    SET __ = SUBSTRING_INDEX(dosering, ' ', 1); -- OF REGEXP_REPLACE(dosering, '[^0-9.]', '');
    SET dosering_mg = CAST(__ AS FLOAT);
    return dosering_mg / 1000;
END $$

DELIMITER ;

```
De stored functie kan als volgt gebruikt worden in een SQL query
**SQL Query**
```sql
SELECT frequentie, toediening_wijze, convert_mg_g(dosering) AS DOSERING_IN_G FROM Medicijngebruik LIMIT 10;
```
**SQL Returns**
```bash
+----------------------+-------------------------------+---------------+
| frequentie           | toediening_wijze              | DOSERING_IN_G |
+----------------------+-------------------------------+---------------+
| één keer per maand   | injectie                      |           0.1 |
| elke 12 uur          | topische crème/gel            |          0.25 |
| één keer per dag     | intramusculaire (IM) injectie |          0.25 |
| elke 2 weken         | orale inname (tablet/capsule) |          0.15 |
| één keer per nacht   | orale inname (tablet/capsule) |         0.025 |
| elke 2 weken         | topische crème/gel            |           0.1 |
| één keer per week    | intramusculaire (IM) injectie |          0.02 |
| drie keer per dag    | oculaire (oogdruppels)        |         0.025 |
| één keer per maand   | transdermale patch            |          0.02 |
| elke 3 uur           | nasale spray                  |          0.05 |
+----------------------+-------------------------------+---------------+
10 rows in set (0,00 sec)
```

## 10 SQL Queries

Deze query doet iets, de query werkt als volgt, de query vertoont

**SQL query**
```sql
DESCRIBE Medicijn;
```
**MySQL Returns**
```bash
+-----------------+--------------+------+-----+---------+-------+
| Field           | Type         | Null | Key | Default | Extra |
+-----------------+--------------+------+-----+---------+-------+
| medicijn_nummer | int          | NO   | PRI | NULL    |       |
| naam            | varchar(100) | YES  |     | NULL    |       |
| beschrijving    | mediumtext   | YES  |     | NULL    |       |
| handleiding     | longtext     | YES  |     | NULL    |       |
| fabrikant       | varchar(100) | YES  |     | NULL    |       |
+-----------------+--------------+------+-----+---------+-------+
5 rows in set (0,00 sec)
```



