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

De voglende opgeslagen procedure zorgt ervoor dat een diagnose gelijk gekoppeld wordt aan een onderzoek en ziekte. De regel is dat elke diagnose 1 of meer onderzoeken en 1 of meer ziektes heeft.
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

**Nog meer stored functions**

De volgende opgeslagen functie zet een tijdsduur opgeslagen als string om naar een integer. Wat het nummer in minuten is.

```sql
DROP FUNCTION IF EXISTS tijdsduur_in_min;

DELIMITER $$

CREATE FUNCTION tijdsduur_in_min(minuten VARCHAR(100))
RETURNS INT
DETERMINISTIC
BEGIN
	DECLARE _min INT;
    SET _min = CAST(LEFT(minuten, LOCATE(' ', minuten) - 1) AS SIGNED);
	RETURN _min;
END $$
DELIMITER ;
```

De volgende opgeslagen functie berekent de leeftijd, gegeven een geboorte datum. En de huidige datum.

```sql
DROP FUNCTION IF EXISTS leeftijd;

DELIMITER $$

CREATE FUNCTION leeftijd(dob DATE)
RETURNS INT
DETERMINISTIC
BEGIN
     return TIMESTAMPDIFF(YEAR, dob, CURDATE());
END $$

DELIMITER ;
```

## Views

De volgende view zorgt voor een volledige basis profiel van een Bewoner. De view bestaat uit 2 right joins vanuit de tabel Persoon naar Bewoner en van Bewoner naar Medischedossier. De tabbellen die worden toegevoegd zijn Bewoner (aanvullende BRP gegevens) en Medischedossier (medische gegevens).

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

**View voor junction tabel (meer op meer relatie)**

```sql
CREATE VIEW Activiteiten_View AS
SELECT bv.code, bv.voornaam, bv.achternaam, bv.geboortedatum, acc.activiteit_naam, acc.datum, acc.locatie, acc.categorie, acc.duur FROM Bewoner_bezoekt_Activiteit ac
LEFT JOIN Bewoner_View bv ON bv.code = ac.Bewoner_code
LEFT JOIN Activiteit acc ON (acc.activiteit_naam, acc.datum, acc.
locatie) = (ac.Activiteit_activiteit_naam, ac.Activiteit_datum, ac.Activiteit_locatie);
```

## 10 SQL Queries

### Query 1

**Beschrijving**
De volgende Query selecteert de geboortenaam, bloedgroep en rookgedragingen van elke Bewoner en limiteeert de resultaten tot 5 rijen.

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

### Query 2

**Beschrijving**
De volgendde query haalt de frequentie, toediening_wijze en dosering (in gram) op uit de tabel Medicijngebruik.

**Technisch**
De query selecteert maximaal tien rijen uit de tabel `Medicijngebruik` en haalt daarbij de kolommen `frequentie` en `toediening_wijze` op, samen met een geconverteerde waarde van de kolom `dosering` via de functie `convert_mg_g()`. Deze functie, converteert de dosering van milligram (mg) naar gram (g), en het resultaat wordt weergegeven met een alias `DOSERING_IN_G`. De `LIMIT 10`-clausule beperkt de uitvoer tot maximaal tien rijen. De database verwerkt de query door de tabel `Medicijngebruik` te lezen, de transformatie met `convert_mg_g()` toe te passen op elke rij, en vervolgens alleen de eerste tien resultaten terug te geven.

**Kennis**
De toegepaste kennis is het gebruik van de basis statements, keywords en clausules in SQL in MySQL en het gebruik van een Stored function in een query.

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

### Query 3

**Beschrijving**
De volgende query berekent de gemiddelde leeftijd van bewoners die activiteiten bezoeken met een tijdsduur langer dan 60 minuten.

