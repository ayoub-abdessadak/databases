import worldnames
from datetime import timedelta, datetime
import random
import os

try:
    print(os.system("rm insertion.sql personen.sql artsen.sql aanmeldingen.sql"))
    print(os.system("ls"))
except:
    pass

personen_in_memory = []

def write_line(files: list, value: bool, line: str, current_index: int=None, ending_index: int=None):

    if not value or current_index == ending_index-1:
        line = f"{line}\n"
    else:
        line = f"{line},\n"
    
    for file in files:
        file.writelines(line)


insertion = open("insertion.sql", "w")
personen = open("personen.sql", "w")
artsen = open("artsen.sql", "w")
aanmeldingen = open("aanmeldingen.sql", "w")
personen_artsen = list({random.randint(0, 1267) for _ in range(100)})[0:10]

write_line([insertion, personen], value=False, line="INSERT INTO Persoon (persoon_nummer, voornaam, achternaam, geboortedatum, geslacht)\nVALUES")

for _ in range(1267):
    dob = datetime.now() - timedelta(days=((worldnames.age()*365)+(random.randint(1, 30))))
    persoon = _, worldnames.first_name(), worldnames.last_name(), dob.strftime("%Y-%m-%d"), random.choice(["Man", "Vrouw"]), worldnames.phone_number(), 
    persoon = tuple([*list(persoon), worldnames.email(persoon[1], persoon[2])])
    id, first_name, last_name, dob, gender, phone, email = persoon 
    personen_in_memory.append(persoon)
    line = f"""({_}, "{first_name}", "{last_name}", "{dob}", "{gender}")"""
    write_line([insertion, personen], value=True, line=line, current_index=_, ending_index=1267)


write_line([insertion, artsen], value=False, line="INSERT INTO Arts (arts_code, Persoon_persoon_nummer)\nVALUES")

for persoon, index in zip(personen_artsen, range(10)):
    line = f"({index}, {persoon})"
    write_line([insertion, artsen], value=True, line=line, current_index=index, ending_index=10)

aanmeldingen_in_memory = []
write_line([insertion, aanmeldingen], value=False, line="INSERT INTO Aanmelding (aanmeld_nummer, email, telefoon_nummer, Persoon_persoon_nummer)\nVALUES")
_ = 0
for persoon in personen_in_memory:
    if persoon[0] not in personen_artsen:
        line = f'({_}, "{persoon[6]}, "{persoon[5]}", {persoon[0]})'
        write_line([insertion, aanmeldingen], value=True, line=line, current_index=_, ending_index=10)
        aanmeldingen_in_memory.append(persoon)
        _ += 1
    if _ >= 10:
        break

insertion.close()
personen.close()
artsen.close()
aanmeldingen.close()