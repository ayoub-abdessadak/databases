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