**Technisch**
De query haalt alle rijen op uit de virtuele tabel `Activiteiten_View`, die is opgebouwd via twee left joins op de junction-tabel `Bewoner_bezoekt_Activiteit`. Deze junction-tabel wordt aangevuld met gegevens uit de tabellen `Activiteit` en de virtuele tabel `Bewoner_View`. De geselecteerde kolommen zijn: `code`, `voornaam`, `achternaam`, `geboortedatum`, `activiteit_naam`, `datum`, `locatie`, `categorie`, en `duur`. Daarnaast maakt de query gebruik van zowel ingebouwde SQL-functies als stored functions. Zo wordt de gemiddelde leeftijd berekend met de functie `AVG` in combinatie met de stored function `leeftijd`, die de leeftijd bepaalt op basis van een opgegeven datum en de huidige dag. Ook wordt de stored function `tijdsduur_in_min` gebruikt om tijdsduren, die als strings zijn opgeslagen, om te zetten naar gehele getallen voor verdere berekeningen. De query maakt gebruik van de `SELECT`-clausule om de gemiddelde leeftijd te berekenen en bevat een `WHERE`-clausule met een "groter dan of gelijk aan"-operator om te filteren op activiteiten met een tijdsduur van 60 minuten of meer. Verder wordt er in de view tabel gebruik gemaakt van de indexes `fk_Bewoner_bezoekt_Activiteit_Bewoner1_idx` en `fk_Medischedossier_Bewoner1_idx`.

**Kennis**
De toegepaste kennis is het gebruik van de basis statements, keywords en clausules in SQL in MySQL en het gebruik van een opgeslagen functie in een query.

**SQL Query**

```sql
SELECT AVG(leeftijd(geboortedatum)) as leeftijd FROM Activiteiten_View WHERE tijdsduur_in_min(duur) >= 60;
```

**SQL Returns**

```bash
+----------+
| leeftijd |
+----------+
| 62.0962  |
+----------+
1 row in set (0,01 sec)
```

De EXPLAIN statement voor de bovenstaande query vertoont het gebruik van de indexes in de View tabel.

```sql
EXPLAIN SELECT AVG(leeftijd(geboortedatum)) as leeftijd FROM Activiteiten_View WHERE tijdsduur_in_min(duur) >= 60;
```

De tabel ac is Activiteit en md is Medischedossier.

```sql
+----+-------------+---------+------------+--------+---------------------------------+--------------------------------------------+---------+-------------------------------------------------------------------------------------------------------------------------------+------+----------+-------------+
| id | select_type | table   | partitions | type   | possible_keys                   | key                                        | key_len | ref                                                                                                                           | rows | filtered | Extra       |
+----+-------------+---------+------------+--------+---------------------------------+--------------------------------------------+---------+-------------------------------------------------------------------------------------------------------------------------------+------+----------+-------------+
|  1 | SIMPLE      | ac      | NULL       | index  | NULL                            | fk_Bewoner_bezoekt_Activiteit_Bewoner1_idx | 4       | NULL                                                                                                                          |  466 |   100.00 | Using index |
|  1 | SIMPLE      | md      | NULL       | ref    | fk_Medischedossier_Bewoner1_idx | fk_Medischedossier_Bewoner1_idx            | 4       | Verzorgingcentrum.ac.Bewoner_code                                                                                             |    1 |   100.00 | Using index |
|  1 | SIMPLE      | Bewoner | NULL       | eq_ref | PRIMARY                         | PRIMARY                                    | 4       | Verzorgingcentrum.ac.Bewoner_code                                                                                             |    1 |   100.00 | NULL        |
|  1 | SIMPLE      | Persoon | NULL       | eq_ref | PRIMARY                         | PRIMARY                                    | 4       | Verzorgingcentrum.Bewoner.Persoon_persoon_nummer                                                                              |    1 |   100.00 | NULL        |
|  1 | SIMPLE      | acc     | NULL       | eq_ref | PRIMARY                         | PRIMARY                                    | 1007    | Verzorgingcentrum.ac.Activiteit_activiteit_naam,Verzorgingcentrum.ac.Activiteit_datum,Verzorgingcentrum.ac.Activiteit_locatie |    1 |   100.00 | Using where |
+----+-------------+---------+------------+--------+---------------------------------+--------------------------------------------+---------+-------------------------------------------------------------------------------------------------------------------------------+------+----------+-------------+
5 rows in set, 1 warning (0,00 sec)
```

### SQL query 4

**Beschrijving**
De volgende query maakt gebruik van 2 subqueries waarbij de medicijn gebruik beter wordt gerepresenteerd aan de hand van relaties naar medicijn gebruik. In deze query wordt de `voornaam`, `toediening_wijze`, `dosering` en `medicijn` opgehaald.

**Technisch**
De gegeven MySQL-query haalt gegevens op uit de tabel Medicijngebruik (mg) en gebruikt geneste subqueries (scalar subqueries) binnen de SELECT-clausule. De eerste subquery haalt de voornaam op uit de Bewoner_View-view door te controleren of de kolom md_nummer overeenkomt met mg.Medischedossier_md_nummer van de hoofdquery. De tweede subquery haalt de naam van het medicijn op uit de tabel Medicijn door te filteren op medicijn_nummer dat overeenkomt met mg.Medicijn_medicijn_nummer. De directe kolommen toediening_wijze en dosering worden rechtstreeks uit Medicijngebruik geselecteerd. De query beperkt de uitvoer tot de eerste vijf rijen (LIMIT 5).

