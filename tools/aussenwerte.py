#!/usr/bin/env python3
"""Erzeugt symbole/anzeigen/aussenwerte/Aussen{temperatur,feuchte}_<Stil>[_20].svg.

Kleine Symbole, die links vor die Wertfelder für Außentemperatur und Außenfeuchte gesetzt werden.
Thermometer und Tropfen, statisch, ohne clipPath und ohne Animation. Zwei Größen:
16 × 16 (passt in die Zeilenhöhe der Wertfelder) und 20 × 20 (Zusatz _20), gleiche Zeichnung.

Stil  grau       nur graue Kontur #808080, Flüssigkeit grau (wie die übrigen Konturen)
      flach      Thermometer rot, Tropfen blau, flach
      plastisch  wie flach, mit Verlauf und Glanzlicht
Zustandsabhängig (Umschaltung per image-Binding, alle Varianten gleich groß, gleiche Lage):
      Aussentemperatur_{frost,kalt,mild,warm,heiss}  Füllstand und Farbe nach Temperatur
      Aussenfeuchte_{trocken,normal,feucht}          Füllstand des Tropfens nach Feuchte

Aufruf: python tools/aussenwerte.py [Zielordner]
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KONTUR = "#808080"
ROT, BLAU = "#F04F46", "#4A86D4"     # Vorlauf rot / Rücklauf blau wie bei Rohren und Heizkreis

# Thermometer (Koordinaten im 16er-Raster): Röhre, Kugel, Flüssigkeitssäule
ROEHRE = '<rect x="5.5" y="1" width="5" height="10.5" rx="2.5" fill="#FFFFFF" stroke="#808080" stroke-width="1.2"/>'
SKALA = ('<path d="M10.5,4 h-1.4 M10.5,6.5 h-1.4 M10.5,9 h-1.4" stroke="#808080" stroke-width=".7"/>')


def thermometer(farbe: str, oben: float, kugel: str | None = None) -> str:
    """Säule von y = oben bis in die Kugel; die Säule überdeckt die Kugelkontur am Übergang."""
    return (ROEHRE + SKALA
            + f'<circle cx="8" cy="12" r="3" fill="{kugel or farbe}" stroke="{KONTUR}" stroke-width="1.2"/>'
            + f'<rect x="7.1" y="{oben}" width="1.8" height="{12 - oben:.2f}" rx=".9" fill="{farbe}"/>')


# Tropfen: Spitze (8, 1.5), Bézier bis (3, 10.5), unten Halbkreis r = 5 um (8, 10.5)
TROPFEN = "M8,1.5 C8,1.5 3,7.5 3,10.5 A5,5 0 0 0 13,10.5 C13,7.5 8,1.5 8,1.5 Z"
P0, P1, P2, P3 = (8, 1.5), (8, 1.5), (3, 7.5), (3, 10.5)


def _bez(t: float, a, b, c, d):
    u = 1 - t
    return tuple(u ** 3 * a[i] + 3 * u * u * t * b[i] + 3 * u * t * t * c[i] + t ** 3 * d[i] for i in (0, 1))


def _teil_ab(t: float):
    """Teilkurve der linken Tropfenseite von t bis zum Ende (de Casteljau)."""
    lerp = lambda p, q: (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    a, b, c = lerp(P0, P1), lerp(P1, P2), lerp(P2, P3)
    d, e = lerp(a, b), lerp(b, c)
    f = lerp(d, e)
    return f, e, c, P3


def f(x: float) -> str:
    return f"{x:.2f}".rstrip("0").rstrip(".")


def wasser(y: float) -> str:
    """Füllfläche des Tropfens bis zur Höhe y (ohne clipPath, als eigener Pfad)."""
    if y >= 10.5:
        dx = (25 - (y - 10.5) ** 2) ** 0.5
        return f"M{f(8 - dx)},{f(y)} A5,5 0 0 0 {f(8 + dx)},{f(y)} Z"
    lo, hi = 0.0, 1.0
    for _ in range(40):                       # t suchen, bei dem die linke Seite die Höhe y hat
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if _bez(mid, P0, P1, P2, P3)[1] < y else (lo, mid)
    s, c1, c2, e = _teil_ab(lo)
    spiegel = lambda p: (16 - p[0], p[1])
    r_s, r_c1, r_c2 = spiegel(s), spiegel(c1), spiegel(c2)
    return (f"M{f(s[0])},{f(s[1])} C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(e[0])},{f(e[1])} "
            f"A5,5 0 0 0 13,10.5 C{f(r_c2[0])},{f(r_c2[1])} {f(r_c1[0])},{f(r_c1[1])} {f(r_s[0])},{f(r_s[1])} Z")


def tropfen(fuellung: str, glanz: str = "#FFFFFF", wasserhoehe: float | None = None, wasserfarbe: str = BLAU) -> str:
    s = f'<path d="{TROPFEN}" fill="{fuellung}"/>'
    if wasserhoehe is not None:
        s += f'<path d="{wasser(wasserhoehe)}" fill="{wasserfarbe}"/>'
    s += f'<path d="{TROPFEN}" fill="none" stroke="{KONTUR}" stroke-width="1.2" stroke-linejoin="round"/>'
    s += f'<path d="M5.4,10.6 a2.6,2.6 0 0 0 2.2,2.5" fill="none" stroke="{glanz}" stroke-width="1.1" stroke-linecap="round"/>'
    return s


GRAU_T = thermometer(KONTUR, 5)
GRAU_D = tropfen("#FFFFFF", glanz=KONTUR)
FLACH_T = thermometer(ROT, 5)
FLACH_D = tropfen(BLAU)
PLAST_DEFS = ('<defs><linearGradient id="gT" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F7A19B"/>'
              '<stop offset="1" stop-color="#B8231C"/></linearGradient>'
              '<linearGradient id="gS" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F7A19B"/>'
              f'<stop offset=".5" stop-color="{ROT}"/><stop offset="1" stop-color="#B8231C"/></linearGradient>'
              '<linearGradient id="gR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF"/>'
              '<stop offset="1" stop-color="#E4E4E4"/></linearGradient>'
              '<linearGradient id="gD" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#A9C8EE"/>'
              '<stop offset=".55" stop-color="#4A86D4"/><stop offset="1" stop-color="#2A5DA0"/></linearGradient></defs>')
PLAST_T = (thermometer("url(#gS)", 5, kugel="url(#gT)").replace('fill="#FFFFFF" stroke', 'fill="url(#gR)" stroke', 1)
           + '<circle cx="7" cy="11" r=".9" fill="#FFFFFF" opacity=".75"/>'
           + '<rect x="6.4" y="2.4" width=".8" height="6" rx=".4" fill="#FFFFFF" opacity=".9"/>')
PLAST_D = (tropfen("url(#gD)", glanz="#FFFFFF")
           + '<ellipse cx="6.2" cy="8.6" rx=".9" ry="1.5" fill="#FFFFFF" opacity=".75" transform="rotate(20 6.2 8.6)"/>')

# Zustandsabhängig: (Name, Farbe, Oberkante der Säule, Titel)
TEMPERATUR = [
    ("frost", "#2A5DA0", 9.4, "Frost (unter 0 °C)"),
    ("kalt", "#7CA6DE", 7.8, "kalt (0 bis 10 °C)"),
    ("mild", "#5DA84E", 6.2, "mild (10 bis 20 °C)"),
    ("warm", "#F0A030", 4.6, "warm (20 bis 28 °C)"),
    ("heiss", ROT, 3, "heiß (über 28 °C)"),
]
FEUCHTE = [
    ("trocken", 12.2, "trocken (unter 35 %rF)"),
    ("normal", 8.6, "normal (35 bis 70 %rF)"),
    ("feucht", 4.4, "feucht (über 70 %rF)"),
]


def datei(groesse: int, titel: str, inhalt: str, defs: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{groesse}" height="{groesse}" viewBox="0 0 16 16" role="img">\n'
            f'  <title>{titel}</title>\n  {defs}{inhalt}\n</svg>\n')


def symbole() -> dict[str, tuple[str, str, str]]:
    s = {
        "Aussentemperatur_grau": ("Außentemperatur, grau", GRAU_T, ""),
        "Aussenfeuchte_grau": ("Außenfeuchte, grau", GRAU_D, ""),
        "Aussentemperatur_flach": ("Außentemperatur, flach", FLACH_T, ""),
        "Aussenfeuchte_flach": ("Außenfeuchte, flach", FLACH_D, ""),
        "Aussentemperatur_plastisch": ("Außentemperatur, plastisch", PLAST_T, PLAST_DEFS),
        "Aussenfeuchte_plastisch": ("Außenfeuchte, plastisch", PLAST_D, PLAST_DEFS),
    }
    for name, farbe, oben, titel in TEMPERATUR:
        s[f"Aussentemperatur_{name}"] = (f"Außentemperatur, {titel}", thermometer(farbe, oben), "")
    for name, hoehe, titel in FEUCHTE:
        s[f"Aussenfeuchte_{name}"] = (f"Außenfeuchte, {titel}", tropfen("#FFFFFF", glanz="#FFFFFF", wasserhoehe=hoehe), "")
    return s


def main() -> None:
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "symbole" / "anzeigen" / "aussenwerte"
    ziel.mkdir(parents=True, exist_ok=True)
    for name, (titel, inhalt, defs) in symbole().items():
        for groesse, zusatz in ((16, ""), (20, "_20")):
            p = ziel / f"{name}{zusatz}.svg"
            with open(p, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(datei(groesse, titel, inhalt, defs))
            print(p.name)


if __name__ == "__main__":
    main()
