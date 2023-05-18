import unittest
import kundenkartei
import extraktor


class Testkundenkartei(unittest.TestCase):

    def test_init(self):
        signatur = "Max Mustermann	\nProduct Engineering\nHead of Mastersystems\nSuper Muster Motive GmbH 	" \
                   "\nMuster-Zufall-Straße 6\nD-21102 Kiel /Germany	\nfon: +49 421 3949-2257" \
                   "\nmobil: +49 112 2672085\nmail: maximilian.must@mu-wf.com\nweb: http://www.mu-wf.com	"
        kunde = kundenkartei.Kundenkartei(signatur)
        self.assertIsNotNone(kunde)
        self.assertEqual(kunde.original, signatur)

    def test_init_fehler(self):
        with self.assertRaises(ValueError):
            kundenkartei.Kundenkartei(None)

    def test_extrahiere_name(self):
        signatur = "Max Mustermann	\nProduct Engineering\nHead of Mastersystems\nSuper Muster Motive GmbH 	" \
                   "\nMuster-Zufall-Straße 6\nD-21102 Kiel /Germany	\nfon: +49 421 3949-2257" \
                   "\nmobil: +49 112 2672085\nmail: maximilian.must@mu-wf.com\nweb: http://www.mu-wf.com	"
        kunde = kundenkartei.Kundenkartei(signatur)
        extraktor.extrahiere_name(kunde)
        self.assertEqual(kunde.ansprechpartner, "Max Mustermann")
        self.assertEqual(kunde.radierer, ["Max Mustermann"])

    def test_extrahiere_firma(self):
        signatur = "Max Mustermann	\nProduct Engineering\nHead of Mastersystems\nSuper Muster Motive GmbH" \
                   "\nMuster-Zufall-Straße 6\nD-21102 Kiel /Germany	\nfon: +49 421 3949-2257" \
                   "\nmobil: +49 112 2672085\nmail: maximilian.must@mu-wf.com\nweb: http://www.mu-wf.com	"
        kunde = kundenkartei.Kundenkartei(signatur)
        extraktor.extrahiere_firma(kunde)
        self.assertEqual(kunde.firma, "Super Muster Motive GmbH")
        self.assertEqual(kunde.radierer, ["Super Muster Motive GmbH"])

    def test_extrahiere_strasse(self):
        signatur = "Max Mustermann	\nProduct Engineering\nHead of Mastersystems\nSuper Muster Motive GmbH 	" \
                   "\nMuster-Zufall-Straße 6\nD-21102 Kiel /Germany	\nfon: +49 421 3949-2257" \
                   "\nmobil: +49 112 2672085\nmail: maximilian.must@mu-wf.com\nweb: http://www.mu-wf.com	"
        kunde = kundenkartei.Kundenkartei(signatur)
        extraktor.extrahiere_strasse(kunde)
        self.assertEqual(kunde.strasse, "Muster-Zufall-Straße 6")
        self.assertEqual(kunde.radierer, ["Muster-Zufall-Straße 6"])

    def test_extrahiere_ortschaft(self):
        signatur = "Max Mustermann	\nProduct Engineering		\nHead of Mastersystems			" \
                   "\nSuper Muster Motive GmbH 	\nMuster-Zufall-Straße 6			" \
                   "\nD-21102 Kiel /Germany	\nmail: maximilian.must@mu-wf.com		\nweb: http://www.mu-wf.com	"
        kunde = kundenkartei.Kundenkartei(signatur)
        extraktor.extrahiere_ortschaft(kunde)
        self.assertEqual(kunde.land, "Deutschland")
        self.assertEqual(kunde.plz, "21102")
        self.assertEqual(kunde.ortschaft, "Kiel")
        self.assertEqual(kunde.radierer, ["21102", "Kiel"])

    def test_extrahiere_email(self):
        signatur = "Max Mustermann	\nProduct Engineering		\nHead of Mastersystems			\nSuper Muster Motive GmbH 	" \
                   "		\nMuster-Zufall-Straße 6			\nD-21102 Kiel /Germany		\nfon: +49 421 3949-2257			" \
                   "\nmobil: +49 112 2672085			\nmail: maximilian.must@mu-wf.com		\nweb: http://www.mu-wf.com	"
        kunde = kundenkartei.Kundenkartei(signatur)
        extraktor.extrahiere_email(kunde)
        self.assertEqual(kunde.email, "maximilian.must@mu-wf.com")
        self.assertEqual(kunde.radierer, ["maximilian.must@mu-wf.com"])

    def test_extrahiere_url(self):
        signatur = "Max Mustermann	\nProduct Engineering		\nHead of Mastersystems			" \
                   "\nSuper Muster Motive GmbH 		\nMuster-Zufall-Straße 6			\nD-21102 Kiel /Germany		" \
                   "\nfon: +49 421 3949-2257	\nmobil: +49 112 2672085	\nweb: http://www.mu-wf.com	"
        kunde = kundenkartei.Kundenkartei(signatur)
        extraktor.extrahiere_url(kunde)
        self.assertEqual(kunde.webseite, "http://www.mu-wf.com")

    def test_extrahiere_nummern(self):
        signatur = "Max Mustermann	\nProduct Engineering		\nHead of Mastersystems			" \
                   "\nSuper Muster Motive GmbH 		\nMuster-Zufall-Straße 6			\nD-21102 Kiel /Germany		" \
                   "\nfon: +49 421 3949-2257	\nmobil: +49 112 2672085	\nweb: http://www.mu-wf.com	"
        kunde = kundenkartei.Kundenkartei(signatur)
        extraktor.extrahiere_nummern(kunde)
        self.assertEqual(kunde.nummern, ["fon: +49 421 3949-2257"])
        self.assertEqual(kunde.radierer,  ["fon: +49 421 3949-2257"])


if __name__ == "__main__":
    unittest.main()