**Kennis**
De toegepaste kennis is het gebruik van de basis statements, keywords en clausules in SQL in MySQL. Ook worden er subqueries gebruikt, gedefinieerd in tussenhaken.

**SQL query**

```sql
SELECT (SELECT voornaam, FROM Bewoner_View bv WHERE bv.md_nummer = mg.Medischedossier_md_nummer) AS voornaam,
toediening_wijze,
dosering,
(SELECT naam FROM Medicijn WHERE medicijn_nummer=mg.Medicijn_medicijn_nummer) as medicijn
FROM Medicijngebruik mg
LIMIT 5;
```

**SQL returns**

```bash
+-------------+-------------------------------+----------+--------------+
| voornaam    | toediening_wijze              | dosering | medicijn     |
+-------------+-------------------------------+----------+--------------+
| Tlachinolli | injectie                      | 100 mg   | Benzonatate  |
| Bo          | topische crème/gel            | 250 mg   | Fluticasone  |
| Evi         | intramusculaire (IM) injectie | 250 mg   | Alprazolam   |
| Amakhar     | orale inname (tablet/capsule) | 150 mg   | Sildenafil   |
| Youssef     | orale inname (tablet/capsule) | 25 mg    | Amoxicilline |
+-------------+-------------------------------+----------+--------------+
5 rows in set (0,00 sec)
```

### SQL Query 5

**Beschrijving**
De query haalt alle zorgverleners op. De zorgverleners hun `big_code`, `voornaam`,

**Technisch**
Deze SQL-query haalt gegevens op uit twee tabellen: `Zorgverlener` (alias `zr`) en `Persoon` (alias `ps`), waarbij `Zorgverlener` een subtypering is van `Persoon`. Dit betekent dat elke zorgverlener ook een persoon is, en dat de tabel `Zorgverlener` aanvullende gegevens bevat specifiek voor zorgverleners. De query maakt gebruik van een `LEFT JOIN`, wat ervoor zorgt dat alle rijen uit de tabel `Zorgverlener` worden weergegeven, zelfs als er geen overeenkomstige rij in de tabel `Persoon` bestaat, wat hoogst onwaarschijnlijk is. De koppeling gebeurt via de sleutel `zr.Persoon_persoon_nummer = ps.persoon_nummer`. De geselecteerde kolommen zijn: `big_code` uit `Zorgverlener`, `voornaam` en `achternaam` uit `Persoon`, de berekende kolom `leeftijd` (gebaseerd op de `geboortedatum` uit `Persoon` met een functie die de leeftijd berekent), `geslacht` uit `Persoon`, en `werkervaring`, `afdeling`, `dienstverband` en `start_datum` uit `Zorgverlener`. De `LIMIT 10`-clausule beperkt de uitvoer tot de eerste 10 rijen van het resultaat.

**Kennis**
De toegepaste kennis is het gebruik van de basis statements, keywords en clausules in SQL in MySQL. Verder wordt er een JOIN statements toegeapst.

**SQL query**

```sql
SELECT zr.big_code, ps.voornaam, ps.achternaam, leeftijd(ps.geboortedatum) AS leeftijd, 
ps.geslacht, zr.werkervaring, zr.afdeling, zr.dienstverband, zr.start_datum FROM Zorgverlener zr
LEFT JOIN Persoon ps ON zr.Persoon_persoon_nummer = ps.persoon_nummer LIMIT 10; 
```

**SQL return**

