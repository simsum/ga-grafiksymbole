"""Einheitliche Zustandsfarben für alle Symbole mit Betriebszustand (siehe docs/STYLEGUIDE.md, „Zustandsfarben“).

Je Zustand: (Verlauf oben, Verlauf unten, Kontur). Der Verlauf läuft senkrecht von oben nach unten.
Erzeuger-Skripte importieren diese Werte, statt eigene Farben festzulegen.
"""

AUS = ("#EDEDED", "#A6A6A6", "#808080")        # grau:  aus / keine Freigabe
FREIGABE = ("#FFEB8F", "#E3B200", "#A88400")   # gelb:  Freigabe / bereit
BETRIEB = ("#A8DC96", "#3E9A3A", "#2F7A2C")    # grün:  Betrieb / an
STOERUNG = ("#F5A3A0", "#D7302B", "#9E1F1B")   # rot:   Störung

# Zuordnung zu den Zustandsnamen in Dateinamen
ZUSTAENDE = {"aus": AUS, "freigabe": FREIGABE, "an": BETRIEB, "stoerung": STOERUNG}
