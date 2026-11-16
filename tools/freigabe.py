#!/usr/bin/env python3
"""Erzeugt symbole/anzeigen/freigabe/Freigabe_<Variante>_{an,aus}.svg.

Kleine, unaufdringliche Anzeigen für „Freigabe“ (gelb, _an) und „keine Freigabe“ (grau, _aus),
24 × 24, Farben aus tools/zustandsfarben.py (dieselben wie bei den Pumpen). Fünf Varianten:

  Haken     runder Knopf, weißer Haken / weißer Strich
  Schalter  Kippschalter, Knopf rechts (frei) / links (gesperrt)
  Schloss   Schloss offen / geschlossen
  Ein       Ein-Symbol (Power) im runden Knopf
  Punkt     Punkt mit Ring, am dezentesten

Statisch, ohne Animation und ohne clipPath. Aufruf: python tools/freigabe.py [Zielordner]
"""
import sys
from pathlib import Path

from zustandsfarben import AUS, FREIGABE

ROOT = Path(__file__).resolve().parent.parent
G = 24
TITEL = {"an": "Freigabe", "aus": "keine Freigabe"}

KREIS = '<circle cx="12" cy="12" r="10.2" fill="url(#g)" stroke="K" stroke-width="1.4"/>'
HAKEN = "M7.2,12.4 L10.4,15.4 L16.8,8.8"
SCHLOSS_KOERPER = ('<rect x="5" y="10.5" width="14" height="10.5" rx="2" fill="url(#g)" stroke="K" stroke-width="1.4"/>'
                   '<circle cx="12" cy="15" r="1.5" fill="K"/><rect x="11.3" y="15.5" width="1.4" height="3" rx=".7" fill="K"/>')
EIN = ('<path d="M8.6,8.6 a5,5 0 1 0 6.8,0" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>'
       '<path d="M12,6.2 V11.6" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>')
PUNKT = ('<circle cx="12" cy="12" r="9.5" fill="none" stroke="K" stroke-width="1.4" opacity=".7"/>'
         '<circle cx="12" cy="12" r="5.6" fill="url(#g)" stroke="K" stroke-width="1.2"/>')
SCHALTER = '<rect x="1.5" y="6" width="21" height="12" rx="6" fill="url(#g)" stroke="K" stroke-width="1.4"/>'

VARIANTEN = {
    "Haken": {
        "an": KREIS + f'<path d="{HAKEN}" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
                      f'<path d="{HAKEN}" fill="none" stroke="K" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" opacity=".55"/>',
        "aus": KREIS + '<path d="M7.5,12 H16.5" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round"/>',
    },
    "Schalter": {
        "an": SCHALTER + '<circle cx="16.5" cy="12" r="4.4" fill="#FFFFFF" stroke="K" stroke-width="1.2"/>',
        "aus": SCHALTER + '<circle cx="7.5" cy="12" r="4.4" fill="#FFFFFF" stroke="K" stroke-width="1.2"/>',
    },
    "Schloss": {
        "an": '<path d="M8,9 V4 a4,4 0 0 1 8,0 V5" fill="none" stroke="K" stroke-width="2" stroke-linecap="round"/>' + SCHLOSS_KOERPER,
        "aus": '<path d="M8,10.5 V7.5 a4,4 0 0 1 8,0 V10.5" fill="none" stroke="K" stroke-width="2"/>' + SCHLOSS_KOERPER,
    },
    "Ein": {"an": KREIS + EIN, "aus": KREIS + EIN},
    "Punkt": {"an": PUNKT, "aus": PUNKT},
}


def svg(variante: str, zustand: str) -> str:
    oben, unten, kontur = FREIGABE if zustand == "an" else AUS
    inhalt = VARIANTEN[variante][zustand].replace('"K"', f'"{kontur}"')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{G}" height="{G}" viewBox="0 0 {G} {G}" role="img" aria-labelledby="title">\n'
            f'  <title id="title">{TITEL[zustand]} ({variante})</title>\n'
            f'  <defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{oben}"/>'
            f'<stop offset="1" stop-color="{unten}"/></linearGradient></defs>\n'
            f'  {inhalt}\n</svg>\n')


def main() -> int:
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "symbole" / "anzeigen" / "freigabe"
    ziel.mkdir(parents=True, exist_ok=True)
    for variante in VARIANTEN:
        for zustand in ("an", "aus"):
            p = ziel / f"Freigabe_{variante}_{zustand}.svg"
            p.write_text(svg(variante, zustand), encoding="utf-8", newline="\n")
            print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
