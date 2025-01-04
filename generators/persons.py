import worldnames
from data import *
from datetime import timedelta, datetime
from copy import deepcopy
import pandas as pd
import json
import random
import os
from uuid import uuid4
from faker import Faker
import time
import sys
from zorgplan import zorgplan

start = time.time()

faker = Faker("nl_NL")

try:
    stored_files = open("files.json", "r")
    files = json.load(stored_files)
    print(os.system(f"rm {' '.join(files['files'])}"))
    print(os.system("ls"))
except:
    pass


def write_line(files: list, value: bool, line: str, current_index: int=None, ending_index: int=None, nested_index=False):

    print(current_index, ending_index, nested_index, value)
    if not value:
        line = f"{line}\n"
    elif value and current_index == ending_index-1 and not nested_index:
        line = f"{line};\n"
    else:
        line = f"{line},\n"
    print(line)
    for file in files:
        file.writelines(line)

files = []
aantal_personen = 9_147
aantal_artsen = int((aantal_personen/100) * 15)
aantal_aanmeldingen = int((aantal_personen/100) * 10)
aantal_bewoners = int((aantal_personen/100) * 50)
aantal_zorgverleners = int((aantal_personen/100) * 25)
aantal_personen += 5
if aantal_bewoners < 20:
    sys.exit()

print(f"Aantal personen: {aantal_personen}\nAantal artsen: {aantal_artsen}\nAantal aanmeldingen: {aantal_aanmeldingen}\n" +  
        f"Aantal bewoners: {aantal_bewoners}\nAantal zorgverleners:{aantal_zorgverleners}"
)
insertion = open("insertion.sql", "w")

personen = open("personen.sql", "w")
personen_in_memory = []
write_line([insertion, personen], value=False, line="INSERT INTO Persoon(persoon_nummer, voornaam, achternaam, geboortedatum, geslacht)\nVALUES")
for _ in range(aantal_personen):
    dob = datetime.now() - timedelta(days=((worldnames.age()*365)+(random.randint(1, 30))))
    persoon = _, random.choice([worldnames.first_name, faker.first_name])(), faker.last_name(), dob.strftime("%Y-%m-%d"), random.choice(["Man", "Vrouw"]), worldnames.phone_number(), 
    persoon = tuple([*list(persoon), worldnames.email(persoon[1], persoon[2])])
    id, first_name, last_name, dob, gender, phone, email = persoon 
    personen_in_memory.append(persoon)
    line = f"""({_}, "{first_name}", "{last_name}", "{dob}", "{gender}")"""
    write_line([insertion, personen], value=True, line=line, current_index=_, ending_index=aantal_personen)
personen.close()
files.append("personen.sql")

artsen = open("artsen.sql", "w")
artsen_in_memory = deepcopy(personen_in_memory)
random.shuffle(artsen_in_memory)
_artsen_in_memory = [arts[0] for arts in artsen_in_memory[0:aantal_artsen]]
artsen_in_memory = []
write_line([insertion, artsen], value=False, line="INSERT INTO Arts (arts_code, Persoon_persoon_nummer)\nVALUES")
for persoon, index in zip(_artsen_in_memory, range(aantal_artsen)):
    line = f"({index}, {persoon})"
    write_line([insertion, artsen], value=True, line=line, current_index=index, ending_index=aantal_artsen)
    artsen_in_memory.append(index)
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
prep_bewoners = [persoon for persoon in personen_in_memory if persoon[0] not in artsen_in_memory and persoon[0] not in aanmeldingen_in_memory]
write_line([insertion, bewoners], value=False, line="INSERT INTO Bewoner(code, geboorteplaats, geboorteland, bsn, nationaliteit, overleden, kiesrecht, Persoon_persoon_nummer)\nVALUES")
for index, _bewoner in zip(range(len(prep_bewoners)), prep_bewoners):
    if _ >= aantal_bewoners:
        break
    persoon = _bewoner
    bsn = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    random.shuffle(bsn)
    bsn = bsn[0:8]
    bsn = ''.join(bsn)
    line = f'({index}, "{random.choice(geboorteplaatsen)}", "{random.choice(migratie_achtergronden_nederland)}", "{bsn}", "Nederlandse", 0, 1, {persoon[0]})'
    write_line([insertion, bewoners], value=True, line=line, current_index=_, ending_index=aantal_bewoners)
    bewoners_in_memory.append(index)
    _ += 1
