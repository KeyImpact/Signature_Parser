"""Kundenkartei die beim Initialisieren die Signatur benötigt aus der die Attribute gezogen werden"""


class Kundenkartei:

    def __init__(self, signatur):
        self.ansprechpartner = None
        self.firma = None
        self.strasse = None
        self.plz = None
        self.ortschaft = None
        self.land = None
        self.email = None
        self.nummern = None
        self.webseite = None
        self.signatur = signatur
        self.radierer = []
        self.original = signatur

        if self.original is None:
            raise ValueError("Keine gültige Signatur eingelesen")

    def __str__(self):
        return f"\n[1]Name: {self.ansprechpartner}\n" \
               f"[2]Firma: {self.firma}\n" \
               f"[3]Straße und Hausnummer: {self.strasse}\n" \
               f"[4]PLZ: {self.plz}\n" \
               f"[5]Ortschaft: {self.ortschaft}\n" \
               f"[6]Land: {self.land}\n" \
               f"[7]E-Mail: {self.email}\n" \
               f"[8]Nummer(n): {self.nummern}\n" \
               f"[9]Webseite: {self.webseite}"
