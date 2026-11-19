#!/usr/bin/env python3
"""Erzeugt symbole/allgemein/kopfzeilen/: Kopfzeilen-Hintergründe und einzelne Wertfelder für die Außenwerte.

Kopfzeile_{hell,dunkel,zweizeilig}  1600 × 90, ohne Schrift. Texte, Werte und Legende-Beschriftung kommen als
                                     Niagara-Labels darüber; die Logos (transparent) auf die Logo-Felder.
Kopfzeilenwert_{Temperatur,Feuchte,Luftdruck,CO2}_{hell,dunkel,zweizeilig}
                                     ein Feld je Außenwert mit Symbol, passend zur jeweiligen Kopfzeile;
                                     nur die Werte anlegen, die es in der Anlage gibt.
  hell        Chip 124 × 22, Symbol links, Wert-Label rechts daneben (x = 24 … 120)
  dunkel      Kachel 100 × 58, Symbol oben links, Bezeichnung oben (y = 5 … 21), Wert unten (y = 25 … 51)
  zweizeilig  130 × 20 transparent, Symbol links, Wert-Label rechts daneben (x = 12 … 130), für die graue Statuszeile
Aufruf: python tools/kopfzeilen.py
"""
from pathlib import Path

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "allgemein" / "kopfzeilen"
W, H = 1600, 90

SYMBOLE = {   # um (0, 0), ca. 12 × 12; {g} = Linienfarbe, {d} = Zeiger
    "Temperatur": ('<path d="M0,-6 a2,2 0 0 1 2,2 v5 a3.5,3.5 0 1 1 -4,0 v-5 a2,2 0 0 1 2,-2 Z" fill="none" stroke="{g}" '
                   'stroke-width="1.3"/><circle cx="0" cy="3.5" r="1.8" fill="#F04F46"/>'),
    "Feuchte": '<path d="M0,-6 C2.5,-2.5 4,-0.5 4,1.8 a4,4 0 0 1 -8,0 C-4,-0.5 -2.5,-2.5 0,-6 Z" fill="#4A86D4"/>',
    "Luftdruck": ('<path d="M-5.5,3 a5.5,5.5 0 1 1 11,0" fill="none" stroke="{g}" stroke-width="1.3"/>'
                  '<path d="M0,3 L2.5,-1.5" stroke="{d}" stroke-width="1.4" stroke-linecap="round"/>'),
    "CO2": ('<circle cx="-2.5" cy="1" r="3.3" fill="none" stroke="{g}" stroke-width="1.3"/>'
            '<circle cx="3" cy="-2" r="2.4" fill="none" stroke="{g}" stroke-width="1.3"/>'),
}


def symbol(name: str, x: float, y: float, g: str = "#6B7480", d: str = "#2B3440") -> str:
    return f'<g transform="translate({x} {y})">{SYMBOLE[name].format(g=g, d=d)}</g>'


def datei(w: int, h: int, titel: str, inhalt: str, defs: str = "") -> str:
    d = f"<defs>{defs}</defs>" if defs else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">\n'
            f'  <title>{titel}</title>\n  {d}{inhalt}\n</svg>\n')


def kopf_hell() -> str:
    defs = ('<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F4F5F7"/>'
            '<stop offset="1" stop-color="#E3E6EA"/></linearGradient>')
    s = (f'<rect width="{W}" height="{H}" fill="url(#bg)"/><rect y="{H - 3}" width="{W}" height="3" fill="#8A94A0"/>'
         '<rect x="20" y="15" width="160" height="58" rx="6" fill="#FFFFFF" fill-opacity="0.75" stroke="#CDD2D8" stroke-width="1"/>'
         '<rect x="1405" y="9" width="175" height="46" rx="6" fill="#FFFFFF" fill-opacity="0.75" stroke="#CDD2D8" stroke-width="1"/>'
         '<rect x="749.5" y="16" width="1" height="58" fill="#B9BFC6"/>'
         '<rect x="1500" y="61" width="80" height="20" rx="4" fill="#EFEFEF" stroke="#9A9A9A" stroke-width="1"/>')
    return datei(W, H, "Kopfzeile hell", s, defs)


def kopf_dunkel() -> str:
    s = (f'<rect width="{W}" height="{H}" fill="#2B3138"/><rect y="{H - 3}" width="{W}" height="3" fill="#4A86D4"/>'
         '<rect x="20" y="15" width="160" height="58" rx="6" fill="#FFFFFF"/>'
         '<rect x="1320" y="15" width="175" height="58" rx="6" fill="#FFFFFF"/>'
         '<rect x="1505" y="32" width="75" height="24" rx="4" fill="#3F4750" stroke="#59636E" stroke-width="1"/>')
    return datei(W, H, "Kopfzeile dunkel", s)


def kopf_zweizeilig() -> str:
    defs = ('<linearGradient id="ak" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F04F46"/>'
            '<stop offset="0.3" stop-color="#F29A38"/><stop offset="0.6" stop-color="#94C652"/>'
            '<stop offset="1" stop-color="#4A86D4"/></linearGradient>')
    s = (f'<rect width="{W}" height="{H}" fill="#FFFFFF"/><rect width="{W}" height="24" fill="#E9ECEF"/>'
         f'<rect y="23.5" width="{W}" height="1" fill="#D2D6DB"/><rect y="{H - 3}" width="{W}" height="3" fill="url(#ak)"/>'
         '<rect x="20" y="31" width="160" height="50" rx="6" fill="#FFFFFF"/>'
         '<rect x="1320" y="31" width="175" height="50" rx="6" fill="#FFFFFF"/>'
         '<rect x="1505" y="44" width="75" height="24" rx="4" fill="#EFEFEF" stroke="#9A9A9A" stroke-width="1"/>')
    return datei(W, H, "Kopfzeile zweizeilig", s, defs)


def wert(name: str, stil: str) -> str:
    titel = f"Kopfzeilenwert {name}, {stil}"
    if stil == "hell":
        return datei(124, 22, titel, '<rect x="0.5" y="0.5" width="123" height="21" rx="10.5" fill="#FFFFFF" stroke="#CDD2D8" '
                     f'stroke-width="1"/>{symbol(name, 13, 11)}')
    if stil == "dunkel":
        return datei(100, 58, titel, f'<rect width="100" height="58" rx="8" fill="#353C44"/>'
                     f'{symbol(name, 12, 13, g="#AEB6C0", d="#F0F2F4")}')
    return datei(130, 20, titel, symbol(name, 6, 10))


def main() -> None:
    ZIEL.mkdir(parents=True, exist_ok=True)
    dateien = {"Kopfzeile_hell.svg": kopf_hell(), "Kopfzeile_dunkel.svg": kopf_dunkel(),
               "Kopfzeile_zweizeilig.svg": kopf_zweizeilig()}
    for name in SYMBOLE:
        for stil in ("hell", "dunkel", "zweizeilig"):
            dateien[f"Kopfzeilenwert_{name}_{stil}.svg"] = wert(name, stil)
    for n, inhalt in dateien.items():
        with open(ZIEL / n, "w", encoding="utf-8", newline="\n") as f:
            f.write(inhalt)
        print(n)


if __name__ == "__main__":
    main()
