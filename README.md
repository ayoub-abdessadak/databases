# SQL Verzorgingcentrum


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

De voglende opgeslagen procedure zorgt ervoor dat een diagnose gelijk gekoppeld wordt aan een onderzoek en ziekte. De regel is dat elke diagnose 1 of meer onderzoeken heeft en 1 of meer ziektes.
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

## Views
De volgende view brengt zorgt voor een volledige basis profiel van een Bewoner
```sql
CREATE VIEW Bewoner_Details AS 
SELECT Persoon.voornaam, Persoon.achternaam, Persoon.geboortedatum, Persoon.geslacht, Bewoner.geboorteland, Bewoner.BSN,
Bewoner.nationaliteit, Bewoner.overleden, Bewoner.kiesrecht, md.md_nummer, md.bloedgroep, md.verzekering_informatie, md.rookgedrag, md.alcoholgedrag, md.mentale_gezondheid
FROM Persoon
RIGHT JOIN Bewoner ON Persoon.persoon_nummer = Bewoner.Persoon_persoon_nummer
RIGHT JOIN Medischedossier md ON md.Bewoner_code = Bewoner.code;
```

**SQL Query**
```sql
SELECT * FROM Bewoner_Details LIMIT 10;
```

**SQL Returns**
```bash
+-----------------+--------------+---------------+----------+---------------+----------+---------------+-----------+-----------+-----------+------------+------------------------+--------------------------+----------------------------+---------------------------------------+
| voornaam        | achternaam   | geboortedatum | geslacht | geboorteland  | BSN      | nationaliteit | overleden | kiesrecht | md_nummer | bloedgroep | verzekering_informatie | rookgedrag               | alcoholgedrag              | mentale_gezondheid                    |
+-----------------+--------------+---------------+----------+---------------+----------+---------------+-----------+-----------+-----------+------------+------------------------+--------------------------+----------------------------+---------------------------------------+
| Merodak-mu-basa | Mathol       | 1962-12-31    | man      | West-Europees | 59374128 | Nederlandse   |         0 |         1 |         0 | A+         | Paramed                | Verslaafde rokers        | Vervangend drinker         | Paranoïde persoonlijkheidsstoornis    |
| Savvas          | van Straaten | 2016-12-31    | man      | Surinaams     | 28614357 | Nederlandse   |         0 |         1 |         1 | A-         | VGZ                    | Creatief roken           | Vervangend drinker         | Dissociatieve amnesie                 |
| Amasis          | de Grunt     | 1952-01-11    | man      | Hongaarse     | 86724931 | Nederlandse   |         0 |         1 |         2 | B+         | ANWB Zorgverzekering   | Vervangend roken         | Experimenterend drinker    | Aanpassingsstoornis                   |
| Stefan          | Wolfsdr      | 1961-12-31    | vrouw    | Filipijns     | 98634512 | Nederlandse   |         0 |         1 |         3 | B-         | DSW                    | Verslaafde rokers        | Gezondheidsbewuste drinker | Boulimia nervosa                      |
| Geeraard        | Bezemer      | 1932-01-16    | man      | Grieks        | 69341572 | Nederlandse   |         0 |         1 |         4 | A-         | SNS Zorgverzekering    | Intermitterend roken     | Aangepaste drinker         | Insomnie                              |
| Siem            | Mulder       | 1955-12-27    | vrouw    | Zweeds        | 13857946 | Nederlandse   |         0 |         1 |         5 | O+         | Achmea                 | Gelegenheidsrokers       | Feestdrinker               | Schizoaffectieve stoornis             |
| Philip          | Horrocks     | 2009-12-19    | man      | Vietnamese    | 57241869 | Nederlandse   |         0 |         1 |         6 | A-         | DSW                    | Roken tijdens pauzes     | Functioneel drinker        | Afhankelijke persoonlijkheidsstoornis |
| Pien            | Smits        | 1991-12-12    | man      | Afrikaans     | 56843912 | Nederlandse   |         0 |         1 |         7 | B-         | Menzis                 | Stress roken             | Aangepaste drinker         | Zelfbeschadigend gedrag               |
| Xavi            | Oostveen     | 2021-12-17    | man      | Tsjechisch    | 57916834 | Nederlandse   |         0 |         1 |         8 | AB+        | FBTO                   | Stress roken             | Verslaafde drinker         | Schizoaffectieve stoornis             |
| Milo            | de Strigter  | 2012-12-19    | vrouw    | West-Europees | 95134786 | Nederlandse   |         0 |         1 |         9 | O+         | SNS Zorgverzekering    | Roken tijdens maaltijden | Verslaafde drinker         | Pica                                  |
+-----------------+--------------+---------------+----------+---------------+----------+---------------+-----------+-----------+-----------+------------+------------------------+--------------------------+----------------------------+---------------------------------------+
10 rows in set (0,00 sec)
```

## 10 SQL Queries

### Query 1

**Beschrijving**
De voglende Query selecteert de geboortenaam, bloedgroep en rookgedragingen van elke Bewoner. 

**Technisch**
De query haalt maximaal vijf rijen op uit de view `Bewoner_View` en selecteert daarbij de kolommen `geboortedatum`, `bloedgroep`, en `rookgedrag`. Een view is een virtuele tabel die is gebaseerd op een onderliggende query en wordt gebruikt om data uit een of meerdere tabellen te presenteren. De `LIMIT 5`-clausule beperkt het resultaat tot vijf rijen. De database voert eerst de query van de view uit, selecteert de opgegeven kolommen en past vervolgens de rijbeperking toe.

**Kennis**
De toegepaste kennis is het gebruik van de basis statements, keywords en clausules in SQL in MySQL en het gebruik van een View (Virtuele tabel).

**SQL Query**
```sql
SELECT geboortedatum, bloedgroep, rookgedrag FROM Bewoner_View LIMIT 5;
```

**SQL Returns**
```bash
+---------------+------------+----------------------+
| geboortedatum | bloedgroep | rookgedrag           |
+---------------+------------+----------------------+
| 1962-12-31    | A+         | Verslaafde rokers    |
| 2016-12-31    | A-         | Creatief roken       |
| 1952-01-11    | B+         | Vervangend roken     |
| 1961-12-31    | B-         | Verslaafde rokers    |
| 1932-01-16    | A-         | Intermitterend roken |
+---------------+------------+----------------------+
```