```bash
+----------------------+------------+-------------------+----------+----------+--------------+----------+---------------+-------------+
| big_code             | voornaam   | achternaam        | leeftijd | geslacht | werkervaring | afdeling | dienstverband | start_datum |
+----------------------+------------+-------------------+----------+----------+--------------+----------+---------------+-------------+
| 0017146e-92e1-48d6-a | Iris       | van Waas          |       68 | vrouw    | 6-10 jaar    | Overal   | Part-time     | 2000-10-16  |
| 002862dd-77ce-4ba2-a | Kyan       | de Kok            |       36 | man      | 2-4 jaar     | Overal   | Fulltime      | 2000-10-16  |
| 006bf766-7ef1-4299-a | Victoria   | Palman            |       56 | vrouw    | 2-4 jaar     | Overal   | Part-time     | 2000-10-16  |
| 0077a49c-93e7-4239-b | Anders     | Wolfswinkel       |       72 | man      | 7-10 jaar    | Overal   | Part-time     | 2000-10-16  |
| 00aef53d-9140-4246-8 | Aglæca     | van der Spaendonc |      102 | man      | 2-4 jaar     | Overal   | Part-time     | 2000-10-16  |
| 00d67b49-12ef-4294-9 | Chanin     | Spanhaak          |      116 | man      | 2-4 jaar     | Overal   | Fulltime      | 2000-10-16  |
| 00f976e5-e2f0-4d31-a | Hildebrand | Labado            |       95 | man      | 2-5 jaar     | Overal   | Part-time     | 2000-10-16  |
| 018a67a7-a070-4032-9 | Tirza      | van Noordeloos    |      119 | vrouw    | 2-5 jaar     | Overal   | Part-time     | 2000-10-16  |
| 0191061c-faf2-47af-8 | Lidan-gula | Serra             |      105 | man      | 10+ jaar     | Overal   | Nul uren      | 2000-10-16  |
| 019ae22a-ca56-4b2c-a | Jayda      | Momberg           |       96 | vrouw    | 2-5 jaar     | Overal   | Part-time     | 2000-10-16  |
+----------------------+------------+-------------------+----------+----------+--------------+----------+---------------+-------------+
10 rows in set (0,00 sec)
```

**Query explain**

```bash
+----+-------------+-------+------------+--------+---------------+---------+---------+---------------------------------------------+------+----------+-------+
| id | select_type | table | partitions | type   | possible_keys | key     | key_len | ref                                         | rows | filtered | Extra |
+----+-------------+-------+------------+--------+---------------+---------+---------+---------------------------------------------+------+----------+-------+
|  1 | SIMPLE      | zr    | NULL       | ALL    | NULL          | NULL    | NULL    | NULL                                        | 2286 |   100.00 | NULL  |
|  1 | SIMPLE      | ps    | NULL       | eq_ref | PRIMARY       | PRIMARY | 4       | Verzorgingcentrum.zr.Persoon_persoon_nummer |    1 |   100.00 | NULL  |
+----+-------------+-------+------------+--------+---------------+---------+---------+---------------------------------------------+------+----------+-------+
2 rows in set, 1 warning (0,01 sec)
```

### Query 6

**Beschrijving**
De query haalt alle soorten ziektes geassocieerd met kanker op.

**Technisch**
De SQL-query `SELECT naam, beschrijving FROM Ziekte WHERE naam LIKE "%kanker%";` haalt gegevens op uit de tabel `Ziekte`. Specifiek selecteert de query de kolommen `naam` en `beschrijving`. De `WHERE`-clausule beperkt de resultaten tot rijen waarbij de kolom `naam` een tekenreeks bevat die overeenkomt met het woord "kanker" op een willekeurige positie in de tekst. Het percentage-teken (`%`) is een wildcard in SQL, wat betekent dat er vóór en na het woord "kanker" elk aantal tekens (inclusief geen) kan staan. Dit maakt de zoekopdracht een patroonzoekopdracht (case-insensitive in de meeste databases, afhankelijk van de collation). Het resultaat bevat alle ziekten waarvan de naam het woord "kanker" bevat, samen met hun bijbehorende beschrijving.

**Kennis**
De toegepaste kennis is het gebruik van de basis statements, keywords en clausules in SQL in MySQL. Verder wordt er gebruik gemaakt van pattern matching.

**SQL query**
```sql
SELECT naam, beschrijving FROM Ziekte WHERE naam LIKE "%kanker%";
```

**SQL returns**
```bash
+--------------------------+----------------------------------------------------------------------------------+
| naam                     | beschrijving                                                                     |
+--------------------------+----------------------------------------------------------------------------------+
| Kanker                   | Een groep van ziekten gekenmerkt door oncontroleerbare celgroei en verspreiding. |
| Borstkanker              | Een type kanker dat begint in de cellen van de borst.                            |
| Prostaatkanker           | Een type kanker dat voorkomt in de prostaat, een klier bij mannen.               |
| Schildklierkanker        | Een type kanker dat begint in de schildklier, een klier in de hals.              |
| Kanker van de Dikke Darm | Een type kanker dat begint in de dikke darm of endeldarm.                        |
+--------------------------+----------------------------------------------------------------------------------+
5 rows in set (0,00 sec)
```