bewoners.close()    
files.append("bewoners.sql")

def gen_big_code():
    big_code = ["1", "2", "A", "4", "5", "G", "7", "1", "9"]
    random.shuffle(big_code)
    big_code = ''.join(big_code)
    return big_code

zorgverleners = open("zorgverleners.sql", "w")
zorgverleners_in_memory = []
big_codes = []
_ = 0
prep_zorgverleners = [persoon for persoon in personen_in_memory if persoon[0] not in artsen_in_memory and persoon[0] not in aanmeldingen_in_memory and persoon[0] not in bewoners_in_memory]
write_line([insertion, zorgverleners], value=False, line="INSERT INTO Zorgverlener(big_code, werkervaring, afdeling, dienstverband, start_datum, Persoon_persoon_nummer)\nVALUES")
for index, _zorgverlener in zip(range(len(prep_zorgverleners)), prep_zorgverleners):
    if _ >= aantal_zorgverleners:
        break
    persoon = _zorgverlener
    big_code = uuid4().__str__()[0:20]
    werkervaring = random.choice(werkervaringen)
    line = f"""("{big_code}",  "{werkervaring['Jaren Ervaring']}", "Overal", "{random.choice(["Fulltime", "Part-time", "Nul uren"])}", "2000-10-16", {persoon[0]})"""
    write_line([insertion, zorgverleners], value=True, line=line, current_index=_, ending_index=aantal_zorgverleners)
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
    line = f"""("{team['Team_naam']}", "{team['Beschrijving']}", {team_length})"""
    write_line([insertion, team_file], value=True, line=line, current_index=index, ending_index=len(teams))
    teams_in_memory.append(team["Team_naam"])
team_file.close()
files.append("team.sql")

zorgverlener_heeft_team_file = open("zorgverlener_heeft_team.sql", "w")
write_line([insertion, zorgverlener_heeft_team_file], value=False, line="INSERT INTO Zorgverlener_heeft_Team(Zorgverlener_big_code, Team_team_naam)\nVALUES")
index = 0
czorgverleners_in_memory = deepcopy(zorgverleners_in_memory)
for team, index in zip(teams_in_memory, range(len(teams_in_memory))):
    random.shuffle(czorgverleners_in_memory)
    for _ in range(team_length):
        line = f"""("{czorgverleners_in_memory[_][0]}", "{team}")"""
        write_line([insertion, zorgverlener_heeft_team_file], value=True, line=line, current_index=index, ending_index=len(teams_in_memory), nested_index=not (_ == team_length-1))
zorgverlener_heeft_team_file.close()
files.append("zorgverlener_heeft_team.sql")
tz = [zorgverlener[0] for zorgverlener in zorgverleners_in_memory]
zorgverlener_heeft_team_file.close()

zorgverlener_heeft_specialisatie_file = open("zorgverlener_heeft_specialisatie.sql", "w")
write_line([insertion, zorgverlener_heeft_specialisatie_file], value=False, line="INSERT INTO Zorgverlener_heeft_Specialisatie(Zorgverlener_big_code, Specialisatie_specialisatie_code)\nVALUES")
for zorgverlener, index in zip(zorgverleners_in_memory, range(len(zorgverleners_in_memory))):
    specialisaties = [random.randint(0, len(specialisaties)) for _ in range(random.randint(2, 12))]
    specialisaties = list(set(specialisaties))
    for specialisatie in specialisaties:
        line = f"""("{zorgverlener[0]}", {specialisatie})"""
        write_line([insertion, zorgverlener_heeft_specialisatie_file], value=True, line=line, current_index=index, ending_index=len(zorgverleners_in_memory), nested_index=not (specialisatie == specialisaties[-1]))
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
        
    line = f"""({index}, "{random.choice(bloedgroepen)}", "{rookgedrag}", "{alcoholgedrag}", "{lichamelijke_beperkingen}", "{mentale_toestand}", "{random.choice(zorgverzekeraars)}", {bewoner})"""
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
    write_line([insertion, bijwerkingen_file], value=True, line=line, current_index=index, ending_index=len(bijwerkingen), nested_index=True)
    bijwerkingen_in_memory.append((index, bijwerking))
    
