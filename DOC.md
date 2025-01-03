# SQL Queries Verzorgingcentrum


Deze query doet iets, de query werkt als volgt, de query vertoont

**SQL query**
```sql
DESCRIBE Medicijn;
```
**MySQL Returns**
```bash
+-----------------+--------------+------+-----+---------+-------+
| Field           | Type         | Null | Key | Default | Extra |
+-----------------+--------------+------+-----+---------+-------+
| medicijn_nummer | int          | NO   | PRI | NULL    |       |
| naam            | varchar(100) | YES  |     | NULL    |       |
| beschrijving    | mediumtext   | YES  |     | NULL    |       |
| handleiding     | longtext     | YES  |     | NULL    |       |
| fabrikant       | varchar(100) | YES  |     | NULL    |       |
+-----------------+--------------+------+-----+---------+-------+
5 rows in set (0,00 sec)
```



