import pyperclip


def zwischenablage():
    input("Kopieren Sie die Signatur und bestätigen Sie mit ENTER")
    clipboard = pyperclip.paste()
    return clipboard


def display_signaturen(kunde):
    print("---------------------------------------")
    print("\nOriginal Signatur: \n")
    print(kunde.original)
    print("---------------------------------------")

    print("---------------------------------------")
    print("\nGekürzte Signatur: \n")
    print(kunde.signatur)
    print("---------------------------------------")


# Fordere den Nutzer dazu auf das Fertige Profil zu bestätigen oder zu Editieren
def bestaetigung(kunde):
    print(kunde)
    print("\nSind Sie mit der folgenden Auswahl zufrieden?\n")
    print("\nWenn Sie zufrieden sind, bestätigen Sie mit '0'\n"
          "Zur weiterbearbeitung drücken Sie die jeweilige Zahl")

    while True:
        try:
            eingabe = int(input("Geben Sie eine Nummer ein: "))
            break
        except ValueError:
            print("Ungültige Eingabe, bitte versuchen Sie es nochmal")

    if eingabe == 0:
        print("Die Kundekartei wurde für Sie angelegt"
              "\nBis zum nächsten mal :)")
        quit()

    elif 0 <= int(eingabe) <= 10:
        return eingabe

    else:
        print("Ziffer zu hoch")
        bestaetigung(kunde)


# Attribute werden bearbeitet
def edit_attribut(kunde, nummer):
    if nummer == 1:
        kunde.ansprechpartner = input("Geben Sie den neuen Ansprechpartner ein: ")
    elif nummer == 2:
        kunde.firma = input("Geben Sie den neuen Firmennamen ein: ")
    elif nummer == 3:
        kunde.strasse = input("Geben Sie die neue Straße und Hausnummer ein: ")
    elif nummer == 4:
        kunde.plz = input("Geben Sie die neue Postleitzahl ein: ")
    elif nummer == 5:
        kunde.ortschaft = input("Geben Sie die neue Ortschaft ein: ")
    elif nummer == 6:
        kunde.land = input("Geben Sie das neue Land ein: ")
    elif nummer == 7:
        kunde.email = input("Geben Sie die neue E-Mail-Adresse ein: ")
    elif nummer == 8:
        kunde.nummern = input("Geben Sie die neue Telefonnummer(n) ein: ")
    elif nummer == 9:
        kunde.webseite = input("Geben Sie die neue Webseite ein: ")
    else:
        print("Ungültige Eingabe")
        return

    print("\nProfil erfolgreich aktualisiert:")