bijwerking_bestaat_al = [bijwerking for bijwerking in bijwerkingen]
for bijwerking, index in zip(vaccinatie_bijwerkingen, range(len(vaccinatie_bijwerkingen))):
    if bijwerking['naam'] in bijwerking_bestaat_al:
        continue
    line = f"""("{bijwerking['naam']}", "{bijwerking['beschrijving_bijwerking']}")"""
    write_line([insertion, bijwerkingen_file], value=True, line=line, current_index=index, ending_index=50)
    bijwerking_bestaat_al.append(bijwerking['naam'])
bijwerkingen_file.close()
files.append("bijwerkingen.sql")

medicijn_heeft_bijwerking_file = open("medicijn_heeft_bijwerking.sql", "w")
write_line([insertion, medicijn_heeft_bijwerking_file], value=False, line="INSERT INTO Medicijn_heeft_Bijwerking(Bijwerking_bijwerking_id, Medicijn_medicijn_nummer)\nVALUES")
for index, bijwerking in bijwerkingen_in_memory:
    for medicijn in medicijn_in_memory:
        if medicijn in bijwerkingen[bijwerking]['medicijnen']:
            line = f"""({index+1}, {medicijn_in_memory[medicijn]})"""
            write_line([insertion, medicijn_heeft_bijwerking_file], value=True, line=line, current_index=index, ending_index=len(bijwerkingen_in_memory), nested_index=not (medicijn == bijwerkingen[bijwerking]['medicijnen'][-1]))
medicijn_heeft_bijwerking_file.close()
files.append("medicijn_heeft_bijwerking.sql")

vaccin_file = open("vaccin.sql", "w")
vaccin_in_memory = []
vaccin_bestaat_al = []
write_line([insertion, vaccin_file], value=False, line="INSERT INTO Vaccin(vaccin_naam, vaccin_code, opmerkingen)\nVALUES")
for vaccin, index in zip(vaccinaties, range(len(vaccinaties))):
    if vaccin['vaccin_naam'] not in vaccin_bestaat_al:
        line = f"""("{vaccin['vaccin_naam']}", "{vaccin['vaccinatie_code']}", "{vaccin['opmerkingen']}")"""
        write_line([insertion, vaccin_file], value=True, line=line, current_index=index, ending_index=45)
        vaccin_in_memory.append((vaccin['vaccin_naam'], vaccin['vaccinatie_code']))
        vaccin_bestaat_al.append(vaccin['vaccin_naam'])
vaccin_file.close()
files.append("vaccin.sql")

vaccinaties_file = open("vaccinaties.sql", "w")
vaccinaties_in_memory = []
write_line([insertion, vaccinaties_file], value=False, line="INSERT INTO Vaccinatie(batch_nummer, toediening_datum, toediening_plaats, herhaling_datum, vaccinatie_status, Medischedossier_md_nummer, Vaccin_vaccin_naam, Vaccin_vaccin_code)\nVALUES")
for vaccin, index in zip(vaccin_in_memory, range(len(vaccin_in_memory))):
    date = datetime.now() - timedelta(days=random.randint(30, 200))
    md_in_memory = deepcopy(medischedossier_in_memory)
    bewoners_length = int((aantal_bewoners/100)*30)
    random.shuffle(md_in_memory)
    __ = md_in_memory[0:bewoners_length]
    for md_nummer in __:
        batch_nummer = uuid4().__str__().replace("-", "")
        line = f"""("{batch_nummer}", "{date.strftime('%Y-%m-%d')}", "{random.choice(geboorteplaatsen)}", "{(date + timedelta(days=60)).strftime('%Y-%m-%d')}", "{random.choice(["Niet toegediend", "Toegediend"])}", {md_nummer}, "{vaccin[0]}", "{vaccin[1]}")"""
        vaccinaties_in_memory.append(batch_nummer)
        write_line([insertion, vaccinaties_file], value=True, line=line, current_index=index, ending_index=len(vaccin_in_memory), nested_index=not (md_nummer == __[-1]))
vaccinaties_file.close()
files.append("vaccinaties.sql")


