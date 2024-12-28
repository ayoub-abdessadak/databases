
DROP DATABASE Verzorgingcentrum;
CREATE DATABASE Verzorgingcentrum;
USE Verzorgingcentrum;

CREATE TABLE Persoon (
    persoon_nummer INT NOT NULL,
    voornaam VARCHAR(100) NULL,
    achternaam VARCHAR(100) NULL,
    geboortedatum DATE NULL,
    geslacht ENUM("man", "vrouw") NULL,
    PRIMARY KEY (persoon_nummer)
);

CREATE TABLE Arts(
    arts_code INT NOT NULL,
    Persoon_persoon_nummer INT NOT NULL,
    PRIMARY KEY (arts_code),
    FOREIGN KEY (Persoon_persoon_nummer) REFERENCES Persoon(persoon_nummer)
);


CREATE TABLE Aanmelding(
    aanmeld_nummer VARCHAR(20) NOT NULL,
    email VARCHAR(200) NULL,
    telefoon_nummer VARCHAR(20) NULL,
    Persoon_persoon_nummer INT NOT NULL,
    PRIMARY KEY (aanmeld_nummer),
    FOREIGN KEY (Persoon_persoon_nummer) REFERENCES Persoon(persoon_nummer)
);

CREATE TABLE Bewoner (
	code INT NOT NULL,
	geboorteplaats VARCHAR(50) NULL,
	geboorteland VARCHAR(85) NULL,
	bsn CHAR(9) NULL,
	nationaliteit VARCHAR(85) NULL,
	overleden TINYINT(1) NULL,
	kiesrecht TINYINT(1) NULL, 
	Persoon_persoon_nummer INT NOT NULL,
	PRIMARY KEY (code),
	FOREIGN KEY (Persoon_persoon_nummer) REFERENCES Persoon(persoon_nummer)	
);

CREATE TABLE Medischedossier(
	md_nummer INT NOT NULL,
	aandachtspunten TINYTEXT NULL,
	specialist_id VARCHAR(50) NULL,
	bloedgroep VARCHAR(25) NULL,
	rookgedrag TINYTEXT NULL,
	alcoholgedrag TINYTEXT NULL,
	lichamelijke_beperkingen TINYTEXT NULL,
	mentale_gezondheid TINYTEXT NULL,
	famillie_geschiedenis MEDIUMTEXT NULL,
	verzekering_informatie MEDIUMTEXT NULL,
	Bewoner_code INT NULL,
	PRIMARY KEY (md_nummer),
	FOREIGN KEY (Bewoner_code) REFERENCES Bewoner(code)
);

CREATE TABLE Medischedossier_heeft_Arts(
	Medischedossier_md_nummer INT NOT NULL,
	Arts_arts_code INT NOT NULL,
	PRIMARY KEY (Medischedossier_md_nummer, Arts_arts_code),
	FOREIGN KEY (Medischedossier_md_nummer) REFERENCES Medischedossier(md_nummer),
	FOREIGN KEY (Arts_arts_code) REFERENCES Arts(arts_code)
);

CREATE TABLE Activiteit(
	activiteit_naam VARCHAR(100) NOT NULL,
	datum DATE NOT NULL,
	locatie VARCHAR(150) NOT NULL,
	categorie VARCHAR(40) NULL,
	activiteit_beschrijving MEDIUMTEXT NULL,
	duur VARCHAR(32) NULL,
	activiteit_status ENUM("binnenkort", "bezig", "beëndigd"),
	PRIMARY KEY (activiteit_naam, datum, locatie)
);

CREATE TABLE Bewoner_bezoekt_Activiteit(
	Bewoner_code INT NOT NULL,
	Activiteit_activiteit_naam VARCHAR(100) NOT NULL,
	Activiteit_datum DATE NOT NULL,
	Activiteit_locatie VARCHAR(150) NOT NULL,
	PRIMARY KEY (Bewoner_code, Activiteit_activiteit_naam, Activiteit_datum, Activiteit_locatie),
	FOREIGN KEY (Bewoner_code) REFERENCES Bewoner(code),
	FOREIGN KEY (Activiteit_activiteit_naam) REFERENCES Activiteit(activiteit_naam),
	FOREIGN KEY (Activiteit_datum) REFERENCES Activiteit(datum),
	FOREIGN KEY (Activiteit_locatie) REFERENCES Activiteit(locatie)
);

CREATE TABLE Zorgplan(
	referentie_nummer INT NOT NULL,
	opstelling_datum DATE NULL,
	herziening_datum DATE NULL,
	zorg_doelen MEDIUMTEXT NULL,
	zorg_type VARCHAR(50) NULL,
	behandel_plan MEDIUMTEXT NULL,
	frequentie_zorg VARCHAR(20) NULL,
	specifieke_instructies MEDIUMTEXT NULL,
	zorgplan_status ENUM("open", "wordt uitgevoerd") NULL,
	opmerkingen MEDIUMTEXT NULL,
	Bewoner_code INT NOT NULL,
    PRIMARY KEY (referentie_nummer)
);
