

DROP PROCEDURE IF EXISTS add_diagnose;
DELIMITER $$
CREATE PROCEDURE add_diagnose(code INT, naam VARCHAR(100), datum DATE, beschrijving LONGTEXT, status ENUM("in afwachting", "voorlopig", "bevestigd", "uitgesloten", "chronisch", "herstellend"), arts_code INT, onderzoek INT, ziekte INT)
BEGIN
	INSERT INTO Diagnose(diagnose_code, diagnose_naam, diagnose_datum, diagnose_beschrijving, opmerkingen, diagnose_status, Arts_arts_code) VALUES (code, naam, datum, beschrijving, opmerkingen, status, arts_code);
	INSERT INTO Onderzoek_heeft_Diagnose(Onderzoek_onderzoek_id, Diagnose_diagnose_code) VALUES (onderzoek, code);
    INSERT INTO Diagnose_heeft_Ziekte(Ziekte_ziekte_id, Diagnose_diagnose_code) VALUES (ziekte, code);
END $$
DELIMITER ;

DROP FUNCTION IF EXISTS leeftijd; 

DELIMITER $$

CREATE FUNCTION leeftijd(dob DATE)
RETURNS INT
DETERMINISTIC 
BEGIN
     return TIMESTAMPDIFF(YEAR, dob, CURDATE());
END $$

DELIMITER ;

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

DROP FUNCTION IF EXISTS convert_mg_g;

DELIMITER $$

CREATE FUNCTION convert_mg_g (dosering VARCHAR(100))
RETURNS FLOAT
DETERMINISTIC
BEGIN
	DECLARE dosering_mg FLOAT;
    DECLARE __ VARCHAR(100);
    SET __ = SUBSTRING_INDEX(dosering, ' ', 1);
	SET dosering_mg = CAST(__ AS FLOAT);
    return dosering_mg / 1000;
END $$

DELIMITER ;

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

CALL add_diagnose(314, "Griep", "2022-12-17", 
"Last van verkoudheid, verhoogde lichaamstempratuur, kort ademigheid", "in afwachting", 
85, 220, 12);

CREATE VIEW Bewoner_View AS 
SELECT Bewoner.code, Persoon.voornaam, Persoon.achternaam, Persoon.geboortedatum, Persoon.geslacht, Bewoner.geboorteland, Bewoner.BSN,
Bewoner.nationaliteit, Bewoner.overleden, Bewoner.kiesrecht, md.md_nummer, md.bloedgroep, md.verzekering_informatie, md.rookgedrag, md.alcoholgedrag, md.mentale_gezondheid
FROM Persoon
RIGHT JOIN Bewoner ON Persoon.persoon_nummer = Bewoner.Persoon_persoon_nummer
RIGHT JOIN Medischedossier md ON md.Bewoner_code = Bewoner.code;

CREATE VIEW Activiteiten_View AS
SELECT bv.code, bv.voornaam, bv.achternaam, bv.geboortedatum, acc.activiteit_naam, acc.datum, acc.locatie, acc.categorie, acc.duur FROM Bewoner_bezoekt_Activiteit ac
LEFT JOIN Bewoner_View bv ON bv.code = ac.Bewoner_code
LEFT JOIN Activiteit acc ON acc.activiteit_naam=ac.Activiteit_activiteit_naam 
AND acc.datum=ac.Activiteit_datum 
AND acc.locatie=ac.Activiteit_locatie;

