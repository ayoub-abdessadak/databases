CREATE VIEW Activiteiten_View AS
SELECT bv.code, bv.voornaam, bv.achternaam, bv.geboortedatum, acc.activiteit_naam, acc.datum, acc.locatie, acc.categorie, acc.duur FROM Bewoner_bezoekt_Activiteit ac
LEFT JOIN Bewoner_View bv ON bv.code = ac.Bewoner_code
LEFT JOIN Activiteit acc ON (acc.activiteit_naam, acc.datum, acc.
locatie) = (ac.Activiteit_activiteit_naam, ac.Activiteit_datum, ac.Activiteit_locatie);