
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
	INDEX fk_Arts_Persoon_idx (Persoon_persoon_nummer ASC) VISIBLE,
	CONSTRAINT fk_Arts_Persoon1
		FOREIGN KEY (Persoon_persoon_nummer) 
		REFERENCES Persoon(persoon_nummer)
		ON DELETE CASCADE
		ON UPDATE NO ACTION
);


CREATE TABLE Aanmelding(
	aanmeld_nummer VARCHAR(20) NOT NULL,
	email VARCHAR(200) NULL,
	telefoon_nummer VARCHAR(20) NULL,
	Persoon_persoon_nummer INT NOT NULL,
	PRIMARY KEY (aanmeld_nummer),
	INDEX fk_Aanmelding_Persoon1 (Persoon_persoon_nummer ASC) VISIBLE,
	CONSTRAINT fk_Aanmelding_Persoon1
		FOREIGN KEY (Persoon_persoon_nummer) 
		REFERENCES Persoon(persoon_nummer)
		ON DELETE CASCADE
		ON UPDATE NO ACTION
);

CREATE TABLE Bewoner(
	code INT NOT NULL,
	geboorteplaats VARCHAR(50) NULL,
	geboorteland VARCHAR(85) NULL,
	bsn CHAR(9) NULL,
	nationaliteit VARCHAR(85) NULL,
	overleden TINYINT(1) NULL,
	kiesrecht TINYINT(1) NULL,
    Persoon_persoon_nummer INT NOT NULL,
	PRIMARY KEY (code),
	INDEX fk_Bewoner_Persoon1_idx (Persoon_persoon_nummer ASC) VISIBLE,
	CONSTRAINT fk_Bewoner_Persoon1
		FOREIGN KEY (Persoon_persoon_nummer)
		REFERENCES Persoon(persoon_nummer)
		ON DELETE CASCADE
		ON UPDATE NO ACTION
);

