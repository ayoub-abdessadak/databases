import worldnames
from data import *
from datetime import timedelta, datetime
from copy import deepcopy
import pandas as pd
import json
import random
import os
from uuid import uuid4

try:
    stored_files = open("files.json", "r")
    files = json.load(stored_files)
    print(os.system(f"rm {' '.join(files['files'])}"))
    print(os.system("ls"))
except:
    pass


def write_line(files: list, value: bool, line: str, current_index: int=None, ending_index: int=None):

    if not value:
        line = f"{line}\n"
    elif value and current_index == ending_index-1:
        line = f"{line};\n"
    else:
        line = f"{line},\n"
    
    for file in files:
        file.writelines(line)

files = []
aantal_personen = 500
aantal_artsen = int((aantal_personen/100) * 15)
aantal_aanmeldingen = int((aantal_personen/100) * 10)
aantal_bewoners = int((aantal_personen/100) * 50)
aantal_zorgverleners = int((aantal_personen/100) * 25)
aantal_personen += 5

print(f"Aantal personen: {aantal_personen}\nAantal artsen: {aantal_artsen}\nAantal aanmeldingen: {aantal_aanmeldingen}\n" +  
        f"Aantal bewoners: {aantal_bewoners}\nAantal zorgverleners:{aantal_zorgverleners}"
)
insertion = open("insertion.sql", "w")

personen = open("personen.sql", "w")
personen_in_memory = []
write_line([insertion, personen], value=False, line="INSERT INTO Persoon (persoon_nummer, voornaam, achternaam, geboortedatum, geslacht)\nVALUES")
for _ in range(aantal_personen):
    dob = datetime.now() - timedelta(days=((worldnames.age()*365)+(random.randint(1, 30))))
    persoon = _, worldnames.first_name(), worldnames.last_name(), dob.strftime("%Y-%m-%d"), random.choice(["Man", "Vrouw"]), worldnames.phone_number(), 
    persoon = tuple([*list(persoon), worldnames.email(persoon[1], persoon[2])])
    id, first_name, last_name, dob, gender, phone, email = persoon 
    personen_in_memory.append(persoon)
    line = f"""({_}, "{first_name}", "{last_name}", "{dob}", "{gender}")"""
    write_line([insertion, personen], value=True, line=line, current_index=_, ending_index=aantal_personen)
personen.close()
files.append("personen.sql")

artsen = open("artsen.sql", "w")
artsen_in_memory = list({random.randint(0, aantal_personen) for _ in range(round(aantal_personen/2))})[0:aantal_artsen]
write_line([insertion, artsen], value=False, line="INSERT INTO Arts (arts_code, Persoon_persoon_nummer)\nVALUES")
for persoon, index in zip(artsen_in_memory, range(aantal_artsen)):
    line = f"({index}, {persoon})"
    write_line([insertion, artsen], value=True, line=line, current_index=index, ending_index=aantal_artsen)
artsen.close()
files.append("artsen.sql")

aanmeldingen = open("aanmeldingen.sql", "w")
aanmeldingen_in_memory = []
write_line([insertion, aanmeldingen], value=False, line="INSERT INTO Aanmelding (aanmeld_nummer, email, telefoon_nummer, Persoon_persoon_nummer)\nVALUES")
_ = 0
for persoon in personen_in_memory:
    if persoon[0] not in artsen_in_memory:
        line = f'({_}, "{persoon[6]}", "{persoon[5]}", {persoon[0]})'
        write_line([insertion, aanmeldingen], value=True, line=line, current_index=_, ending_index=aantal_aanmeldingen)
        aanmeldingen_in_memory.append(persoon[0])
        _ += 1
    if _ >= aantal_aanmeldingen:
        break
aanmeldingen.close()
files.append("aanmeldingen.sql")

bewoners = open("bewoners.sql", "w")
bewoners_in_memory = []
_ = 0
write_line([insertion, bewoners], value=False, line="INSERT INTO Bewoner(code, geboorteplaats, geboorteland, bsn, nationaliteit, overleden, kiesrecht, Persoon_persoon_nummer)\nVALUES")
while _ < aantal_bewoners:
    persoon = personen_in_memory[_]
    if persoon[0] not in artsen_in_memory and persoon[0] not in aanmeldingen_in_memory:
        bsn = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        random.shuffle(bsn)
        bsn = bsn[0:8]
        line = f'({_},  "{random.choice(geboorteplaatsen)}", "{random.choice(migratie_achtergronden_nederland)}", "{''.join(bsn)}", "Nederlandse", 0, 1, {persoon[0]})'
        write_line([insertion, bewoners], value=True, line=line, current_index=_, ending_index=aantal_bewoners)
        bewoners_in_memory.append(persoon)
    _ += 1 
