-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Persoon`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Persoon` (
  `persoon_nummer` INT NOT NULL,
  `voornaam` VARCHAR(100) NULL,
  `achternaam` VARCHAR(100) NULL,
  `geboortedatum` DATE NULL,
  `geslacht` ENUM("man", "vrouw") NULL,
  PRIMARY KEY (`persoon_nummer`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Arts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Arts` (
  `arts_code` INT NOT NULL,
  `Persoon_persoon_nummer` INT NOT NULL,
  INDEX `fk_Arts_Persoon_idx` (`Persoon_persoon_nummer` ASC) VISIBLE,
  PRIMARY KEY (`arts_code`),
  CONSTRAINT `fk_Arts_Persoon`
    FOREIGN KEY (`Persoon_persoon_nummer`)
    REFERENCES `mydb`.`Persoon` (`persoon_nummer`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Aanmelding`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Aanmelding` (
  `aanmeld_nummer` VARCHAR(20) NOT NULL,
  `email` VARCHAR(200) NULL,
  `telefoon_nummer` VARCHAR(20) NULL,
  `Persoon_persoon_nummer` INT NOT NULL,
  PRIMARY KEY (`aanmeld_nummer`),
  INDEX `fk_Aanmelding_Persoon1_idx` (`Persoon_persoon_nummer` ASC) VISIBLE,
  CONSTRAINT `fk_Aanmelding_Persoon1`
    FOREIGN KEY (`Persoon_persoon_nummer`)
    REFERENCES `mydb`.`Persoon` (`persoon_nummer`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Bewoner`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Bewoner` (
  `code` INT NOT NULL,
  `geboorteplaats` VARCHAR(50) NULL,
  `geboorteland` VARCHAR(85) NULL,
  `bsn` CHAR(9) NULL,
  `nationaliteit` VARCHAR(85) NULL,
  `overleden` TINYINT(1) NULL,
  `kiesrecht` TINYINT(1) NULL,
  `Persoon_persoon_nummer` INT NOT NULL,
  PRIMARY KEY (`code`),
  INDEX `fk_Bewoner_Persoon1_idx` (`Persoon_persoon_nummer` ASC) VISIBLE,
  CONSTRAINT `fk_Bewoner_Persoon1`
    FOREIGN KEY (`Persoon_persoon_nummer`)
    REFERENCES `mydb`.`Persoon` (`persoon_nummer`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Medischedossier`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Medischedossier` (
  `md_nummer` INT NOT NULL,
  `aandachtspunten` TINYTEXT NULL,
  `specialist_id` VARCHAR(50) NULL,
  `bloedgroep` VARCHAR(25) NULL,
  `rookgedrag` TINYTEXT NULL,
  `alcoholgedrag` TINYTEXT NULL,
  `lichamelijke_beperkingen` TINYTEXT NULL,
  `mentale_gezondheid` TINYTEXT NULL,
  `famillie_geschiedenis` MEDIUMTEXT NULL,
  `verzekering_informatie` MEDIUMTEXT NULL,
  `Bewoner_code` INT NOT NULL,
  PRIMARY KEY (`md_nummer`),
  INDEX `fk_Medischedossier_Bewoner1_idx` (`Bewoner_code` ASC) VISIBLE,
  CONSTRAINT `fk_Medischedossier_Bewoner1`
    FOREIGN KEY (`Bewoner_code`)
    REFERENCES `mydb`.`Bewoner` (`code`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Medischedossier_heeft_Arts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Medischedossier_heeft_Arts` (
  `Medischedossier_md_nummer` INT NOT NULL,
  `Arts_arts_code` INT NOT NULL,
  PRIMARY KEY (`Medischedossier_md_nummer`, `Arts_arts_code`),
  INDEX `fk_Medischedossier_heeft_Arts_Medischedossier1_idx` (`Medischedossier_md_nummer` ASC) VISIBLE,
  INDEX `fk_Medischedossier_heeft_Arts_Arts1_idx` (`Arts_arts_code` ASC) VISIBLE,
  CONSTRAINT `fk_Medischedossier_heeft_Arts_Medischedossier1`
    FOREIGN KEY (`Medischedossier_md_nummer`)
    REFERENCES `mydb`.`Medischedossier` (`md_nummer`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Medischedossier_heeft_Arts_Arts1`
    FOREIGN KEY (`Arts_arts_code`)
    REFERENCES `mydb`.`Arts` (`arts_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Activiteit`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Activiteit` (
  `activiteit_naam` VARCHAR(100) NOT NULL,
  `datum` DATE NOT NULL,
  `locatie` VARCHAR(150) NOT NULL,
  `categorie` VARCHAR(40) NULL,
  `activiteit_beschrijving` MEDIUMTEXT NULL,
  `duur` VARCHAR(32) NULL,
  `activiteit_status` ENUM("binnenkort", "bezig", "beëndigd") NULL,
  PRIMARY KEY (`activiteit_naam`, `datum`, `locatie`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Bewoner_bezoekt_Activiteit`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Bewoner_bezoekt_Activiteit` (
  `Bewoner_code` INT NOT NULL,
  `Activiteit_activiteit_naam` VARCHAR(100) NOT NULL,
  `Activiteit_datum` DATE NOT NULL,
  `Activiteit_locatie` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`Bewoner_code`, `Activiteit_activiteit_naam`, `Activiteit_datum`, `Activiteit_locatie`),
  INDEX `fk_Bewoner_bezoekt_Activiteit_Activiteit1_idx` (`Activiteit_activiteit_naam` ASC, `Activiteit_datum` ASC, `Activiteit_locatie` ASC) VISIBLE,
  CONSTRAINT `fk_Activiteit_has_Bewoner_Bewoner1`
    FOREIGN KEY (`Bewoner_code`)
    REFERENCES `mydb`.`Bewoner` (`code`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Bewoner_bezoekt_Activiteit_Activiteit1`
    FOREIGN KEY (`Activiteit_activiteit_naam` , `Activiteit_datum` , `Activiteit_locatie`)
    REFERENCES `mydb`.`Activiteit` (`activiteit_naam` , `datum` , `locatie`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Zorgplan`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Zorgplan` (
  `referentie_nummer` INT NOT NULL,
  `opstelling_datum` DATE NULL,
  `herziening_datum` DATE NULL,
  `zorg_doelen` MEDIUMTEXT NULL,
  `zorg_type` VARCHAR(50) NULL,
  `behandel_plan` MEDIUMTEXT NULL,
  `frequentie_zorg` VARCHAR(20) NULL,
  `specifieke_instructies` MEDIUMTEXT NULL,
  `zorgplan_status` ENUM("open", "wordt uitgevoerd") NULL,
  `opmerkingen` MEDIUMTEXT NULL,
  `Bewoner_code` INT NOT NULL,
  PRIMARY KEY (`referentie_nummer`, `Bewoner_code`),
  INDEX `fk_Zorgplan_Bewoner1_idx` (`Bewoner_code` ASC) VISIBLE,
  CONSTRAINT `fk_Zorgplan_Bewoner1`
    FOREIGN KEY (`Bewoner_code`)
    REFERENCES `mydb`.`Bewoner` (`code`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Zorgbehoefte`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Zorgbehoefte` (
  `zb_code` INT NOT NULL,
  `zb_categorie` VARCHAR(40) NULL,
  `zb_naam` VARCHAR(50) NULL,
  `zb_beschrijving` MEDIUMTEXT NULL,
  `urgentie` TINYINT(1) NULL,
  PRIMARY KEY (`zb_code`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Bewoner_heeft_Zorgbehoefte`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Bewoner_heeft_Zorgbehoefte` (
  `Zorgbehoefte_zb_code` INT NOT NULL,
  `Bewoner_code` INT NOT NULL,
  PRIMARY KEY (`Zorgbehoefte_zb_code`, `Bewoner_code`),
  INDEX `fk_Zorgbehoefte_has_Bewoner_Bewoner1_idx` (`Bewoner_code` ASC) VISIBLE,
  INDEX `fk_Zorgbehoefte_has_Bewoner_Zorgbehoefte1_idx` (`Zorgbehoefte_zb_code` ASC) VISIBLE,
  CONSTRAINT `fk_Zorgbehoefte_has_Bewoner_Zorgbehoefte1`
    FOREIGN KEY (`Zorgbehoefte_zb_code`)
    REFERENCES `mydb`.`Zorgbehoefte` (`zb_code`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Zorgbehoefte_has_Bewoner_Bewoner1`
    FOREIGN KEY (`Bewoner_code`)
    REFERENCES `mydb`.`Bewoner` (`code`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Zorgverlener`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Zorgverlener` (
  `big_code` VARCHAR(20) NOT NULL,
  `werkervaring` VARCHAR(40) NULL,
  `afdeling` VARCHAR(80) NULL,
  `dienstverband` VARCHAR(30) NULL,
  `opmerkingen` TINYTEXT NULL,
  `start_datum` DATE NULL,
  `Persoon_persoon_nummer` INT NOT NULL,
  PRIMARY KEY (`big_code`),
  INDEX `fk_Zorgverlener_Persoon1_idx` (`Persoon_persoon_nummer` ASC) VISIBLE,
  CONSTRAINT `fk_Zorgverlener_Persoon1`
    FOREIGN KEY (`Persoon_persoon_nummer`)
    REFERENCES `mydb`.`Persoon` (`persoon_nummer`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Bewoner_heeft_zorgverlener`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Bewoner_heeft_zorgverlener` (
  `Zorgverlener_big_code` VARCHAR(20) NOT NULL,
  `Bewoner_code` INT NOT NULL,
  PRIMARY KEY (`Zorgverlener_big_code`, `Bewoner_code`),
  INDEX `fk_Zorgverlener_has_Bewoner_Bewoner1_idx` (`Bewoner_code` ASC) VISIBLE,
  INDEX `fk_Zorgverlener_has_Bewoner_Zorgverlener1_idx` (`Zorgverlener_big_code` ASC) VISIBLE,
  CONSTRAINT `fk_Zorgverlener_has_Bewoner_Zorgverlener1`
    FOREIGN KEY (`Zorgverlener_big_code`)
    REFERENCES `mydb`.`Zorgverlener` (`big_code`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Zorgverlener_has_Bewoner_Bewoner1`
    FOREIGN KEY (`Bewoner_code`)
    REFERENCES `mydb`.`Bewoner` (`code`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Specialisatie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Specialisatie` (
  `specialisatie_code` INT NOT NULL,
  `specialisatie_naam` VARCHAR(100) NULL,
  `specialisatie_beschrijving` MEDIUMTEXT NULL,
  PRIMARY KEY (`specialisatie_code`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Team`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Team` (
  `team_naam` VARCHAR(20) NOT NULL,
  `omschrijving` TINYTEXT NULL,
  `aantal_leden` INT NULL,
  PRIMARY KEY (`team_naam`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Zorgverlener_heeft_Team`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Zorgverlener_heeft_Team` (
  `Zorgverlener_big_code` VARCHAR(20) NOT NULL,
  `Team_team_naam` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`Zorgverlener_big_code`, `Team_team_naam`),
  INDEX `fk_Zorgverlener_has_Team_Team1_idx` (`Team_team_naam` ASC) VISIBLE,
  INDEX `fk_Zorgverlener_has_Team_Zorgverlener1_idx` (`Zorgverlener_big_code` ASC) VISIBLE,
  CONSTRAINT `fk_Zorgverlener_has_Team_Zorgverlener1`
    FOREIGN KEY (`Zorgverlener_big_code`)
    REFERENCES `mydb`.`Zorgverlener` (`big_code`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Zorgverlener_has_Team_Team1`
    FOREIGN KEY (`Team_team_naam`)
    REFERENCES `mydb`.`Team` (`team_naam`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Zorgverlener_heeft_Specialisatie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Zorgverlener_heeft_Specialisatie` (
  `Zorgverlener_big_code` VARCHAR(20) NOT NULL,
  `Specialisatie_specialisatie_code` INT NOT NULL,
  PRIMARY KEY (`Zorgverlener_big_code`, `Specialisatie_specialisatie_code`),
  INDEX `fk_Zorgverlener_has_Specialisatie_Specialisatie1_idx` (`Specialisatie_specialisatie_code` ASC) VISIBLE,
  INDEX `fk_Zorgverlener_has_Specialisatie_Zorgverlener1_idx` (`Zorgverlener_big_code` ASC) VISIBLE,
  CONSTRAINT `fk_Zorgverlener_has_Specialisatie_Zorgverlener1`
    FOREIGN KEY (`Zorgverlener_big_code`)
    REFERENCES `mydb`.`Zorgverlener` (`big_code`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Zorgverlener_has_Specialisatie_Specialisatie1`
    FOREIGN KEY (`Specialisatie_specialisatie_code`)
    REFERENCES `mydb`.`Specialisatie` (`specialisatie_code`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Medicijn`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Medicijn` (
  `medicijn_nummer` INT NOT NULL,
  `naam` VARCHAR(100) NULL,
  `beschrijving` MEDIUMTEXT NULL,
  `handleiding` LONGTEXT NULL,
  `fabrikant` VARCHAR(100) NULL,
  PRIMARY KEY (`medicijn_nummer`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Medicijngebruik`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Medicijngebruik` (
  `gebruiker_referentie` VARCHAR(100) NOT NULL,
  `frequentie` VARCHAR(30) NULL,
  `dosering` VARCHAR(100) NULL,
  `toediening_wijze` MEDIUMTEXT NULL,
  `start_datum` DATE NULL,
  `eind_datum` DATE NULL,
  `contra_indicaties` MEDIUMTEXT NULL,
  `type_voorschrift` VARCHAR(50) NULL,
  `Medicijn_medicijn_nummer` INT NOT NULL,
  `Medischedossier_md_nummer` INT NOT NULL,
  `Arts_arts_code` INT NOT NULL,
  PRIMARY KEY (`gebruiker_referentie`),
  INDEX `fk_Medicijngebruik_Medicijn1_idx` (`Medicijn_medicijn_nummer` ASC) VISIBLE,
  INDEX `fk_Medicijngebruik_Medischedossier1_idx` (`Medischedossier_md_nummer` ASC) VISIBLE,
  INDEX `fk_Medicijngebruik_Arts1_idx` (`Arts_arts_code` ASC) VISIBLE,
  CONSTRAINT `fk_Medicijngebruik_Medicijn1`
    FOREIGN KEY (`Medicijn_medicijn_nummer`)
    REFERENCES `mydb`.`Medicijn` (`medicijn_nummer`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Medicijngebruik_Medischedossier1`
    FOREIGN KEY (`Medischedossier_md_nummer`)
    REFERENCES `mydb`.`Medischedossier` (`md_nummer`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Medicijngebruik_Arts1`
    FOREIGN KEY (`Arts_arts_code`)
    REFERENCES `mydb`.`Arts` (`arts_code`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Afspraak`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Afspraak` (
  `afspraak_referentie` VARCHAR(100) NOT NULL,
  `datum` DATE NULL,
  `locatie` VARCHAR(150) NULL,
  `omschrijving` MEDIUMTEXT NULL,
  `vervoer` VARCHAR(100) NULL,
  `afspraak_status` ENUM("Gepland", "Verlopen") NULL,
  `herhaling` TINYINT(1) NULL,
  `tijdsduur` VARCHAR(60) NULL,
  `prioriteit` ENUM("Hoog", "Gemiddeld", "Laag") NULL,
  `herinnering_ingesteld` TINYINT(1) NULL,
  `annulering_reden` TINYTEXT NULL,
  `afspraak_type` VARCHAR(40) NULL,
  `Medischedossier_md_nummer` INT NOT NULL,
  PRIMARY KEY (`afspraak_referentie`),
  INDEX `fk_Afspraak_Medischedossier1_idx` (`Medischedossier_md_nummer` ASC) VISIBLE,
  CONSTRAINT `fk_Afspraak_Medischedossier1`
    FOREIGN KEY (`Medischedossier_md_nummer`)
    REFERENCES `mydb`.`Medischedossier` (`md_nummer`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Behandeling`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Behandeling` (
  `behandeling_nummer` VARCHAR(100) NOT NULL,
  `behandeling_naam` VARCHAR(80) NULL,
  `behandeling_datum` DATE NULL,
  `behandelaar` VARCHAR(120) NULL,
  `locatie` VARCHAR(100) NULL,
  `opmerkingen` TINYTEXT NULL,
  `Medischedossier_md_nummer` INT NOT NULL,
  PRIMARY KEY (`behandeling_nummer`),
  INDEX `fk_Behandeling_Medischedossier1_idx` (`Medischedossier_md_nummer` ASC) VISIBLE,
  CONSTRAINT `fk_Behandeling_Medischedossier1`
    FOREIGN KEY (`Medischedossier_md_nummer`)
    REFERENCES `mydb`.`Medischedossier` (`md_nummer`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Vaccinatie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Vaccinatie` (
  `batch_nummer` VARCHAR(120) NOT NULL,
  `vaccin_naam` VARCHAR(100) NULL,
  `vaccinatie_code` VARCHAR(50) NULL,
  `toediening_datum` DATE NULL,
  `toediening_plaats` VARCHAR(50) NULL,
  `herhaling_datum` DATE NULL,
  `opmerkingen` TINYTEXT NULL,
  `vaccinatie_status` ENUM("Niet toegediend", "Toegediend") NULL,
  `Medischedossier_md_nummer` INT NOT NULL,
  PRIMARY KEY (`batch_nummer`, `Medischedossier_md_nummer`),
  INDEX `fk_Vaccinatie_Medischedossier1_idx` (`Medischedossier_md_nummer` ASC) VISIBLE,
  CONSTRAINT `fk_Vaccinatie_Medischedossier1`
    FOREIGN KEY (`Medischedossier_md_nummer`)
    REFERENCES `mydb`.`Medischedossier` (`md_nummer`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Bijwerking`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Bijwerking` (
  `bijwerking_id` INT NOT NULL,
  `soort` VARCHAR(120) NULL,
  `beschrijving_bijwerking` LONGTEXT NULL,
  PRIMARY KEY (`bijwerking_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Vaccinatie_heeft_bijwerking`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Vaccinatie_heeft_bijwerking` (
  `Bijwerking_bijwerking_id` INT NOT NULL,
  `Vaccinatie_batch_nummer` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Bijwerking_bijwerking_id`, `Vaccinatie_batch_nummer`),
  INDEX `fk_Bijwerking_has_Vaccinatie_Vaccinatie1_idx` (`Vaccinatie_batch_nummer` ASC) VISIBLE,
  INDEX `fk_Bijwerking_has_Vaccinatie_Bijwerking1_idx` (`Bijwerking_bijwerking_id` ASC) VISIBLE,
  CONSTRAINT `fk_Bijwerking_has_Vaccinatie_Bijwerking1`
    FOREIGN KEY (`Bijwerking_bijwerking_id`)
    REFERENCES `mydb`.`Bijwerking` (`bijwerking_id`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Bijwerking_has_Vaccinatie_Vaccinatie1`
    FOREIGN KEY (`Vaccinatie_batch_nummer`)
    REFERENCES `mydb`.`Vaccinatie` (`batch_nummer`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Medicijn_heeft_bijwerking`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Medicijn_heeft_bijwerking` (
  `Bijwerking_bijwerking_id` INT NOT NULL,
  `Medicijn_medicijn_nummer` INT NOT NULL,
  PRIMARY KEY (`Bijwerking_bijwerking_id`, `Medicijn_medicijn_nummer`),
  INDEX `fk_Bijwerking_has_Medicijn_Medicijn1_idx` (`Medicijn_medicijn_nummer` ASC) VISIBLE,
  INDEX `fk_Bijwerking_has_Medicijn_Bijwerking1_idx` (`Bijwerking_bijwerking_id` ASC) VISIBLE,
  CONSTRAINT `fk_Bijwerking_has_Medicijn_Bijwerking1`
    FOREIGN KEY (`Bijwerking_bijwerking_id`)
    REFERENCES `mydb`.`Bijwerking` (`bijwerking_id`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Bijwerking_has_Medicijn_Medicijn1`
    FOREIGN KEY (`Medicijn_medicijn_nummer`)
    REFERENCES `mydb`.`Medicijn` (`medicijn_nummer`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Diagnose`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Diagnose` (
  `diagnose_code` INT NOT NULL,
  `diagnose_naam` VARCHAR(100) NULL,
  `diagnose_datum` DATE NULL,
  `diagnose_beschrijving` LONGTEXT NULL,
  `opmerkingen` TINYTEXT NULL,
  `diagnose_status` ENUM("in afwachting", "voorlopig", "bevestigd", "uitgesloten", "chronisch", "herstellend", "onbekend") NULL,
  `Medischedossier_md_nummer` INT NOT NULL,
  `Arts_arts_code` INT NOT NULL,
  PRIMARY KEY (`diagnose_code`, `Medischedossier_md_nummer`, `Arts_arts_code`),
  INDEX `fk_Diagnose_Medischedossier1_idx` (`Medischedossier_md_nummer` ASC) VISIBLE,
  INDEX `fk_Diagnose_Arts1_idx` (`Arts_arts_code` ASC) VISIBLE,
  CONSTRAINT `fk_Diagnose_Medischedossier1`
    FOREIGN KEY (`Medischedossier_md_nummer`)
    REFERENCES `mydb`.`Medischedossier` (`md_nummer`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Diagnose_Arts1`
    FOREIGN KEY (`Arts_arts_code`)
    REFERENCES `mydb`.`Arts` (`arts_code`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
