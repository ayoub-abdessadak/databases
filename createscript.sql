SELECT 
    TABLE_NAME AS Tabel, 
    COLUMN_NAME AS Kolom, 
    COLUMN_TYPE AS Type, 
    IS_NULLABLE AS Mag_Null, 
    COLUMN_KEY AS Sleutel, 
    EXTRA AS Extra_Opties, 
    COLUMN_DEFAULT AS Standaardwaarde 
FROM 
    INFORMATION_SCHEMA.COLUMNS
WHERE 
    TABLE_SCHEMA = 'mydb'
ORDER BY 
    TABLE_NAME, ORDINAL_POSITION;
