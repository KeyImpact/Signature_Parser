import spacy
import re
import phonenumbers.phonenumbermatcher

"""Funktionen für die extraktion der Attribute"""


# Name wird mit Named entity recognition extrahiert
# funktioniert jedoch nicht immer zuverlässig da die Sprachmodelle
# kontext benötigen, welcher in einer Signatur nicht gegeben ist.
# Zum Testen der Sprachmodelle siehe funktion entity_erkennung()
def extrahiere_name(kunde):
    nlp = spacy.load("de_core_news_md")
    signatur_tokens = nlp(kunde.signatur)
    per = True
    for ent in signatur_tokens.ents:
        if ent.label_ == "PER" and per:
            name = ent.text.strip()
            per = False
            kunde.radierer.append(name)
            kunde.ansprechpartner = name
        else:
            break


# Ermittlung der Position der Firma anhand der Rechtsform
# mit regex. Falls keine Rechtsform vorhanden ist, wird aus dem
# Domain-Teil der E-Mail der Firmennamen ermittelt. Falls keine E-Mail
# vorhanden ist, wird der Domain-Teil der URL verwendet.
def extrahiere_firma(kunde):
    rechtsformen_regex = 'GmbH|AG|KG|OHG|e.V.|GbR|UG'
    rechtsform = re.search(rechtsformen_regex, kunde.signatur)

    if rechtsform:
        vor_der_rechtsform = kunde.signatur[:rechtsform.span()[1]]
        index_anfang = finde_trennung_davor(vor_der_rechtsform)
        index_ende = finde_trennung_danach(kunde.signatur[index_anfang:])
        firmenname = kunde.signatur[index_anfang:(index_anfang + index_ende)]

        kunde.firma = firmenname.strip()
        kunde.radierer.append(firmenname)

    elif kunde.email:
        email_domain_regex = '@([^.]+)\\.'
        email_domain = re.search(email_domain_regex, kunde.email)
        kunde.firma = email_domain.group(1).capitalize()

    elif kunde.webseite:
        url_regex = r'(?:https?://)?(?:www\.)?([^./]+)\.'
        url_domain = re.search(url_regex, kunde.webseite)
        kunde.firma = url_domain.group(1).capitalize()

    else:
        return None


# Ermittlung der Hausnummer durch regex, nachdem alle erwarteten
# Ziffern (PLZ und Telefonnummern) aus der Signatur gekürzt worden sind.
# Das Element vor der Ziffer ist i.d.R. der Strassenname
def extrahiere_strasse(kunde):
    hausnummer_regex = r"\b\d{1,3}\b"
    hausnummer_in_string = re.search(hausnummer_regex, kunde.signatur)

    if hausnummer_in_string:
        vor_der_hausnummer = kunde.signatur[:hausnummer_in_string.span()[1]]
        index_anfang = finde_trennung_davor(vor_der_hausnummer)
        index_ende = finde_trennung_danach(kunde.signatur[index_anfang:])
        adresse = kunde.signatur[index_anfang:(index_anfang + index_ende)]
        rohadresse = adresse.strip()
        kunde.strasse = rohadresse.strip("-")
        kunde.radierer.append(adresse)
    else:
        return None


# Es wird nach 4 oder 5 Ziffern gesucht, von denen Ausgegangen wird, dass es sich
# um Postleitzahlen hält.
# Da PLZ i.d.R vor der Ortschaft stehen, wird das Element
# danach als Ortschaft genommen. Es wird davon ausgegangen, dass 5 Ziffern zu DE
# gehören, während bei 4 Ziffern in der Signatur nach Schlüsselwörtern gesucht wird,
# um das Land zu ermitteln.
def extrahiere_ortschaft(kunde):
    ger_plz_regex = '\\d{5}'
    other_plz_regex = '\\d{4}'

    ger_match = re.search(ger_plz_regex, kunde.signatur)
    other_match = re.search(other_plz_regex, kunde.signatur)

    if ger_match:
        plz = ger_match.group()
        nach_plz = kunde.signatur[ger_match.span()[1]:]
        einzelteile = nach_plz.split()

        kunde.radierer.append(plz)
        kunde.radierer.append(einzelteile[0])
        # if any(keyword in kunde.signatur for keyword in ["Deutschland", "Germany", "DE"]):
        #    kunde.land = "Deutschland"
        kunde.land = "Deutschland"
        kunde.plz = plz
        kunde.ortschaft = einzelteile[0].strip().strip(',')

    elif other_match:
        if any(keyword in kunde.signatur for keyword in ["Österreich", "Austria", "AT"]):
            kunde.land = "Österreich"
        elif any(keyword in kunde.signatur for keyword in ["Schweiz", "Switzerland", "CH", "Svizzera"]):
            kunde.land = "Schweiz"
        plz = other_match.group()
        nach_plz = kunde.signatur[other_match.span()[1]:]
        einzelteile = nach_plz.split()

        kunde.radierer.append(plz)
        kunde.radierer.append(einzelteile[0])
        kunde.plz = plz
        kunde.ortschaft = einzelteile[0].strip().strip(',')

    else:
        return None