vaccin_heeft_bijwerking_file = open("vaccin_heeft_bijwerking.sql", "w")
vaccinatie_heeft_bijwerking_in_memory = []
write_line([insertion, vaccin_heeft_bijwerking_file], value=False, line="INSERT INTO Vaccin_heeft_Bijwerking(Vaccin_vaccin_naam, Vaccin_vaccin_code, Bijwerking_bijwerking_id)\nVALUES")
for vaccin, index in zip(vaccin_in_memory, range(len(vaccin_in_memory))):    
    bijwerkingen = list(set(random.randint(1, 90) for _ in range(random.randint(10, 40))))
    for bijwerking in bijwerkingen:
        line = f"""("{vaccin[0]}", "{vaccin[1]}", {bijwerking})"""
        write_line([insertion, vaccin_heeft_bijwerking_file], value=True, line=line, current_index=index, ending_index=43, nested_index=not (bijwerking == bijwerkingen[-1]))
vaccin_heeft_bijwerking_file.close()
files.append("vaccin_heeft_bijwerking.sql")

medicijn_gebruik_file = open("medicijn_gebruik.sql", "w")
write_line([insertion, medicijn_gebruik_file], value=False, line="INSERT INTO Medicijngebruik(gebruiker_referentie, frequentie, dosering, toediening_wijze, start_datum, eind_datum, type_voorschrift, Medicijn_medicijn_nummer, Medischedossier_md_nummer, Arts_arts_code)\nVALUES")
for medicijn, index in zip(medicijn_in_memory, range(len(medicijn_in_memory))):
    aantal_gebruikers = random.randint(5, len(medischedossier_in_memory))
    md_nummers = deepcopy(medischedossier_in_memory)
    random.shuffle(md_nummers)
    start_date = datetime.now()
    end_date = start_date + timedelta(days=random.randint(10, 250))
    __ = md_nummers[0:aantal_gebruikers]
    for md_nummer in __:
        ref = uuid4().__str__()
        ref = ref.replace("-", "")
        line = f"""("{ref}", "{random.choice(frequenties)}", "{random.choice(doseringen)}", "{random.choice(toedieningswijzen)}", "{start_date.strftime('%Y-%m-%d')}", "{end_date.strftime('%Y-%m-%d')}", "{random.choice(type_voorschriften)}", {medicijn_in_memory[medicijn]}, {md_nummer}, {random.choices(artsen_in_memory)[0]})"""
        write_line([insertion, medicijn_gebruik_file], value=True, line=line, current_index=index, ending_index=len(medicijn_in_memory), nested_index=not (md_nummer == __[-1]))
medicijn_gebruik_file.close()
files.append("medicijn_gebruik.sql")

type_aandoening_file = open("type_aandoening.sql", "w")
write_line([insertion, type_aandoening_file], value=False, line="INSERT INTO Type_aandoening(type_id, naam)\nVALUES")
for type_aandoening, index in zip(type_aandoeningen, range(len(type_aandoeningen))):
    line = f"""({index}, "{type_aandoening}")"""
    write_line([insertion, type_aandoening_file], value=True, line=line, current_index=index, ending_index=len(type_aandoeningen))
type_aandoening_file.close()
files.append("type_aandoening.sql")

ziekte_file = open("ziekte.sql", "w")
ziekte_heeft_type_aandoening_file = open("ziekte_heeft_type_aandoening.sql", "w")
ziekte_bestaat_al = []
ziektes_in_memory = []
ziekte_per_type_aandoening = {type_aandoening:[] for type_aandoening in type_aandoeningen}
write_line([insertion, ziekte_file], value=False, line="INSERT INTO Ziekte(ziekte_id, naam, beschrijving)\nVALUES")
_ = 0
for index, ziekte in zip(range(len(ziektes)), ziektes):
    if ziekte['naam'] not in ziekte_bestaat_al:
        line = f"""({_}, "{ziekte['naam']}", "{ziekte['beschrijving']}")"""
        write_line([insertion, ziekte_file], value=True, line=line, current_index=_, ending_index=57)
        ziekte_bestaat_al.append(ziekte['naam'])
        ziekte_per_type_aandoening[ziekte['type_aandoening']].append(_)
        ziektes_in_memory.append(_)
        _ +=1
write_line([insertion, ziekte_heeft_type_aandoening_file], value=False, line="INSERT INTO Ziekte_heeft_Type_aandoening(Ziekte_ziekte_id, Type_aandoening_type_id)\nVALUES")
for type_aandoening, index in zip(ziekte_per_type_aandoening, range(len(ziekte_per_type_aandoening))):
    for ziekte in ziekte_per_type_aandoening[type_aandoening]:
        line = f"""({ziekte}, {index})"""
        write_line([insertion, ziekte_heeft_type_aandoening_file], value=True, line=line, current_index=index, ending_index=len(ziekte_per_type_aandoening), nested_index=not (ziekte == ziekte_per_type_aandoening[type_aandoening][-1]))