bewoners.close()    
files.append("bewoners.sql")

zorgverleners = open("zorgverleners.sql", "w")
zorgverleners_in_memory = []
_ = 0
write_line([insertion, zorgverleners], value=False, line="INSERT INTO Zorgverlener(big_code, werkervaring, afdeling, dienstverband, start_datum, Persoon_persoon_nummer)\nVALUES")
while _ < aantal_bewoners:
    persoon = personen_in_memory[_]
    if persoon[0] not in artsen_in_memory and persoon[0] not in aanmeldingen_in_memory and persoon[0] not in zorgverleners_in_memory:
        big_code = ["1", "2", "A", "4", "5", "G", "7", "1", "9"]
        random.shuffle(big_code)
        big_code = ''.join(big_code)
        werkervaring = random.choice(werkervaringen)
        line = f"""("{big_code}",  "{werkervaring['Jaren Ervaring']}", "Overal", "{random.choice(["Fulltime", "Part-time", "Nul uren"])}", "2000-10-16", {persoon[0]})"""
        write_line([insertion, zorgverleners], value=True, line=line, current_index=_, ending_index=aantal_bewoners)
        zorgverleners_in_memory.append((big_code, persoon[0]))
    _ += 1 
zorgverleners.close()
files.append("zorgverleners.sql")

specialisaties_file = open("specialisaties.sql", "w")
write_line([insertion, specialisaties_file], value=False, line="INSERT INTO Specialisatie(specialisatie_code, specialisatie_naam, specialisatie_beschrijving)\nVALUES")
for specialisatie, index in zip(specialisaties, range(len(specialisaties))):
    line = f"""({index}, "{specialisatie['Specialisatie']}", "{specialisatie['Beschrijving']}")"""
    write_line([insertion, specialisaties_file], value=True, line=line, current_index=index, ending_index=len(specialisaties))
specialisaties_file.close()
files.append("specialisaties.sql")

team_length = int(len(zorgverleners_in_memory) / len(teams))
teams_in_memory = []
team_file = open("team.sql", "w")
write_line([insertion, team_file], value=False, line="INSERT INTO Team(team_naam, omschrijving, aantal_leden)\nVALUES")
for team, index in zip(teams, range(len(teams))):
    line = f"""("{team['Team_naam'][0:20]}", "{team['Beschrijving']}", {team_length})"""
    write_line([insertion, team_file], value=True, line=line, current_index=index, ending_index=len(teams))
    teams_in_memory.append(team["Team_naam"])
team_file.close()
files.append("team.sql")

zorgverlener_heeft_team_file = open("zorgverlener_heeft_team.sql", "w")
write_line([insertion, zorgverlener_heeft_team_file], value=False, line="INSERT INTO Zorgverlener_heeft_Team(Zorgverlener_big_code, Team_team_naam)\nVALUES")
index = 0
for team, index in zip(teams_in_memory, range(len(team))):
    for _ in range(team_length):
        line = f"""("{zorgverleners_in_memory[index][0]}", "{team}")"""
        write_line([insertion, zorgverlener_heeft_team_file], value=True, line=line, current_index=index, ending_index=len(team))
        index += 1
zorgverlener_heeft_team_file.close()
files.append("zorgverlener_heeft_team.sql")
tz = [zorgverlener[0] for zorgverlener in zorgverleners_in_memory]
zorgverlener_heeft_team_file.close()

zorgverlener_heeft_specialisatie_file = open("zorgverlener_heeft_specialisatie.sql", "w")
write_line([insertion, zorgverlener_heeft_specialisatie_file], value=False, line="INSERT INTO Zorgverlener_heeft_Specialisatie(Zorgverlener_big_code, Specialisatie_specialisatie_code)\nVALUES")
for zorgverlener, index in zip(zorgverleners_in_memory, range(len(zorgverleners_in_memory))):
    specialisaties = [random.randint(0, len(specialisaties)) for _ in range(random.randint(2, 12))]
    specialisaties = set(specialisaties)
    for specialisatie in specialisaties:
        line = f"""("{zorgverlener[0]}", {specialisatie})"""
        write_line([insertion, zorgverlener_heeft_specialisatie_file], value=True, line=line, current_index=index, ending_index=len(zorgverleners_in_memory))
