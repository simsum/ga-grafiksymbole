#!/usr/bin/env python3
"""Erzeugt einzelne Flanschanschlüsse unter symbole/hydraulik/anschluesse/ und Fun-Varianten (undicht)
unter symbole/fun/hydraulik/anschluesse/.

Alle Symbole 24 × 24 (Fun: 24 × 36, gleiche Lage oben, unten 12 px Platz für den fallenden Tropfen).

  Flansch_Geraet_<farbe>_<richtung>  Geräteflansch wie an der Wärmepumpe: grauer Hals, farbige Flanschplatte.
                                     <richtung> = Seite, zu der das Rohr abgeht (unten, oben, links, rechts);
                                     das Rohr (12 px) setzt mittig an der Außenkante der Platte an.
  Flansch_Platte_<achse>             einzelne graue Flanschplatte quer zur Rohrachse
  Flansch_Paar_<achse>               zwei graue Flanschplatten mit Schrauben (Rohrverbindung)
                                     <achse> = Richtung der Rohrachse (waagerecht, senkrecht); Rohrachse durch die Mitte

  Fun_Flansch_*_undicht              dieselben Formen mit brauner Fun-Kontur; an der tiefsten Kante bildet sich
                                     ein Wassertropfen, fällt und zerplatzt (SMIL, 2,4 s)

Aufruf: python tools/flansche.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZIEL = ROOT / "symbole" / "hydraulik" / "anschluesse"
ZIEL_FUN = ROOT / "symbole" / "fun" / "hydraulik" / "anschluesse"

GRAU, GRAU_K = "#8C8C8C", "#6B6B6B"
BRAUN = "#3B2412"
FARBEN = {  # Flanschfarben wie an Wärmepumpe und Mehrleitermaschine
    "rot": "#D7302B",        # Heizung Vorlauf
    "orange": "#F29A38",     # Heizung Rücklauf
    "blau": "#2E6BC2",       # Kälte Vorlauf
    "hellblau": "#7CA6DE",   # Kälte Rücklauf
    "gruen": "#6BB33A",      # Kaltwasser
    "grau": "#9A9A9A",       # neutral
}
DREHUNG = {"unten": 0, "links": 90, "oben": 180, "rechts": 270}
ACHSE = {"senkrecht": 0, "waagerecht": 90}

# Tiefster Punkt der Form nach Drehung (dort tropft es): x, y im 24er-Feld
TROPF_GERAET = {"unten": (17, 16), "oben": (18.5, 14), "links": (11, 20), "rechts": (13, 20)}
TROPF_PLATTE = {"senkrecht": (18.5, 14.5), "waagerecht": (12, 21)}
TROPF_PAAR = {"senkrecht": (18.5, 16), "waagerecht": (12, 21)}


def geraet(platte: str, kontur: str, sw: float = 1) -> str:
    """Richtung „unten“: Hals oben (Gerätekante y = 5), Platte darunter, Rohr setzt bei y = 16 an."""
    return (f'<rect x="9" y="5" width="6" height="5" fill="{GRAU}" stroke="{kontur}" stroke-width="{sw}"/>'
            f'<rect x="4" y="10" width="16" height="6" rx="1" fill="{platte}" stroke="{kontur}" stroke-width="{sw}"/>')


def platte(kontur: str, sw: float = 1) -> str:
    """Achse senkrecht: Platte waagerecht quer zur Rohrachse, Mitte bei y = 12."""
    return f'<rect x="3" y="9.5" width="18" height="5" rx="1" fill="{GRAU}" stroke="{kontur}" stroke-width="{sw}"/>'


def paar(kontur: str, sw: float = 1) -> str:
    """Achse senkrecht: zwei Platten mit Fuge bei y = 12, Schrauben an den Enden."""
    return (f'<g fill="{GRAU}" stroke="{kontur}" stroke-width="{sw}"><rect x="3" y="8" width="18" height="3.5" rx=".8"/>'
            f'<rect x="3" y="12.5" width="18" height="3.5" rx=".8"/></g>'
            f'<g fill="{kontur}"><circle cx="5.5" cy="12" r=".9"/><circle cx="18.5" cy="12" r=".9"/></g>')


def tropfen(x: float, y: float) -> str:
    """Tropfen wächst an (x, y), fällt bis y = 33 und zerplatzt; Ruhebild ohne SMIL: hängender Tropfen."""
    tropf = (f'<path d="M0,0 C1.6,2.2 2.4,3.4 2.4,4.4 a2.4,2.4 0 0 1 -4.8,0 C-2.4,3.4 -1.6,2.2 0,0 Z" '
             f'fill="#5DB8F0" stroke="{BRAUN}" stroke-width="1" stroke-linejoin="round"/>'
             f'<circle cx="-0.8" cy="3.9" r=".7" fill="#FFFFFF"/>')
    fall = 33 - 7 - y
    return (f'<g transform="translate({x} {y})">'
            f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 {fall:.1f};0 {fall:.1f}" '
            f'keyTimes="0;0.55;0.8;1" dur="2.4s" repeatCount="indefinite"/>'
            f'<g><animateTransform attributeName="transform" type="scale" values="0.2;1;1;1" keyTimes="0;0.55;0.8;1" '
            f'dur="2.4s" repeatCount="indefinite"/>'
            f'<g><animate attributeName="opacity" values="1;1;1;0;0" keyTimes="0;0.55;0.79;0.8;1" dur="2.4s" repeatCount="indefinite"/>'
            f'{tropf}</g></g></g></g>'
            # Spritzer am Boden
            f'<g transform="translate({x} 33)" fill="none" stroke="#5DB8F0" stroke-width="1.2" stroke-linecap="round" opacity="0">'
            f'<animate attributeName="opacity" values="0;0;1;0" keyTimes="0;0.8;0.86;1" dur="2.4s" repeatCount="indefinite"/>'
            f'<path d="M-4,-1 l-1.5,-2 M0,-2 v-2.5 M4,-1 l1.5,-2"/><path d="M-3.5,0.5 h7" stroke="{BRAUN}" stroke-width="1"/></g>')


def datei(breite: int, hoehe: int, titel: str, inhalt: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}" viewBox="0 0 {breite} {hoehe}" '
            f'role="img" aria-labelledby="title">\n  <title id="title">{titel}</title>\n  {inhalt}\n</svg>\n')


def schreiben(ordner: Path, name: str, text: str) -> None:
    ordner.mkdir(parents=True, exist_ok=True)
    (ordner / f"{name}.svg").write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    n = 0
    for farbe, c in FARBEN.items():
        for richtung, w in DREHUNG.items():
            schreiben(ZIEL, f"Flansch_Geraet_{farbe}_{richtung}",
                      datei(24, 24, f"Geräteflansch {farbe}, Rohr nach {richtung}",
                            f'<g transform="rotate({w} 12 12)">{geraet(c, GRAU_K)}</g>'))
            n += 1
    for achse, w in ACHSE.items():
        schreiben(ZIEL, f"Flansch_Platte_{achse}",
                  datei(24, 24, f"Flanschplatte, Rohrachse {achse}", f'<g transform="rotate({w} 12 12)">{platte(GRAU_K)}</g>'))
        schreiben(ZIEL, f"Flansch_Paar_{achse}",
                  datei(24, 24, f"Flanschpaar, Rohrachse {achse}", f'<g transform="rotate({w} 12 12)">{paar(GRAU_K)}</g>'))
        n += 2
    # Fun: undichte Flansche mit Tropfen
    for richtung, w in DREHUNG.items():
        schreiben(ZIEL_FUN, f"Fun_Flansch_Geraet_{richtung}_undicht",
                  datei(24, 36, f"Fun-Geräteflansch undicht, Rohr nach {richtung}",
                        f'<g transform="rotate({w} 12 12)">{geraet(FARBEN["grau"], BRAUN, 1.3)}</g>{tropfen(*TROPF_GERAET[richtung])}'))
        n += 1
    for achse, w in ACHSE.items():
        schreiben(ZIEL_FUN, f"Fun_Flansch_Platte_{achse}_undicht",
                  datei(24, 36, f"Fun-Flanschplatte undicht, Rohrachse {achse}",
                        f'<g transform="rotate({w} 12 12)">{platte(BRAUN, 1.3)}</g>{tropfen(*TROPF_PLATTE[achse])}'))
        schreiben(ZIEL_FUN, f"Fun_Flansch_Paar_{achse}_undicht",
                  datei(24, 36, f"Fun-Flanschpaar undicht, Rohrachse {achse}",
                        f'<g transform="rotate({w} 12 12)">{paar(BRAUN, 1.3)}</g>{tropfen(*TROPF_PAAR[achse])}'))
        n += 2
    print(f"{n} Symbole erzeugt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