ziekte_file.close()
ziekte_heeft_type_aandoening_file.close()
files.append("ziekte.sql")
files.append("ziekte_heeft_type_aandoening.sql")

onderzoek_file = open("onderzoek.sql", "w")
write_line([insertion, onderzoek_file], value=False, line="INSERT INTO Onderzoek(onderzoek_id, titel, beschrijving, type, status, Medischedossier_md_nummer, Arts_arts_code)\nVALUES")
md_nummers = deepcopy(medischedossier_in_memory)
onderzoeken_in_memory = []
random.shuffle(md_nummers)
for index, onderzoek in zip(range(1, len(onderzoeken)), onderzoeken):
    onderzoek_status = random.choice(["In onderzoek", "Afgerond"])
    md_nummer = random.choice(md_nummers)
    line = f"""({index}, "{onderzoek['titel']}", "{onderzoek['beschrijving']}", "{random.choice(["Diagnostisch onderzoek", "Controle"])}", "{onderzoek_status}", {md_nummer}, {random.choice(artsen_in_memory)})"""
    write_line([insertion, onderzoek_file], value=True, line=line, current_index=index, ending_index=len(onderzoeken))
    onderzoeken_in_memory.append((index, onderzoek_status, md_nummer))
onderzoek_file.close()
files.append("onderzoek.sql")


diagnose_in_memory = []
diagnose_file = open("diagnose.sql", "w")
diagnose_heeft_ziekte_file = open("diagnose_heeft_ziekte.sql", "w")
write_line([insertion, diagnose_file], value=False, line="INSERT INTO Diagnose(diagnose_code, diagnose_naam, diagnose_datum, diagnose_beschrijving, diagnose_status, Arts_arts_code)\nVALUES")
for index, diagnose in zip(range(len(diagnoses)), diagnoses):
    datum = datetime.now() - timedelta(days=random.randint(200, 1000))
    status = random.choice(["in afwachting", "voorlopig", "bevestigd", "uitgesloten", "chronisch", "herstellend"])
    line = f"""({index}, "{diagnose['naam']}", "{datum.strftime('%Y-%m-%d')}", "{diagnose['beschrijving']}", "{status}", {random.choice(artsen_in_memory)})"""
    write_line([insertion, diagnose_file], value=True, line=line, current_index=index, ending_index=len(diagnoses))
    diagnose_in_memory.append(index)
    
write_line([insertion, diagnose_heeft_ziekte_file], value=False, line="INSERT INTO Diagnose_heeft_Ziekte(Ziekte_ziekte_id, Diagnose_diagnose_code)\nVALUES")
for index, diagnose in zip(range(len(diagnose_in_memory)), diagnose_in_memory):
    _ziektes = list({random.choice(ziektes_in_memory) for __ in range(1, 10)})
    xziektes = random.randint(1, 3)
    for _ in range(xziektes):
        line = f"""({_ziektes[_]}, {index})"""
        write_line([insertion, diagnose_heeft_ziekte_file], value=True, line=line, current_index=index, ending_index=len(diagnose_in_memory), nested_index=not (_ == xziektes-1))
diagnose_file.close()
diagnose_heeft_ziekte_file.close()
files.append("diagnose.sql")
files.append("diagnose_heeft_ziekte.sql")

onderzoek_heeft_diagnose_file = open("onderzoek_heeft_diagnose.sql", "w")
write_line([insertion, onderzoek_heeft_diagnose_file], value=False, line="INSERT INTO Onderzoek_heeft_Diagnose(Onderzoek_onderzoek_id, Diagnose_diagnose_code)\nVALUES")
_onderzoeken_in_memory = [onderzoek for onderzoek in onderzoeken_in_memory if onderzoek[1] == "Afgerond"]
for index, onderzoek in zip(range(len(_onderzoeken_in_memory)), _onderzoeken_in_memory):
    if onderzoek[1] == "Afgerond":
        line = f"""({onderzoek[0]}, {diagnose_in_memory[index]})"""
        write_line([insertion, onderzoek_heeft_diagnose_file], value=True, line=line, current_index=index, ending_index=len(_onderzoeken_in_memory))