files.append("zorgverlener_heeft_specialisatie.sql")
zorgverlener_heeft_specialisatie_file.close()

medischedossier_file = open("medischedossier.sql", "w")
percentage_rokers = 5
percentage_drinkers = 40
medischedossier_in_memory = []
write_line([insertion, medischedossier_file], value=False, line="INSERT INTO Medischedossier(md_nummer, bloedgroep, rookgedrag, alcoholgedrag, lichamelijke_beperkingen, mentale_gezondheid, verzekering_informatie, Bewoner_code)\nVALUES")
for bewoner, index in zip(bewoners_in_memory, range(len(bewoners_in_memory))):
    mentale_toestand = "Geen bijzonderheden"
    lichamelijke_beperkingen = "Geen lichamelijke beperkingen"
    
    if index <= aantal_bewoners - (100-percentage_rokers)*(aantal_bewoners/100):
        rookgedrag = random.choice(rookgedragingen)
        mentale_toestand = random.choice(mentale_gezondheidsstoornissen)
        lichamelijke_beperkingen = random.choice(lichamelijke_beperkingen)
    else:
        rookgedrag = "Rookt niet"
        
    if index <= aantal_bewoners - (100-percentage_drinkers) * (aantal_bewoners/100):
        alcoholgedrag = random.choice(alcohol_gedragingen)
        mentale_toestand = random.choice(mentale_gezondheidsstoornissen)
        lichamelijke_beperkingen = random.choice(lichamelijke_beperkingen)
    else:
        alcoholgedrag = "Drinkt geen drank"
        
    line = f"""({index}, "{random.choice(bloedgroepen)}", "{rookgedrag}", "{alcoholgedrag}", "{lichamelijke_beperkingen}", "{mentale_toestand}", "{random.choice(zorgverzekeraars)}", {bewoner[0]})"""
    write_line([insertion, medischedossier_file], value=True, line=line, current_index=index, ending_index=len(bewoners_in_memory))
    medischedossier_in_memory.append(index)
medischedossier_file.close()
files.append("medischedossier.sql")

medischedossier_heeft_arts_file = open("medischedossier_heeft_arts.sql", "w")
write_line([insertion, medischedossier_heeft_arts_file], value=False, line="INSERT INTO Medischedossier_heeft_Arts(Medischedossier_md_nummer, Arts_arts_code)\nVALUES")
for medischedossier, index in zip(medischedossier_in_memory, range(len(medischedossier_in_memory))):
    line = f"""({medischedossier}, {random.choice(artsen_in_memory)})"""
    write_line([insertion, medischedossier_heeft_arts_file], value=True, line=line, current_index=index, ending_index=len(medischedossier_in_memory))
medischedossier_heeft_arts_file.close()
files.append("medischedossier_heeft_arts.sql")

medicijn_file = open("medicijn.sql", "w")
medicijn_in_memory = {}
write_line([insertion, medicijn_file], value=False, line="INSERT INTO Medicijn(medicijn_nummer, naam, beschrijving, handleiding, fabrikant)\nVALUES")
for medicijn, index in zip(medicijnen, range(len(medicijnen))):
    line = f"""({index}, "{medicijn['naam']}", "{medicijn['beschrijving']}", "{medicijn['handleiding']}", "{medicijn['fabrikant']}")"""
    write_line([insertion, medicijn_file], value=True, line=line, current_index=index, ending_index=len(medicijnen))
    medicijn_in_memory[medicijn['naam']] = index
medicijn_file.close()
files.append("medicijn.sql")

# Duplicaties in bijwerkingen weghalen 
bijwerkingen_file = open("bijwerkingen.sql", "w")
bijwerkingen_in_memory = []
write_line([insertion, bijwerkingen_file], value=False, line="INSERT INTO Bijwerking(soort, beschrijving_bijwerking)\nVALUES")
for bijwerking, index in zip(bijwerkingen, range(len(bijwerkingen))):
    line = f"""("{bijwerking}", "{bijwerkingen[bijwerking]['beschrijving']}")"""
    write_line([insertion, bijwerkingen_file], value=True, line=line, current_index=index, ending_index=(len(bijwerkingen)))
    bijwerkingen_in_memory.append((index, bijwerking))
