import worldnames
from datetime import timedelta, datetime
import random
import os
from data import *

try:
    print(os.system("rm insertion.sql personen.sql artsen.sql aanmeldingen.sql"))
    print(os.system("ls"))
except:
    pass


def write_line(files: list, value: bool, line: str, current_index: int=None, ending_index: int=None):

    if not value or current_index == ending_index-1:
        line = f"{line}\n"
    else:
        line = f"{line},\n"
    
    for file in files:
        file.writelines(line)


aantal_artsen = 180
aantal_aanmeldingen = 126
aantal_bewoners = 660
aantal_zorgverleners = 301

insertion = open("insertion.sql", "w")
personen = open("personen.sql", "w")
artsen = open("artsen.sql", "w")
aanmeldingen = open("aanmeldingen.sql", "w")
bewoners = open("bewoners.sql", "w")
zorgverleners = open("zorgverleners.sql", "w")

personen_in_memory = []
write_line([insertion, personen], value=False, line="INSERT INTO Persoon (persoon_nummer, voornaam, achternaam, geboortedatum, geslacht)\nVALUES")
for _ in range(1267):
    dob = datetime.now() - timedelta(days=((worldnames.age()*365)+(random.randint(1, 30))))
    persoon = _, worldnames.first_name(), worldnames.last_name(), dob.strftime("%Y-%m-%d"), random.choice(["Man", "Vrouw"]), worldnames.phone_number(), 
    persoon = tuple([*list(persoon), worldnames.email(persoon[1], persoon[2])])
    id, first_name, last_name, dob, gender, phone, email = persoon 
    personen_in_memory.append(persoon)
    line = f"""({_}, "{first_name}", "{last_name}", "{dob}", "{gender}")"""
    write_line([insertion, personen], value=True, line=line, current_index=_, ending_index=1267)


artsen_in_memory = list({random.randint(0, 1267) for _ in range(100)})[0:aantal_artsen]
write_line([insertion, artsen], value=False, line="INSERT INTO Arts (arts_code, Persoon_persoon_nummer)\nVALUES")
for persoon, index in zip(artsen_in_memory, range(aantal_artsen)):
    line = f"({index}, {persoon})"
    write_line([insertion, artsen], value=True, line=line, current_index=index, ending_index=10)

aanmeldingen_in_memory = []
write_line([insertion, aanmeldingen], value=False, line="INSERT INTO Aanmelding (aanmeld_nummer, email, telefoon_nummer, Persoon_persoon_nummer)\nVALUES")
_ = 0
for persoon in personen_in_memory:
    if persoon[0] not in artsen_in_memory:
        line = f'({_}, "{persoon[6]}, "{persoon[5]}", {persoon[0]})'
        write_line([insertion, aanmeldingen], value=True, line=line, current_index=_, ending_index=10)
        aanmeldingen_in_memory.append(persoon[0])
        _ += 1
    if _ >= aantal_aanmeldingen:
        break

bewoners_in_memory = []
_ = 0
write_line([insertion, bewoners], value=False, line="INSERT INTO Bewoner(code, geboorteplaats, geboorteland, bsn, nationaliteit, overleden, kiesrecht, Persoon_persoon_nummer)\nVALUES")
while _ < aantal_bewoners:
    persoon = personen_in_memory[_]
    if persoon[0] not in artsen_in_memory and persoon[0] not in aanmeldingen_in_memory:
        bsn = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        random.shuffle(bsn)
        line = f'({_},  "{random.choice(geboorteplaatsen)}", "{random.choice(migratie_achtergronden_nederland)}", "{''.join(bsn)}", 0, 1 {persoon[0]}")'
        write_line([insertion, bewoners], value=True, line=line, current_index=_, ending_index=aantal_bewoners)
        bewoners_in_memory.append(persoon[0])
    _ += 1 
    
zorgverleners_in_memory = []
_ = 0
write_line([insertion, zorgverleners], value=False, line="INSERT INTO Bewoner(big_code, werkervaring, afdeling, dienstverband, opmerkingen, start_datum, Persoon_persoon_nummer)\nVALUES")
while _ < aantal_bewoners:
    persoon = personen_in_memory[_]
    if persoon[0] not in artsen_in_memory and persoon[0] not in aanmeldingen_in_memory and persoon[0] not in zorgverleners_in_memory:
        big_code = ["1", "2", "A", "4", "5", "G", "7", "1", "9"]
        random.shuffle(big_code)
        line = f'({big_code},  "{random.choice(geboorteplaatsen)}", "{random.choice(migratie_achtergronden_nederland)}", "{''.join(bsn)}", 0, 1 {persoon[0]}")'
        write_line([insertion, zorgverleners], value=True, line=line, current_index=_, ending_index=aantal_bewoners)
        bewoners_in_memory.append(persoon[0])
    _ += 1 

insertion.close()
personen.close()
artsen.close()
aanmeldingen.close()
bewoners.close()