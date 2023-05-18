import kundenkartei
import prompt
import extraktor


if __name__ == "__main__":
    # Initialisiere die zu füllende Kundenkartei
    profil = kundenkartei.Kundenkartei(prompt.zwischenablage())

    # Teste NER an der Signatur
    # extraktor.entity_erkennung(profil)

    # Extrahiere attribute und kürze die Signatur um verbleibende
    # Attribute leichter zu finden

    # Zuerst werden Name, E-Mail und Nummern extrahiert, um da
    # diese am schwersten zu verwechseln sind
    extraktor.extrahiere_name(profil)
    extraktor.extrahiere_email(profil)
    extraktor.extrahiere_nummern(profil)

    # Nun werden die erhaltenen informationen aus der Signatur
    # gelöscht, um den weiteren verlauf zu erleichtern
    extraktor.radiere_signatur(profil)

    # Ohne die E-Mail in der Signatur ist eine URL nicht zu verwechseln
    # und kann nun fehlerfrei extrahiert werden
    extraktor.extrahiere_url(profil)
    extraktor.radiere_signatur(profil)

    extraktor.extrahiere_ortschaft(profil)
    extraktor.radiere_signatur(profil)
    extraktor.extrahiere_strasse(profil)
    extraktor.radiere_signatur(profil)
    extraktor.extrahiere_firma(profil)
    extraktor.radiere_signatur(profil)

    # Prompte den User zur korrektur oder bestätigung.
    while True:
        nummer = prompt.bestaetigung(profil)
        if nummer == 0:
            print("Die Kundekartei wurde für Sie angelegt\nBis zum nächsten mal :)")
            break
        prompt.edit_attribut(profil, nummer)