### Query 7

**Beschrijving**
De query haalt alle beschrijvingen met het woord verlies daarin.

**Technisch**
De SQL-query `SELECT naam, beschrijving FROM Ziekte WHERE naam LIKE "%kanker%";` haalt gegevens op uit de tabel `Ziekte`. Specifiek selecteert de query de kolommen `naam` en `beschrijving`. De `WHERE`-clausule beperkt de resultaten tot rijen waarbij de kolom `naam` een tekenreeks bevat die overeenkomt met het woord "kanker" op een willekeurige positie in de tekst. Het percentage-teken (`%`) is een wildcard in SQL, wat betekent dat er vóór en na het woord "kanker" elk aantal tekens (inclusief geen) kan staan. Dit maakt de zoekopdracht een patroonzoekopdracht (case-insensitive in de meeste databases, afhankelijk van de collation). Het resultaat bevat alle ziekten waarvan de naam het woord "kanker" bevat, samen met hun bijbehorende beschrijving.

**Kennis**
De toegepaste kennis is het gebruik van de basis statements, keywords en clausules in SQL in MySQL. Verder wordt er gebruik gemaakt van pattern matching.

**SQL query**
```sql
SELECT soort, beschrijving_bijwerking FROM Bijwerking
WHERE beschrijving_bijwerking REGEXP '(?i)verlies';
```

**SQL returns**
```bash
+-----------------------------+--------------------------------------------------------------+
| soort                       | beschrijving_bijwerking                                      |
+-----------------------------+--------------------------------------------------------------+
| Gewichtsverlies             | Kan leiden tot ongewenst gewichtsverlies.                    |
| Gewichtstoename             | Kan leiden tot ongewenst gewichtsverlies of -toename.        |
| Verminderde Appetiet        | Kan leiden tot gewichtsverlies of verminderde eetlust.       |
| Gewichtsverandering         | Kan leiden tot gewichtsverlies of -toename.                  |
| Verlies van Water en Zouten | Kan leiden tot uitdroging en verlies van essentiële zouten.  |
| Verminderde Eetlust         | Kan leiden tot gewichtsverlies of verminderde eetlust.       |
| Flauwvallen                 | Kan leiden tot flauwvallen of bewustzijnsverlies.            |
+-----------------------------+--------------------------------------------------------------+
7 rows in set (0,00 sec)
```

### Query 8

**Beschrijving**
De query telt alle toegediende en niet toegediende vaccinaties op.

**Technisch**
De SQL-query haalt gegevens op uit de tabel `Vaccinatie`. De query selecteert de kolom `vaccinatie_status` en telt het aantal rijen (`COUNT(*)`) voor elke unieke waarde in deze kolom, waarbij alleen de statussen `"Toegediend"` en `"Niet Toegediend"` worden meegenomen. De `WHERE`-clausule filtert de gegevens zodat alleen records met deze twee vaccinatiestatussen worden geanalyseerd. De `GROUP BY`-clausule groepeert vervolgens de resultaten per unieke waarde van `vaccinatie_status`, zodat de telling (`COUNT(*)`) per groep wordt weergegeven. De kolom `aantal` wordt met een alias (`AS`) hernoemd, wat het resultaat overzichtelijker maakt. Het resultaat toont dus per vaccinatiestatus het totale aantal rijen dat aan de filtercriteria voldoet.

**Kennis**
De toegepaste kennis is het gebruik van de basis statements, keywords en clausules in SQL in MySQL. Verder wordt er gebruik gemaakt van de ingebouwde COUNT functie en de group by clausule.

**SQL query**
```sql
SELECT 
    vaccinatie_status, 
    COUNT(*) AS aantal 
FROM 
    Vaccinatie 
WHERE 
    vaccinatie_status IN ("Toegediend", "Niet Toegediend")
GROUP BY 
    vaccinatie_status;
```

**SQL returns**
```bash
+-------------------+--------+
| vaccinatie_status | aantal |
+-------------------+--------+
| Toegediend        |  29280 |
| Niet toegediend   |  29673 |
+-------------------+--------+
2 rows in set (0,05 sec)
```

### Query 9

**Beschrijving**


**Technisch**


**Kennis**


**SQL query**
```sql

```

**SQL returns**
```bash

```

### Query 10

**Beschrijving**


**Technisch**


**Kennis**


**SQL query**
```sql

```

**SQL returns**
```bash

```