onderzoek_heeft_diagnose_file.close()
files.append("onderzoek_heeft_diagnose.sql")

geneeswijze_file = open("geneeswijze.sql", "w")
geneeswijze_in_memory = []
write_line([insertion, geneeswijze_file], value=False, line="INSERT INTO Geneeswijze(naam, beschrijving)\nVALUES")
for index, genees_wijze in zip(range(len(geneeswijzen)), geneeswijzen):
    if genees_wijze['naam'] not in geneeswijze_in_memory:
        line = f"""("{genees_wijze['naam']}", "{genees_wijze['beschrijving']}")"""
        write_line([insertion, geneeswijze_file], value=True, line=line, current_index=index, ending_index=131)
        geneeswijze_in_memory.append(genees_wijze['naam'])
geneeswijze_file.close()
files.append("geneeswijze.sql")

ziekte_heeft_geneeswijze_file = open("ziekte_heeft_geneeswijze.sql", "w")
write_line([insertion, ziekte_heeft_geneeswijze_file], value=False, line="INSERT INTO Ziekte_heeft_Geneeswijze(Geneeswijze_naam, Ziekte_ziekte_id)\nVALUES")
for index, ziekte in zip(range(len(ziektes_in_memory)), ziektes_in_memory):
    xgeneeswijzen = random.randint(1, 4)
    _geneeswijzen = list({random.choice(geneeswijze_in_memory) for _ in range(100)})
    for _ in range(xgeneeswijzen):
        line = f"""("{_geneeswijzen[_]}", {ziekte})"""
        write_line([insertion, ziekte_heeft_geneeswijze_file], value=True, line=line, current_index=index, ending_index=len(ziektes_in_memory), nested_index=not (_ == xgeneeswijzen-1))
ziekte_heeft_geneeswijze_file.close()
files.append("ziekte_heeft_geneeswijze.sql")

geneeswijze_heeft_medicijn_file = open("geneeswijze_heeft_medicijn.sql", "w")
write_line([insertion, geneeswijze_heeft_medicijn_file], value=False, line="INSERT INTO Geneeswijze_heeft_Medicijn(Geneeswijze_naam, Medicijn_medicijn_nummer)\nVALUES")
for index, genees_wijze in zip(range(len(geneeswijze_in_memory)), geneeswijze_in_memory):
    xmedicijnen = random.randint(0, 6)
    _medicijnen = list({medicijn_in_memory[random.choice(list(medicijn_in_memory.keys()))] for __ in range(10)})
    for _ in range(xmedicijnen):
        line = f"""("{genees_wijze}", {_medicijnen[_]})"""
        write_line([insertion, geneeswijze_heeft_medicijn_file], value=True, line=line, current_index=index, ending_index=len(geneeswijze_in_memory), nested_index=not (_ == xmedicijnen-1))
geneeswijze_heeft_medicijn_file.close()
files.append("geneeswijze_heeft_medicijn.sql")

behandeling_in_memory = []
behandeling_file = open("behandeling.sql", "w")
write_line([insertion, behandeling_file], value=False, line="INSERT INTO Behandeling(behandeling_nummer, behandeling_datum, behandelaar, locatie, Medischedossier_md_nummer)\nVALUES")
for index, onderzoek in zip(range(len(onderzoeken_in_memory)), onderzoeken_in_memory):
    datum = datetime.now() + timedelta(days=random.randint(1, 10))
    behandelaar = random.choice([worldnames.first_name, faker.first_name])()
    line = f"""({index}, "{datum.strftime('%Y-%m-%d')}", "{behandelaar}", "{random.choice(ziekenhuizen)}", {onderzoek[2]})"""
    write_line([insertion, behandeling_file], value=True, line=line, current_index=index, ending_index=len(onderzoeken_in_memory))
    behandeling_in_memory.append(index)
behandeling_file.close()
files.append("behandeling.sql")

behandeling_heeft_geneeswijze_file = open("behandeling_heeft_geneeswijze.sql", "w")
write_line([insertion, behandeling_heeft_geneeswijze_file], value=False, line="INSERT INTO Behandeling_heeft_Geneeswijze(Behandeling_behandeling_nummer, Geneeswijze_naam)\nVALUES")
for index, behandeling in zip(range(len(behandeling_in_memory)), behandeling_in_memory):
    line = f"""({behandeling}, "{random.choice(geneeswijze_in_memory)}")"""
    write_line([insertion, behandeling_heeft_geneeswijze_file], value=True, line=line, current_index=index, ending_index=len(onderzoeken_in_memory))
