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

start = time.time()

faker = Faker("nl_NL")

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
aantal_personen = 150
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
artsen_in_memory = [arts[0] for arts in artsen_in_memory[0:aantal_artsen]]
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

vaccin_file = open("vaccin.sql", "w")
vaccin_in_memory = []
vaccin_bestaat_al = []
write_line([insertion, vaccin_file], value=False, line="INSERT INTO Vaccin(vaccin_naam, vaccin_code, opmerkingen)\nVALUES")
for vaccin, index in zip(vaccinaties, range(len(vaccinaties))):
    if vaccin['vaccin_naam'] not in vaccin_bestaat_al:
        line = f"""("{vaccin['vaccin_naam']}", "{vaccin['vaccinatie_code']}", "{vaccin['opmerkingen']}")"""
        write_line([insertion, vaccin_file], value=True, line=line, current_index=index, ending_index=len(vaccinaties))
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
    for md_nummer in md_in_memory[0:bewoners_length]:
        batch_nummer = uuid4().__str__().replace("-", "")
        line = f"""("{batch_nummer}", "{date.strftime('%Y-%m%d')}", "{random.choice(geboorteplaatsen)}", "{(date + timedelta(days=60)).strftime('%Y-%m-%d')}", "{random.choice(["Niet toegediend", "Toegediend"])}", {md_nummer}, "{vaccin[0]}", "{vaccin[1]}")"""
        vaccinaties_in_memory.append(batch_nummer)
        write_line([insertion, vaccinaties_file], value=True, line=line, current_index=index, ending_index=len(vaccinaties))
vaccinaties_file.close()
files.append("vaccinaties.sql")


vaccin_heeft_bijwerking_file = open("vaccin_heeft_bijwerking.sql", "w")
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
    bijwerking_bestaat_al.append(bijwerking['naam'])

write_line([insertion, vaccin_heeft_bijwerking_file], value=False, line="INSERT INTO Vaccin_heeft_Bijwerking(Vaccin_vaccin_naam, Vaccin_vaccin_code, Bijwerking_bijwerking_id)\nVALUES")
for vaccin, index in zip(vaccin_in_memory, range(len(vaccin_in_memory))):    
    bijwerkingen = set(random.randint(1, 90) for _ in range(random.randint(10, 40)))
    for bijwerking in bijwerkingen:
        line = f"""("{vaccin[0]}", "{vaccin[1]}", {bijwerking})"""
        write_line([insertion, vaccin_heeft_bijwerking_file], value=True, line=line, current_index=index, ending_index=len(vaccinaties_in_memory))
vaccin_heeft_bijwerking_file.close()
bijwerkingen_file.close()
files.append("vaccin_heeft_bijwerking.sql")

medicijn_gebruik_file = open("medicijn_gebruik.sql", "w")
write_line([insertion, medicijn_gebruik_file], value=False, line="INSERT INTO Medicijngebruik(gebruiker_referentie, frequentie, dosering, toediening_wijze, start_datum, eind_datum, type_voorschrift, Medicijn_medicijn_nummer, Medischedossier_md_nummer, Arts_arts_code)\nVALUES")
for medicijn, index in zip(medicijn_in_memory, range(len(medicijn_in_memory))):
    ref = uuid4().__str__()
    ref = ref.replace("-", "")
    aantal_gebruikers = random.randint(5, len(medischedossier_in_memory))
    md_nummers = deepcopy(medischedossier_in_memory)
    random.shuffle(md_nummers)
    start_date = datetime.now()
    end_date = start_date + timedelta(days=random.randint(10, 250))
    for md_nummer in md_nummers[0:aantal_gebruikers]:
        line = f"""("{ref[0:10]}", "{random.choice(frequenties)}", "{random.choice(doseringen)}", "{random.choice(toedieningswijzen)}", "{start_date.strftime('%Y-%m-%d')}", "{end_date.strftime('%Y-%m-%d')}", "{random.choice(type_voorschriften)}", {medicijn_in_memory[medicijn]}, {md_nummer}, {random.choices(artsen_in_memory)[0]})"""
        write_line([insertion, medicijn_gebruik_file], value=True, line=line, current_index=index, ending_index=len(medicijn_in_memory))
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
write_line([insertion, ziekte_heeft_type_aandoening_file], value=False, line="INSERT INTO Ziekte(Ziekte_ziekte_id, Type_aandoening_type_id)\nVALUES")
write_line([insertion, ziekte_file], value=False, line="INSERT INTO Ziekte(ziekte_id, naam, beschrijving)\nVALUES")
for index, ziekte in zip(range(len(ziektes)), ziektes):
    if ziekte['naam'] not in ziekte_bestaat_al:
        line = f"""({index}, "{ziekte['naam']}", "{ziekte['beschrijving']}")"""
        write_line([insertion, ziekte_file], value=True, line=line, current_index=index, ending_index=len(ziektes))
        ziekte_bestaat_al.append(ziekte['naam'])
        ziekte_per_type_aandoening[ziekte['type_aandoening']].append(index)
        ziektes_in_memory.append(index)
