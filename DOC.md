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