behandeling_heeft_geneeswijze_file.close()
files.append("behandeling_heeft_geneeswijze.sql")

afspraak_file = open("afspraak.sql", "w")
write_line([insertion, afspraak_file], value=False, line="INSERT INTO Afspraak(afspraak_referentie, datum, locatie, omschrijving, vervoer, afspraak_status, herhaling, tijdsduur, prioriteit, herinnering_ingesteld, afspraak_type, Medischedossier_md_nummer)\nVALUES")
md_nummers = deepcopy(medischedossier_in_memory)
random.shuffle(md_nummers)
for index, medische_afspraak in zip(range(len(medische_afspraken)), medische_afspraken):
    referentie = uuid4().__str__()
    referentie = referentie.replace("-", "")
    datum = datetime.now() + timedelta(days=random.randint(4, 14))
    line = f"""("{referentie}", "{datum.strftime('%Y-%m-%d')}", "{random.choice(ziekenhuizen)}", "{medische_afspraak['omschrijving']}", "{random.choice(vervoer_types)}", "{random.choice(["Gepland", "Verlopen"])}", {random.randint(0,1)}, "{random.choice(tijdsduur_medische_afspraken)}", "{random.choice(["Hoog", "Gemiddeld", "Laag"])}", {random.randint(0,1)}, "{medische_afspraak['afspraak_type']}", {random.choice(md_nummers)})"""
    write_line([insertion, afspraak_file], value=True, line=line, current_index=index, ending_index=len(medische_afspraken))
afspraak_file.close()
files.append("afspraak.sql")

activiteit_in_memory = []
activiteit_file = open("activiteit.sql", "w")
write_line([insertion, activiteit_file], value=False, line="INSERT INTO Activiteit(activiteit_naam, datum, locatie, categorie, activiteit_beschrijving, duur, activiteit_status)\nVALUES")
for index, activiteit in zip(range(len(activiteiten_verzorgingcentrum)), activiteiten_verzorgingcentrum):
    status = random.choice(["binnenkort", "bezig", "beëndigd"])
    if status == "binnenkort":
        datum = datetime.now() + timedelta(days=random.randint(1, 7))
    else:
       datum = datetime.now() - timedelta(days=random.randint(1, 7)) 
    ac_naam = activiteit['activiteit_naam']
    ac_locatie = activiteit['locatie']
    line = f"""("{activiteit['activiteit_naam']}", "{datum.strftime('%Y-%m-%d')}", "{ac_locatie}", "{activiteit['categorie']}", "{activiteit['activiteit_beschrijving']}", "{activiteit['duur']}", "{status}")"""
    write_line([insertion, activiteit_file], value=True, line=line, current_index=index, ending_index=len(activiteiten_verzorgingcentrum))
    activiteit_in_memory.append((ac_naam, datum, ac_locatie))
activiteit_file.close()
files.append("activiteit.sql")

bewoner_bezoekt_activiteit_file = open("bewoner_bezoekt_activiteit.sql", "w")
write_line([insertion, bewoner_bezoekt_activiteit_file], value=False, line="INSERT INTO Bewoner_bezoekt_Activiteit(Activiteit_activiteit_naam, Activiteit_datum, Activiteit_locatie, Bewoner_code)\nVALUES")
for index, activiteit in zip(range(len(activiteit_in_memory)), activiteit_in_memory):
    ac_naam, datum, ac_locatie = activiteit
    xbewoners = random.randint(2, 10)
    _bewoners = deepcopy(bewoners_in_memory)
    random.shuffle(_bewoners)
    for _ in range(xbewoners):
        line = f"""("{ac_naam}", "{datum.strftime('%Y-%m-%d')}", "{ac_locatie}", {_bewoners[_]})"""
        write_line([insertion, bewoner_bezoekt_activiteit_file], value=True, line=line, current_index=index, ending_index=(len(activiteiten_verzorgingcentrum)), nested_index=not (_ == xbewoners-1))
bewoner_bezoekt_activiteit_file.close()
files.append("bewoner_bezoekt_activiteit.sql")