for type_aandoening, index in zip(ziekte_per_type_aandoening, range(len(ziekte_per_type_aandoening))):
    for ziekte in ziekte_per_type_aandoening[type_aandoening]:
        line = f"""({ziekte}, {index})"""
        write_line([insertion, ziekte_heeft_type_aandoening_file], value=True, line=line, current_index=index, ending_index=len(ziekte_per_type_aandoening))

ziekte_file.close()
ziekte_heeft_type_aandoening_file.close()
files.append("ziekte.sql")
files.append("ziekte_heeft_type_aandoening.sql")

onderzoek_file = open("onderzoek.sql", "w")
write_line([insertion, onderzoek_file], value=False, line="INSERT INTO Onderzoek(onderzoek_id, titel, beschrijving, type, status, Medischedossier_md_nummer, Arts_arts_code)\nVALUES")
md_nummers = deepcopy(medischedossier_in_memory)
onderzoeken_in_memory = []
random.shuffle(md_nummers)
for index, onderzoek in zip(range(len(onderzoeken)), onderzoeken):
    onderzoek_status = random.choice(["In onderzoek", "Afgerond"])
    line = f"""({index}, "{onderzoek['titel']}", "{onderzoek['beschrijving']}", "{random.choice(["Diagnostisch onderzoek", "Controle"])}", "{onderzoek_status}", {random.choice(md_nummers)}, {random.choice(artsen_in_memory)})"""
    write_line([insertion, onderzoek_file], value=True, line=line, current_index=index, ending_index=len(onderzoeken))
    onderzoeken_in_memory.append((index, onderzoek_status))
onderzoek_file.close()
files.append("onderzoek.sql")

diagnose_file = open("diagnose.sql", "w")
diagnose_heeft_ziekte_file = open("diagnose_heeft_ziekte.sql", "w")
write_line([insertion, diagnose_file], value=False, line="INSERT INTO Diagnose(diagnose_code, diagnose_naam, diagnose_datum, diagnose_beschrijving, diagnose_status, Arts_arts_code)\nVALUES")
write_line([insertion, diagnose_heeft_ziekte_file], value=False, line="INSERT INTO Diagnose_heeft_Ziekte(Ziekte_ziekte_id, Diagnose_diagnose_code)\nVALUES")
for index, diagnose in zip(range(len(diagnoses)), diagnoses):
    datum = datetime.now() - timedelta(days=random.randint(200, 1000))
    status = random.choice(["in afwachting", "voorlopig", "bevestigd", "uitgesloten", "chronisch", "herstellend"])
    line = f"""({index}, "{diagnose['naam']}", "{datum.strftime('%Y-%m-%d')}", "{diagnose['beschrijving']}", "{status}", {random.choice(artsen_in_memory)})"""
    write_line([insertion, diagnose_file], value=True, line=line, current_index=index, ending_index=len(diagnoses))
    _ziektes = list({random.choice(ziektes_in_memory) for __ in range(10)})
    xziektes = random.randint(1, 3)
    for _ in range(xziektes):
        line = f"""({_ziektes[_]}, {index})"""
        write_line([insertion, diagnose_heeft_ziekte_file], value=True, line=line, current_index=index, ending_index=len(diagnoses))
diagnose_file.close()
diagnose_heeft_ziekte_file.close()
files.append("diagnose.sql")
files.append("diagnose_heeft_ziekte.sql")

geneeswijze_file = open("geneeswijze.sql", "w")
geneeswijze_in_memory = []
write_line([insertion, geneeswijze_file], value=False, line="INSERT INTO Geneeswijze(naam, beschrijving)\nVALUES")
for index, genees_wijze in zip(range(len(geneeswijzen)), geneeswijzen):
    if genees_wijze['naam'] not in geneeswijze_in_memory:
        line = f"""("{genees_wijze['naam']}", "{genees_wijze['beschrijving']}")"""
        write_line([insertion, geneeswijze_file], value=True, line=line, current_index=index, ending_index=len(geneeswijzen))
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
        write_line([insertion, ziekte_heeft_geneeswijze_file], value=True, line=line, current_index=index, ending_index=len(ziektes_in_memory))
ziekte_heeft_geneeswijze_file.close()
files.append("ziekte_heeft_geneeswijze.sql")

geneeswijze_heeft_medicijn_file = open("geneeswijze_heeft_medicijn.sql", "w")
write_line([insertion, geneeswijze_heeft_medicijn_file], value=False, line="INSERT INTO Geneeswijze_heeft_Medicijn(Geneeswijze_naam, Medicijn_medicijn_nummer)\nVALUES")
for index, genees_wijze in zip(range(len(geneeswijze_in_memory)), geneeswijze_in_memory):
    xmedicijnen = random.randint(0, 6)
    _medicijnen = list({medicijn_in_memory[random.choice(list(medicijn_in_memory.keys()))] for __ in range(10)})
    for _ in range(xmedicijnen):
        line = f"""("{genees_wijze}", {_medicijnen[_]})"""
        write_line([insertion, geneeswijze_heeft_medicijn_file], value=True, line=line, current_index=index, ending_index=len(geneeswijze_in_memory))
geneeswijze_heeft_medicijn_file.close()
files.append("geneeswijze_heeft_medicijn.sql")

insertion.close()
stored_files = open("files.json", "w")
json.dump({"files":files}, stored_files)
stored_files.close()

end = time.time()
print(f"Took {round(end-start, 2)} seconds")