# Extrahiere die E-Mail aus der Signatur und füge sie der Kundenkartei hinzu
def extrahiere_email(kunde):
    mail_regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\\.[A-Z|a-z]{2,})+'
    mail = re.search(mail_regex, kunde.signatur)
    if mail:
        kunde.radierer.append(mail.group())
        kunde.email = mail.group().strip()
    else:
        return None


# Nummern werden mithilfe der Bibliothek Phonenumbers extrahiert.
# Um zwischen Fon, Fax, Mobil usw. zu unterscheiden wird das Element vor
# der Nummer ebenfalls in die Kundenkartei gelesen.
# Alle Treffer werden der Liste hinzugefügt, welche am Ende der Kundenkartei
# hinzugefügt wird.
def extrahiere_nummern(kunde):
    nummer_liste = []
    try:
        for nummer_obj in phonenumbers.PhoneNumberMatcher(kunde.signatur, region='DE'):
            signatur_slice = kunde.signatur[:nummer_obj.end]
            trennung = finde_trennung_davor(signatur_slice)
            die_nummer = signatur_slice[trennung:].strip()
            nummer_liste.append(die_nummer)
            kunde.radierer.append(die_nummer)
        kunde.nummern = nummer_liste
    except phonenumbers.NumberParseException:
        kunde.nummern = None


# Extrahiere URL mithilfe von Regex und füge sie in die Kundenkartei
def extrahiere_url(kunde):
    url_regex = r"\b(?:(?:https?):\/\/|www\.)[^\s/$.?#].[^\s]*\b"

    url = re.search(url_regex, kunde.signatur)

    if url:
        kunde.radierer.append(url.group())
        kunde.webseite = url.group().strip()
    else:
        return None


"""Unterstützende Funktionen"""


# Funktion zum Testen der drei Pipelines von NER.
# Alle erkannten Label werden ausgegeben.
# Wird nur für die erkennung der Namen der Ansprechpartner benutzt,
# da der Kontext für eine verlässliche erkennung weiterer
# Entitäten nicht gegeben ist.
def entity_erkennung(kunde):
    small = spacy.load("de_core_news_sm")
    middle = spacy.load("de_core_news_md")
    large = spacy.load("de_core_news_lg")

    slice1 = small(kunde.signatur)
    slice2 = middle(kunde.signatur)
    slice3 = large(kunde.signatur)

    print("---------------------------------------")
    for ent in slice1.ents:
        print(f"[sm] --- {ent.label_} --- {ent} ")
    print("\n")

    for ent in slice2.ents:
        print(f"[md] --- {ent.label_} --- {ent} ")
    print("\n")

    for ent in slice3.ents:
        print(f"[lg] --- {ent.label_} --- {ent} ")
    print("\n")
    print("---------------------------------------")


# Replace bereits erhaltene info aus der Signatur mit Whitespace
# um verbleibende Attribute leichter rauszufiltern
def radiere_signatur(kunde):
    if not kunde.radierer:
        return
    for item in kunde.radierer:
        kunde.signatur = kunde.signatur.replace(item, " ")
    kunde.radierer = []


# Finde das letzte Trennzeichen der Kategorie (z.b. Firma) VOR dem Attribut
# und return den index NACH der trennung
def finde_trennung_davor(signatur_slice):
    eins = signatur_slice.rfind('|')
    zwei = signatur_slice.rfind('\n')
    drei = signatur_slice.rfind('•')
    vier = signatur_slice.rfind(',')

    index = max(eins, zwei, drei, vier)

    return index + 1


# Finde das erste Trennzeichen und ignoriere
# die, die nicht vorhanden sind (sonst -> -1).
def finde_trennung_danach(signatur_slice):
    eins = signatur_slice.find('|')
    zwei = signatur_slice.find('\n')
    drei = signatur_slice.find('•')
    vier = signatur_slice.find(',')

    index_liste = [position for position in [eins, zwei, drei, vier] if position != -1]

    if index_liste:
        return min(index_liste)
    else:
        raise ValueError