CREATE TABLE Medischedossier(
	md_nummer INT NOT NULL,
	aandachtspunten TINYTEXT NULL,
	bloedgroep VARCHAR(25) NULL,
	rookgedrag TINYTEXT NULL,
	alcoholgedrag TINYTEXT NULL,
	lichamelijke_beperkingen TINYTEXT NULL,
	mentale_gezondheid TINYTEXT NULL,
	famillie_geschiedenis MEDIUMTEXT NULL,
	verzekering_informatie MEDIUMTEXT NULL,
	Bewoner_code INT NOT NULL,
	PRIMARY KEY (md_nummer),
	INDEX fk_Medischedossier_Bewoner1_idx (Bewoner_code ASC) VISIBLE,
	CONSTRAINT fk_Medischedossier_Bewoner
		FOREIGN KEY (Bewoner_code)
		REFERENCES Bewoner(code)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Medischedossier_heeft_Arts(
	Medischedossier_md_nummer INT NOT NULL,
	Arts_arts_code INT NOT NULL,
	PRIMARY KEY (Medischedossier_md_nummer, Arts_arts_code),
	INDEX fk_Medischedossier_heeft_Arts_Medischedossier1_idx (Medischedossier_md_nummer ASC) VISIBLE,
	INDEX fk_Medischedossier_heeft_Arts_Arts1_idx (Arts_arts_code ASC) VISIBLE,
	CONSTRAINT fk_Medischedossier_heeft_Arts_Medischedossier 
		FOREIGN KEY (Medischedossier_md_nummer)
		REFERENCES Medischedossier(md_nummer)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Medischedossier_heeft_Arts_Arts
		FOREIGN KEY (Arts_arts_code)
		REFERENCES Arts(arts_code)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
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
	INDEX fk_Bewoner_bezoekt_Activiteit_Activiteit1_idx (Activiteit_activiteit_naam ASC, Activiteit_datum ASC, Activiteit_locatie ASC) VISIBLE,
	INDEX fk_Bewoner_bezoekt_Activiteit_Bewoner1_idx (Bewoner_code ASC) VISIBLE,
	CONSTRAINT fk_Bewoner_bezoekt_Activiteit_Bewoner
		FOREIGN KEY (Bewoner_code)
		REFERENCES Bewoner(code)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Bewoner_bezoekt_Activiteit_Activiteit
		FOREIGN KEY (Activiteit_activiteit_naam, Activiteit_datum, Activiteit_locatie)
		REFERENCES Activiteit(activiteit_naam, datum, locatie)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Bewoner_bezocht_Activiteit(
    Bewoner_code INT NOT NULL,
	Activiteit_activiteit_naam VARCHAR(100) NOT NULL,
	Activiteit_datum DATE NOT NULL,
	Activiteit_locatie VARCHAR(150) NOT NULL,
	PRIMARY KEY (Bewoner_code, Activiteit_activiteit_naam, Activiteit_datum, Activiteit_locatie),
	INDEX fk_Bewoner_bezocht_Activiteit_Activiteit1_idx (Activiteit_activiteit_naam ASC, Activiteit_datum ASC, Activiteit_locatie ASC) VISIBLE,
	INDEX fk_Bewoner_bezocht_Activiteit_Bewoner1_idx (Bewoner_code ASC) VISIBLE,
	CONSTRAINT fk_Bewoner_bezocht_Activiteit_Activiteit
		FOREIGN KEY (Activiteit_activiteit_naam, Activiteit_datum, Activiteit_locatie)
		REFERENCES Activiteit(activiteit_naam, datum, locatie)
		ON DELETE CASCADE
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Bewoner_bezochtActiviteit_Bewoner
		FOREIGN KEY (Bewoner_code)
		REFERENCES Bewoner(code)
		ON DELETE CASCADE
		ON UPDATE NO ACTION
);

CREATE TABLE Zorgplan(
	referentie_nummer INT NOT NULL,
	opstelling_datum DATE NULL,
	herziening_datum DATE NULL,
	zorg_doelen MEDIUMTEXT NULL,
	zorg_type VARCHAR(50) NULL,
	behandel_plan MEDIUMTEXT NULL,
	frequentie_zorg VARCHAR(2) NULL,
	specifieke_instructies MEDIUMTEXT NULL,
	zorgplan_status ENUM("open", "wordt uitgevoerd") NULL,
	opmerkingen MEDIUMTEXT NULL,
	Bewoner_code INT NOT NULL,
	PRIMARY KEY (referentie_nummer),
	INDEX fk_Zorgplan_Bewoner1_idx (Bewoner_code ASC) VISIBLE,
	CONSTRAINT fk_Zorgplan_Bewoner
		FOREIGN KEY (Bewoner_code)
		REFERENCES Bewoner(code)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Zorgbehoefte(
	zb_code INT NOT NULL,
	zb_categorie VARCHAR(40) NULL,
	zb_naam VARCHAR(50) NULL,
	zb_beschrijving MEDIUMTEXT NULL,
	urgentie TINYINT(1) NULL,
	PRIMARY KEY (zb_code)
);

CREATE TABLE Bewoner_heeft_Zorgbehoefte(
	Zorgbehoefte_zb_code INT NOT NULL,
	Bewoner_code INT NOT NULL,
	PRIMARY KEY (Zorgbehoefte_zb_code, Bewoner_code),
	INDEX fk_Zorgbehoefte_heeft_Bewoner_Bewoner1_idx (Bewoner_code ASC) VISIBLE,
	INDEX fk_Zorgbehoefte_heeft_Bewoner_Zorgbehoefte1_idx (Zorgbehoefte_zb_code ASC) VISIBLE,
	CONSTRAINT fk_Zorgbehoefte_heeft_Bewoner_Bewoner 
		FOREIGN KEY (Bewoner_code)
		REFERENCES Bewoner(code)
		ON DELETE RESTRICT 
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Zorgbehoefte_heeft_Bewoner_Zorgbehoefte
		FOREIGN KEY (Zorgbehoefte_zb_code)
		REFERENCES Zorgbehoefte(zb_code)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Zorgverlener(
	big_code VARCHAR(20) NOT NULL,
	werkervaring VARCHAR(40) NULL,
	afdeling VARCHAR(80) NULL,
	dienstverband VARCHAR(30) NULL,
	opmerkingen TINYTEXT NULL,
	start_datum DATE NULL,
	Persoon_persoon_nummer INT NOT NULL,
	PRIMARY KEY (big_code),
	INDEX fk_Zorgverlener_Persoon (Persoon_persoon_nummer ASC) VISIBLE,
	CONSTRAINT fk_Zorgverlener_Persoon
		FOREIGN KEY (Persoon_persoon_nummer)
		REFERENCES Persoon(persoon_nummer)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Bewoner_heeft_Zorgverlener(
	Zorgverlener_big_code VARCHAR(20) NOT NULL,
	Bewoner_code INT NOT NULL,
	PRIMARY KEY (Zorgverlener_big_code, Bewoner_code),
	INDEX fk_Bewoner_heeft_Zorgverlener_Bewoner1_idx (Bewoner_code ASC) VISIBLE,
	INDEX fk_Bewoner_heeft_Zorgverlener_Zorgverlener1_idx (Zorgverlener_big_code ASC) VISIBLE,
	CONSTRAINT fk_Bewoner_heeft_Zorgverlener_Bewoner
		FOREIGN KEY (Bewoner_code)
		REFERENCES Bewoner(code)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Bewoner_heeft_Zorgverlener_Zorgverlener
		FOREIGN KEY (Zorgverlener_big_code)
		REFERENCES Zorgverlener(big_code)
		ON DELETE RESTRICT 
		ON UPDATE NO ACTION
);

CREATE TABLE Specialisatie(
	specialisatie_code INT NOT NULL,
	specialisatie_naam VARCHAR(100) NULL,
	specialisatie_beschrijving MEDIUMTEXT NULL,
	PRIMARY KEY(specialisatie_code)
);

CREATE TABLE Team(
	team_naam VARCHAR(50) NOT NULL,
	omschrijving TINYTEXT NULL,
	aantal_leden INT NULL,
    PRIMARY KEY(team_naam)
);

CREATE TABLE Zorgverlener_heeft_Specialisatie(
	Zorgverlener_big_code VARCHAR(20) NOT NULL,
	Specialisatie_specialisatie_code INT NOT NULL,
	PRIMARY KEY (Zorgverlener_big_code, Specialisatie_specialisatie_code),
	INDEX fk_Zorgverlener_heeft_Specialisatie_Zorverlener1_idx (Zorgverlener_big_code ASC) VISIBLE,
	INDEX fk_Zorgverlener_heeft_Specialisatie_Specialisatie1_idx (Specialisatie_specialisatie_code ASC) VISIBLE,
	CONSTRAINT fk_Zorgverlener_heeft_Specialisatie_Zorgverlener
		FOREIGN KEY (Zorgverlener_big_code)
		REFERENCES Zorgverlener(big_code)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Zorgverlener_heeft_Specialisatie_Specialisatie
		FOREIGN KEY (Specialisatie_specialisatie_code)
		REFERENCES Specialisatie(specialisatie_code)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Zorgverlener_heeft_Team(
	Zorgverlener_big_code VARCHAR(20) NOT NULL,
	Team_team_naam VARCHAR(20) NOT NULL,
	PRIMARY KEY (Zorgverlener_big_code, Team_team_naam),
	INDEX fk_Zorgverlener_heeft_Team_Zorgverlener1_idx (Zorgverlener_big_code ASC) VISIBLE,
	INDEX fk_Zorgverlener_heeft_Team_Team1_idx (Team_team_naam ASC) VISIBLE,
	CONSTRAINT fk_Zorgverlener_heeft_Team_Zorgverlener
		FOREIGN KEY (Zorgverlener_big_code)
		REFERENCES Zorgverlener(big_code)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Zorgverlener_heeft_Team_Team
		FOREIGN KEY (Team_team_naam)
		REFERENCES Team(team_naam)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);	

CREATE TABLE Bijwerking(
	bijwerking_id INT NOT NULL AUTO_INCREMENT,
	soort VARCHAR(120) NOT NULL UNIQUE,
	beschrijving_bijwerking LONGTEXT NULL,
	PRIMARY KEY (bijwerking_id),
	INDEX soort_UNIQUE (soort ASC) VISIBLE
);

CREATE TABLE Medicijn(
	medicijn_nummer INT NOT NULL,
	naam VARCHAR(100) NULL,
	beschrijving MEDIUMTEXT NULL,
	handleiding LONGTEXT NULL,
	fabrikant VARCHAR(100) NULL,
	PRIMARY KEY (medicijn_nummer)
);

CREATE TABLE Medicijngebruik(
	gebruiker_referentie VARCHAR(100) NOT NULL,
	frequentie VARCHAR(30) NULL,
	dosering VARCHAR(100) NULL,
	toediening_wijze VARCHAR(100) NULL,
	start_datum DATE NULL,
	eind_datum DATE NULL,
	contra_indicaties MEDIUMTEXT NULL,
	type_voorschrift VARCHAR(50) NULL,
	Medicijn_medicijn_nummer INT NOT NULL,
	Medischedossier_md_nummer INT NOT NULL,
	Arts_arts_code INT NOT NULL,
	PRIMARY KEY (gebruiker_referentie),
	INDEX fk_Medicijngebruik_Medicijn1_idx (Medicijn_medicijn_nummer ASC) VISIBLE,
	INDEX fk_Medicijngebruik_Medischedossier1_idx (Medischedossier_md_nummer ASC) VISIBLE,
	INDEX fk_Medicijngebruik_Arts1_idx (Arts_arts_code ASC) VISIBLE,
	CONSTRAINT fk_Medcijngebruik_Medicijn
		FOREIGN KEY (Medicijn_medicijn_nummer)
		REFERENCES Medicijn(medicijn_nummer)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Medicijngebruik_Medischedossier
		FOREIGN KEY (Medischedossier_md_nummer)
		REFERENCES Medischedossier(md_nummer)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Medicijngebruik_Arts
		FOREIGN KEY (Arts_arts_code)
		REFERENCES Arts(arts_code)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Medicijn_heeft_Bijwerking(
	Bijwerking_bijwerking_id INT NOT NULL,
	Medicijn_medicijn_nummer INT NOT NULL,
	PRIMARY KEY (Bijwerking_bijwerking_id, Medicijn_medicijn_nummer),
	INDEX fk_Medicijn_heeft_Bijwerking_Bijwerking1_idx (Bijwerking_bijwerking_id ASC) VISIBLE,
	INDEX fk_Medicijn_heeft_Bijwerking_Medicijn1_idx (Medicijn_medicijn_nummer ASC) VISIBLE,
	CONSTRAINT fk_Medicijn_heeft_Bijwerking_Bijwerking
		FOREIGN KEY (Bijwerking_bijwerking_id)
		REFERENCES Bijwerking(bijwerking_id)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Medicijn_heeft_Bijwerking_Medicijn
		FOREIGN KEY (Medicijn_medicijn_nummer)
		REFERENCES Medicijn(medicijn_nummer)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
); 

CREATE TABLE Afspraak(
	afspraak_referentie VARCHAR(100) NOT NULL,
	datum DATE NULL,
	afspraak_status ENUM("Gepland", "Verlopen") NULL,
	herhaling TINYINT(1) NULL,
	tijdsduur VARCHAR(60) NULL,
	prioriteit ENUM("Hoog", "Gemiddeld", "Laag") NULL,
	herinnering_ingesteld TINYINT(1) NULL,
	annulering_reden TINYTEXT NULL,
	afspraak_type VARCHAR(40) NULL,
	Medischedossier_md_nummer INT NOT NULL,
	PRIMARY KEY (afspraak_referentie),
	INDEX fk_Afspraak_Medischedossier1_idx (Medischedossier_md_nummer ASC) VISIBLE,
	CONSTRAINT fk_Afspraak_Medischedossier
		FOREIGN KEY (Medischedossier_md_nummer)
		REFERENCES Medischedossier(md_nummer)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Behandeling(
	behandeling_nummer VARCHAR(100) NOT NULL,
	behandeling_naam VARCHAR(80) NULL,
	behandeling_datum DATE NULL,
	behandelaar VARCHAR(120) NULL,
	locatie VARCHAR(100) NULL,
	opmerkingen TINYTEXT NULL,
	Medischedossier_md_nummer INT NOT NULL,
	PRIMARY KEY (behandeling_nummer),
	INDEX fk_Behandeling_Medischedossier1_idx (Medischedossier_md_nummer ASC) VISIBLE,
	CONSTRAINT fk_Behandeling_Medischedossier
		FOREIGN KEY (Medischedossier_md_nummer)
		REFERENCES Medischedossier(md_nummer)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Vaccin(
	vaccin_naam VARCHAR(100) NOT NULL,
	vaccin_code VARCHAR(50) NOT NULL,
	opmerkingen VARCHAR(150) NOT NULL,
	PRIMARY KEY (vaccin_naam, vaccin_code, opmerkingen)
);

CREATE TABLE Vaccinatie(
	batch_nummer VARCHAR(120) NOT NULL,
	toediening_datum DATE NULL,
	toediening_plaats VARCHAR(50) NULL,
	herhaling_datum DATE NULL,
	vaccinatie_status ENUM("Niet toegediend", "Toegediend") NULL,
	Medischedossier_md_nummer INT NOT NULL,
	Vaccin_vaccin_naam VARCHAR(100) NOT NULL,
    Vaccin_vaccin_code VARCHAR(50) NOT NULL,
	PRIMARY KEY (batch_nummer),
	INDEX fk_Vaccinatie_Medischedossier1_idx (Medischedossier_md_nummer ASC) VISIBLE,
	INDEX fk_Vaccinatie_Vaccin1_idx (Vaccin_vaccin_naam ASC, Vaccin_vaccin_code ASC) VISIBLE,
	CONSTRAINT fk_Vaccinatie_Medischedossier
		FOREIGN KEY (Medischedossier_md_nummer)
		REFERENCES Medischedossier(md_nummer)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Vaccinatie_Vaccin
		FOREIGN KEY (Vaccin_vaccin_naam, Vaccin_vaccin_code)
		REFERENCES Vaccin(vaccin_naam, vaccin_code)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Geneeswijze(
	naam VARCHAR(150) NOT NULL,
	beschrijving LONGTEXT NULL,
	PRIMARY KEY (naam)
);

CREATE TABLE Vaccin_heeft_Bijwerking(
	Vaccin_vaccin_naam VARCHAR(100) NOT NULL,
	Vaccin_vaccin_code VARCHAR(50) NOT NULL,
	Bijwerking_bijwerking_id INT NOT NULL,
	PRIMARY KEY (Vaccin_vaccin_naam, Vaccin_vaccin_code, Bijwerking_bijwerking_id),
	INDEX fk_Vaccin_heeft_Bijwerking_Bijwerking1_idx (Bijwerking_bijwerking_id ASC) VISIBLE,
	INDEX fk_Vaccin_heeft_Bijwerking_Vaccin1_idx (Vaccin_vaccin_naam ASC, Vaccin_vaccin_code ASC) VISIBLE,
	CONSTRAINT fk_Vaccin_heeft_Bijwerking_Bijwerking
		FOREIGN KEY (Bijwerking_bijwerking_id)
		REFERENCES Bijwerking(bijwerking_id)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Vaccin_heeft_Bijwerking_Vaccin
		FOREIGN	KEY (Vaccin_vaccin_naam, Vaccin_vaccin_code)
		REFERENCES Vaccin(vaccin_naam, vaccin_code)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Ziekte(
	ziekte_id INT NOT NULL AUTO_INCREMENT,
	naam VARCHAR(200) NOT NULL,
	beschrijving LONGTEXT NULL,
	PRIMARY KEY (ziekte_id)
);

CREATE TABLE Ziekte_heeft_Geneeswijze(
	Geneeswijze_naam VARCHAR(150) NOT NULL,
	Ziekte_ziekte_id INT NOT NULL,
	PRIMARY KEY (Geneeswijze_naam, Ziekte_ziekte_id),
	INDEX fk_Geneeswijze_heeft_Ziekte_Ziekte1_idx (Ziekte_ziekte_id ASC) VISIBLE,
	INDEX fk_Geneeswijze_heeft_Ziekte_Geneeswijze1_idx (Geneeswijze_naam ASC) VISIBLE,
	CONSTRAINT fk_Ziekte_heeft_Geneeswijze_Ziekte
		FOREIGN KEY (Ziekte_ziekte_id)
		REFERENCES Ziekte(ziekte_id)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Ziekte_heeft_Geneeswijze_Geneeswijze
		FOREIGN KEY (Geneeswijze_naam)
		REFERENCES Geneeswijze(naam)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Behandeling_heeft_Geneeswijze(
	Behandeling_behandeling_nummer VARCHAR(100) NOT NULL,
	Geneeswijze_naam VARCHAR(150) NOT NULL,
	PRIMARY KEY (Behandeling_behandeling_nummer, Geneeswijze_naam),
	INDEX fk_Behandeling_heeft_Geneeswijze_Geneeswijze1_idx (Geneeswijze_naam ASC) VISIBLE,
	INDEX fk_Behandeling_heeft_Geneeswijze_Behandeling1_idx (Behandeling_behandeling_nummer ASC) VISIBLE,
	CONSTRAINT fk_Behandeling_heeft_Geneeswijze_Geneeswijze
		FOREIGN KEY (Behandeling_behandeling_nummer)
		REFERENCES Behandeling(behandeling_nummer)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Behandeling_heeft_Geneeswijze_Behandeling
		FOREIGN KEY (Geneeswijze_naam)
		REFERENCES Geneeswijze(naam)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Geneeswijze_heeft_Medicijn(
	Geneeswijze_naam VARCHAR(150) NOT NULL,
	Medicijn_medicijn_nummer INT NOT NULL,
	PRIMARY KEY (Geneeswijze_naam, Medicijn_medicijn_nummer),
	INDEX fk_Geneeswijze_heeft_Medicijn_Medicijn1_idx (Medicijn_medicijn_nummer ASC) VISIBLE,
	INDEX fk_Geneeswijze_heeft_Medicijn_Geneeswijze1_idx (Geneeswijze_naam ASC) VISIBLE,
	CONSTRAINT fk_Geneeswijze_heeft_Medicijn_Medicijn
		FOREIGN KEY (Medicijn_medicijn_nummer)
		REFERENCES Medicijn(medicijn_nummer)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Geneeswijze_heeft_Medicijn_Geneeswijze
		FOREIGN KEY (Geneeswijze_naam)
		REFERENCES Geneeswijze(naam)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Onderzoek(
	onderzoek_id INT NOT NULL,
	titel VARCHAR(150) NULL,
	beschrijving LONGTEXT NULL,
	type ENUM("Diagnostisch onderzoek", "Controle") NULL,
	status ENUM("In onderzoek", "Afgerond") NULL,
	Medischedossier_md_nummer INT NOT NULL,
	Arts_arts_code INT NOT NULL,
	PRIMARY KEY (onderzoek_id),
	INDEX fk_Onderzoek_Medischedossier1_id (Medischedossier_md_nummer ASC) VISIBLE,
	INDEX fk_Onderzoek_Arts1_idx (Arts_arts_code ASC) VISIBLE,
	CONSTRAINT fk_Onderzoek_Medischedossier
		FOREIGN KEY (Medischedossier_md_nummer)
		REFERENCES Medischedossier(md_Nummer)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Onderzoek_Arts
		FOREIGN KEY (Arts_arts_code)
		REFERENCES Arts(arts_code)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);


CREATE TABLE Diagnose(
	diagnose_code INT NOT NULL,
	diagnose_naam VARCHAR(100) NULL,
	diagnose_datum DATE NULL,
	diagnose_beschrijving LONGTEXT NULL,
	opmerkingen TINYTEXT NULL,
	diagnose_status ENUM("in afwachting", "voorlopig", "bevestigd", "uitgesloten", "chronisch", "herstellend") NULL,
	Medischedossier_md_nummer INT NOT NULL,
	Arts_arts_code INT NOT NULL,
    PRIMARY KEY (diagnose_code, Medischedossier_md_nummer, Arts_arts_code),
	INDEX fk_Diagnose_Medischedossier1_idx (Medischedossier_md_nummer ASC) VISIBLE,
	INDEX fk_Diagnose_Arts1_idx (Arts_arts_code ASC) VISIBLE,
	CONSTRAINT fk_Diagnose_Medischedossier
		FOREIGN KEY (Medischedossier_md_nummer)
		REFERENCES Medischedossier(md_nummer)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Diagnose_Arts
		FOREIGN KEY (Arts_arts_code)
		REFERENCES Arts(arts_code)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Onderzoek_heeft_Diagnose(
	Onderzoek_onderzoek_id INT NOT NULL,
	Diagnose_diagnose_code INT NOT NULL,
	PRIMARY KEY (Onderzoek_onderzoek_id, Diagnose_diagnose_code),
	INDEX fk_Onderzoek_heeft_Diagnose_Onderzoek1_idx (Onderzoek_onderzoek_id ASC) VISIBLE,
	INDEX fk_Onderzoek_heeft_Diagnose_Diagnose1_idx (Diagnose_diagnose_code ASC) VISIBLE,
	CONSTRAINT fk_Onderzoek_heeft_Diagnose_Onderzoek
		FOREIGN KEY (Onderzoek_onderzoek_id)
		REFERENCES Onderzoek(onderzoek_id)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Onderzoek_heeft_Diagnose_Diagnose
		FOREIGN KEY (Diagnose_diagnose_code)
		REFERENCES Diagnose(diagnose_code)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Diagnose_heeft_Ziekte(
	Ziekte_ziekte_id INT NOT NULL,
	Diagnose_diagnose_code INT NOT NULL,
	PRIMARY KEY (Ziekte_ziekte_id, Diagnose_diagnose_code),
	INDEX fk_Diagnose_heeft_Ziekte_Ziekte1_idx (Ziekte_ziekte_id ASC) VISIBLE,
	INDEX fk_Diagnose_heeft_Ziekte_Diagnose1_idx (Diagnose_diagnose_code ASC) VISIBLE,
	CONSTRAINT fk_Diagnose_heeft_Ziekte_Ziekte
		FOREIGN KEY (Ziekte_ziekte_id)
		REFERENCES Ziekte(ziekte_id)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Diagnose_heeft_Ziekte_Diagnose
		FOREIGN KEY (Diagnose_diagnose_code)
		REFERENCES Diagnose(diagnose_code)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION
);

CREATE TABLE Type_aandoening(
	type_id INT NOT NULL,
	naam VARCHAR(200) NULL,
	PRIMARY KEY (type_id)
);

CREATE TABLE Ziekte_heeft_Type_aandoening(
	Ziekte_ziekte_id INT NOT NULL,
	Type_aandoening_type_id INT NOT NULL,
	PRIMARY KEY (Ziekte_ziekte_id, Type_aandoening_type_id),
	INDEX fk_Ziekte_heeft_Type_aandoening_Type_aandoening1_idx (Type_aandoening_type_id ASC) VISIBLE,
	INDEX fk_Ziekte_heeft_Type_aandoening_Ziekte_Ziekte1_idx (Ziekte_ziekte_id ASC) VISIBLE,
	CONSTRAINT fk_Ziekte_heeft_Type_aandoening_Ziekte
		FOREIGN KEY (Ziekte_ziekte_id)
		REFERENCES Ziekte(ziekte_id)
		ON DELETE RESTRICT
		ON UPDATE NO ACTION,
	CONSTRAINT fk_Ziekte_heeft_Type_aandoening_Type_aandoening
		FOREIGN KEY (Type_aandoening_type_id)
		REFERENCES Type_aandoening(type_id)
		ON DELETE RESTRICT 
		ON UPDATE NO ACTION
);
