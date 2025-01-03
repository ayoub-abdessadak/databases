CREATE VIEW Bewoner_Details AS 
SELECT Persoon.voornaam, Persoon.achternaam, Persoon.geboortedatum, Persoon.geslacht, Bewoner.geboorteland, Bewoner.BSN,
Bewoner.nationaliteit, Bewoner.overleden, Bewoner.kiesrecht, md.md_nummer, md.bloedgroep, md.verzekering_informatie, md.rookgedrag, md.alcoholgedrag, md.mentale_gezondheid
FROM Persoon
RIGHT JOIN Bewoner ON Persoon.persoon_nummer = Bewoner.Persoon_persoon_nummer
RIGHT JOIN Medischedossier md ON md.Bewoner_code = Bewoner.code;