import random

# Definieer de basiscomponenten
zorg_doelen = [
    "Verbeteren van mobiliteit en zelfredzaamheid",
    "Beheersen van chronische ziekten",
    "Verminderen van angst en stress",
    "Verbeteren van eetgewoonten",
    "Bevorderen van sociale interactie",
    "Ondersteunen van cognitieve functies",
    "Bevorderen van geestelijke gezondheid",
    "Verbeteren van huidgezondheid",
    "Bevorderen van zelfstandigheid",
    "Verminderen van pijn",
    "Bevorderen van slaapkwaliteit",
    "Ondersteunen van voeding en hydratatie",
    "Bevorderen van mentale stimulatie",
    "Bevorderen van emotioneel welzijn",
    "Ondersteunen van dagelijkse hygiëne",
    "Bevorderen van zelfstandigheid in voeding",
    "Ondersteunen van sociale verbinding",
    "Verbeteren van cognitieve vaardigheden",
    "Bevorderen van lichamelijke gezondheid",
    "Ondersteunen van geestelijke gezondheid",
    "Verbeteren van algehele gezondheid",
    "Ondersteunen van geestelijke gezondheid",
    "Bevorderen van zelfstandigheid"
]

zorg_types = [
    "Fysiotherapie",
    "Medische zorg",
    "Psychosociale ondersteuning",
    "Voedingszorg",
    "Sociaal",
    "Cognitief",
    "Pijnbeheer",
    "Hulpmiddelen en adaptieve technologie",
    "Geestelijke gezondheid",
    "Spiritualiteit",
    "Slaap en rust",
    "Revalidatie",
    "Huisvesting en omgeving",
    "Financieel beheer",
    "Juridische ondersteuning",
    "Zorgplanning en coördinatie",
    "Familie en mantelzorg",
    "Persoonlijke verzorging",
    "Mobiliteit"
]

behandel_plannen = [
    "Dagelijkse oefeningen gericht op spierversterking en balans.",
    "Regelmatige monitoring en behandeling van aandoeningen zoals diabetes en hypertensie.",
    "Wekelijkse counseling sessies en dagelijkse ontspanningsoefeningen.",
    "Op maat gemaakte dieetplannen en wekelijkse voedingssessies.",
    "Dagelijkse groepsactiviteiten en wekelijkse uitstapjes.",
    "Dagelijkse geheugentraining en wekelijkse puzzelsessies.",
    "Beheer van chronische pijn door medicatie en niet-medicamenteuze therapieën.",
    "Gebruik en aanpassing van rolstoelen voor mobiliteit.",
    "Wekelijkse therapiegroepen en maandelijkse individuele sessies.",
    "Regelmatige huidverzorgingsroutine en wekelijkse dermatologische controles.",
    "Training in dagelijkse activiteiten en gebruik van hulpmiddelen.",
    "Dagelijkse ademhalingsoefeningen en wekelijkse ontspanningssessies.",
    "Aanpassingen aan de woonomgeving voor betere toegankelijkheid.",
    "Ondersteuning bij het beheren van financiële zaken en budgettering.",
    "Toegang tot juridische hulp voor het opstellen van testamenten.",
    "Coördinatie van algehele zorg voor elke bewoner.",
    "Faciliteren van bezoeken en bieden van ondersteuning aan familieleden.",
    "Regelmatige medicatie-inname en wekelijkse bloeddrukmetingen.",
    "Ondersteuning bij wassen, aankleden, eten en andere dagelijkse routines."
]

frequentie_zorg = [
    "Dagelijks",
    "Meerdere keren per week",
    "Wekelijks",
    "Maandelijks",
    "Elke twee weken",
    "Elke dag",
    "Elke week",
    "Op aanvraag",
    "Nadat nodig",
    "3 keer per week"
]

specifieke_instructies = [
    "Gebruik van wandelstok tijdens oefeningen, focus op benen en rug.",
    "Medicatie 's ochtends innemen, bloeddruk registreren in logboek.",
    "Deelnemen aan ademhalingsoefeningen elke ochtend.",
    "Gezonde snacks beschikbaar stellen, rekening houden met allergieën.",
    "Actief deelnemen aan spelletjes en gesprekken.",
    "Gebruik van geheugenapps en deelname aan groepspuzzels.",
    "Registreren van pijnniveaus in dagelijks logboek.",
    "Veilig gebruik van looprekjes en rolstoelen.",
    "Open deelname aan gesprekken, vertrouwelijke omgeving.",
    "Gebruik van hypoallergene producten, vermijden van irriterende stoffen.",
    "Aanpassen van woonomgeving voor betere toegankelijkheid.",
    "Creëren van een rustige en comfortabele slaapruimte.",
    "Aanbieden van water en voedzame snacks gedurende de dag.",
    "Veilig gebruik van looprekjes en rolstoelen.",
    "Gebruik van geheugenapps en deelname aan groepspuzzels.",
    "Deelnemen aan ademhalingsoefeningen elke ochtend.",
    "Regelmatige monitoring en behandeling van aandoeningen zoals diabetes en hypertensie.",
    "Ondersteuning bij wassen, aankleden, eten en andere dagelijkse routines.",
    "Gebruik van wandelstok tijdens oefeningen, focus op benen en rug.",
    "Medicatie 's ochtends innemen, bloeddruk registreren in logboek."
]

def zorgplan():
    doel = random.choice(zorg_doelen)
    type_zorg = random.choice(zorg_types)
    behandel_plan = random.choice(behandel_plannen)
    frequentie = random.choice(frequentie_zorg)
    instructies = random.choice(specifieke_instructies)
    zorgplan = {
            "zorg_doelen": doel,
            "zorg_type": type_zorg,
            "behandel_plan": behandel_plan,
            "frequentie_zorg": frequentie,
            "specifieke_instructies": instructies
        }
    return zorgplan