bijwerkingen_file.close()
files.append("bijwerkingen.sql")

medicijn_heeft_bijwerking_file = open("medicijn_heeft_bijwerking.sql", "w")
write_line([insertion, medicijn_heeft_bijwerking_file], value=False, line="INSERT INTO Medicijn_heeft_Bijwerking(Bijwerking_bijwerking_id, Medicijn_medicijn_nummer)\nVALUES")
for index, bijwerking in bijwerkingen_in_memory:
    for medicijn in medicijn_in_memory:
        if medicijn in bijwerkingen[bijwerking]['medicijnen']:
            line = f"""({index}, {medicijn_in_memory[medicijn]})"""
            write_line([insertion, medicijn_heeft_bijwerking_file], value=True, line=line, current_index=index, ending_index=len(bijwerkingen_in_memory))
medicijn_heeft_bijwerking_file.close()
files.append("medicijn_heeft_bijwerking.sql")

vaccinaties_file = open("vaccinaties.sql", "w")
vaccinaties_in_memory = []
write_line([insertion, vaccinaties_file], value=False, line="INSERT INTO Vaccinatie(batch_nummer, vaccin_naam, vaccinatie_code, toediening_datum, toediening_plaats, herhaling_datum, vaccinatie_status)\nVALUES")
for vaccin, index in zip(vaccinaties, range(len(vaccinaties))):
    date = datetime.now() - timedelta(days=random.randint(30, 200))
    md_in_memory = deepcopy(medischedossier_in_memory)
    bewoners_length = int((aantal_bewoners/100)*30)
    random.shuffle(md_in_memory)
    for md_nummer in md_in_memory[0:bewoners_length]:
        batch_nummer = uuid4().__str__().replace("-", "")
        line = f"""("{batch_nummer}", {vaccin['vaccin_naam']}", "{vaccin['vaccinatie_code']}", "{date.strftime('%Y-%m%d')}", "{random.choice(geboorteplaatsen)}", "{(date + timedelta(days=60)).strftime('%Y-%m-%d')}", "{random.choice(["Niet toegediend", "Toegediend"])}", {md_nummer})"""
        vaccinaties_in_memory.append(batch_nummer)
        write_line([insertion, vaccinaties_file], value=True, line=line, current_index=index, ending_index=len(vaccinaties))
vaccinaties_file.close()
files.append("vaccinaties.sql")


vaccinatie_heeft_bijwerking_file = open("vaccinatie_heeft_bijwerking.sql", "w")
bijwerkingen_file = open("bijwerkingen.sql", "r")
blines = bijwerkingen_file.readlines()
bijwerkingen_file.close()
bijwerkingen_file = open("bijwerkingen.sql", "w")
bijwerkingen_file.writelines(blines)
vaccinatie_heeft_bijwerking_in_memory = []
bijwerking_bestaat_al = [bijwerking for bijwerking in bijwerkingen]
for bijwerking, index in zip(vaccinatie_bijwerkingen, range(len(vaccinatie_bijwerkingen))):
    if bijwerking['naam'] in bijwerking_bestaat_al:
        continue
    line = f"""("{bijwerking['naam']}", "{bijwerking['beschrijving_bijwerking']}")"""
    write_line([insertion, bijwerkingen_file], value=True, line=line, current_index=index, ending_index=len(vaccinatie_bijwerkingen))

write_line([insertion, vaccinatie_heeft_bijwerking_file], value=False, line="INSERT INTO Vaccinatie_heeft_Bijwerking(Bijwerking_bijwerking_id, Vaccinatie_batch_nummer)\nVALUES")
for batch_nummer, index in zip(vaccinaties_in_memory, range(len(vaccinaties_in_memory))):    
    bijwerkingen = set(random.randint(1, 200) for _ in range(random.randint(10, 40)))
    for bijwerking in bijwerkingen:
        line = f"""({bijwerking}, "{batch_nummer}")"""
        write_line([insertion, vaccinatie_heeft_bijwerking_file], value=True, line=line, current_index=index, ending_index=len(vaccinaties_in_memory))
vaccinatie_heeft_bijwerking_file.close()
bijwerkingen_file.close()
files.append("vaccinatie_heeft_bijwerking.sql")

insertion.close()
stored_files = open("files.json", "w")
json.dump({"files":files}, stored_files)
stored_files.close()