zorgbehoefte_in_memory = []
zorgbehoeftes_file = open("zorgbehoefte.sql", "w")
write_line([insertion, zorgbehoeftes_file], value=False, line="INSERT INTO Zorgbehoefte(zb_code, zb_categorie, zb_naam, zb_beschrijving, urgentie)\nVALUES")
for index, zorgbehoefte in zip(range(len(zorgbehoeftes_ouderen)), zorgbehoeftes_ouderen):
    line = f"""({index}, "{zorgbehoefte['zb_categorie']}", "{zorgbehoefte['zb_naam']}", "{zorgbehoefte['zb_beschrijving']}", {random.randint(0,1)})"""
    write_line([insertion, zorgbehoeftes_file], value=True, line=line, current_index=index, ending_index=len(zorgbehoeftes_ouderen))
    zorgbehoefte_in_memory.append(index)
zorgbehoeftes_file.close()
files.append("zorgbehoefte.sql")

_bewoners = [bewoner for bewoner in bewoners_in_memory]

bewoner_heeft_zorgbehoefte_file = open("bewoner_heeft_zorgbehoefte.sql", "w")
write_line([insertion, bewoner_heeft_zorgbehoefte_file], value=False, line="INSERT INTO Bewoner_heeft_Zorgbehoefte(Zorgbehoefte_zb_code, Bewoner_code)\nVALUES")
for index, bewoner in zip(range(len(_bewoners)), _bewoners):
    random.shuffle(zorgbehoefte_in_memory)
    xbehoeftes = random.randint(1, 10)
    for _ in range(xbewoners):
        line = f"""({zorgbehoefte_in_memory[_]}, {bewoner})"""
        write_line([insertion, bewoner_heeft_zorgbehoefte_file], value=True, line=line, current_index=index, ending_index=len(_bewoners), nested_index=not (_ == xbewoners-1))
bewoner_heeft_zorgbehoefte_file.close()
files.append("bewoner_heeft_zorgbehoefte.sql")

zorgplan_file = open("zorgplan.sql", "w")
write_line([insertion, zorgplan_file], value=False, line="INSERT INTO Zorgplan(referentie_nummer, opstelling_datum, herziening_datum, zorg_doelen, zorg_type, behandel_plan, frequentie_zorg, specifieke_instructies, zorgplan_status, Bewoner_code)\nVALUES")
for index, bewoner in zip(range(len(_bewoners)), _bewoners):
    _zorgplan = zorgplan()
    opstelling_datum = datetime.now()
    herziening_datum = opstelling_datum + timedelta(days=random.randint(10, 200))
    line = f"""({index}, "{opstelling_datum.strftime('%Y-%m-%d')}", "{herziening_datum.strftime('%Y-%m-%d')}", "{_zorgplan['zorg_doelen']}", "{_zorgplan['zorg_type']}", "{_zorgplan['behandel_plan']}", "{_zorgplan['frequentie_zorg']}", "{_zorgplan['specifieke_instructies']}", "{random.choice(["open", "wordt uitgevoerd"])}", {bewoner})"""
    write_line([insertion, zorgplan_file], value=True, line=line, current_index=index, ending_index=len(_bewoners))
zorgplan_file.close()
files.append("zorgplan.sql")

bewoner_heeft_zorgverlener_file = open("bewoner_heeft_zorgverlener.sql", "w")
write_line([insertion, bewoner_heeft_zorgverlener_file], value=False, line="INSERT INTO Bewoner_heeft_Zorgverlener(Zorgverlener_big_code, Bewoner_code)\nVALUES")
_dzorgverleners = deepcopy(zorgverleners_in_memory)
for index, bewoner in zip(range(len(_bewoners)), _bewoners):
    random.shuffle(_dzorgverleners)
    xzorgverleners = random.randint(1, 10)
    for _ in range(xzorgverleners):
        zorgverlener = _dzorgverleners[_]
        line = f"""("{zorgverlener[0]}", "{bewoner}")"""
        write_line([insertion, bewoner_heeft_zorgverlener_file], value=True, line=line, current_index=index, ending_index=len(_bewoners), nested_index=not (_ == xzorgverleners-1))
bewoner_heeft_zorgverlener_file.close()
files.append("bewoner_heeft_zorgverlener.sql")

insertion.close()
stored_files = open("files.json", "w")
json.dump({"files":files}, stored_files)
stored_files.close()

end = time.time()
print(f"Took {round(end-start, 2)} seconds")
