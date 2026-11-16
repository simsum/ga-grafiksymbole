"""Erzeugt symbole/fun/Fun_Pumpe_{richtung}_{zustand}.svg (40 × 40, wie die Pumpen unter symbole/hydraulik).

Basis ist das Pumpensymbol aus pumpe.py (im Hintergrund, mit brauner Fun-Kontur), davor je Zustand
eine kleine Cartoon-Animation (SMIL):
  _aus        zwei „z“ steigen auf (schläft)
  _freigabe   Funken blinken (bereit)
  _an         blaue Wassertropfen spritzen seitlich ab
  _stoerung   Pumpe wackelt, Dampfwolken steigen auf, Schweißperlen spritzen ab
Aufruf: python tools/fun_pumpe.py
"""
from pathlib import Path

import pumpe

BRAUN = "#3B2412"


def wolke(cx: float, beginn: float, drift: float) -> str:
    return f'''  <g opacity="1"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.2;0.7;1" dur="1.8s" begin="{beginn}s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" values="0 0;{drift} -8" dur="1.8s" begin="{beginn}s" repeatCount="indefinite"/>
    <path d="M{cx - 2.5},11 a2.6,2.6 0 0 1 2.5,-3.4 a3.1,3.1 0 0 1 5,1 a2.4,2.4 0 0 1 -0.6,4.5 h-6 a2,2 0 0 1 -0.9,-2.1 z" fill="#FFFFFF" stroke="{BRAUN}" stroke-width="1.4" stroke-linejoin="round"/></g>'''


def perle(x: float, y: float, dx: float, dy: float, beginn: float, farbe: str = "#8FD3F5") -> str:
    return f'''  <g opacity="1"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.7;1" dur="1.4s" begin="{beginn}s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" values="0 0;{dx} {dy}" dur="1.4s" begin="{beginn}s" repeatCount="indefinite"/>
    <path d="M{x},{y - 3} q2.7,3.3 0,5.4 q-2.7,-2.1 0,-5.4 z" fill="{farbe}" stroke="{BRAUN}" stroke-width="1.1" stroke-linejoin="round"/>
    <path d="M{x - 0.8},{y} q0,-1.2 0.8,-1.7" fill="none" stroke="#FFFFFF" stroke-width="0.8" stroke-linecap="round"/></g>'''


def zeta(x: float, y: float, groesse: float, beginn: float) -> str:
    g = groesse
    return f'''  <g opacity="1"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.2;0.7;1" dur="2.4s" begin="{beginn}s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" values="0 0;4 -9" dur="2.4s" begin="{beginn}s" repeatCount="indefinite"/>
    <path d="M{x},{y} h{g} l-{g},{g} h{g}" fill="none" stroke="{BRAUN}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M{x},{y} h{g} l-{g},{g} h{g}" fill="none" stroke="#FFFFFF" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></g>'''


def funke(x: float, y: float, r: float, beginn: float) -> str:
    return f'''  <path d="M{x},{y - r} L{x + r * 0.28},{y - r * 0.28} L{x + r},{y} L{x + r * 0.28},{y + r * 0.28} L{x},{y + r} L{x - r * 0.28},{y + r * 0.28} L{x - r},{y} L{x - r * 0.28},{y - r * 0.28} Z" fill="#FFF3A0" stroke="{BRAUN}" stroke-width="1.1" stroke-linejoin="round">
    <animate attributeName="opacity" values="0.15;1;0.15" dur="1.2s" begin="{beginn}s" repeatCount="indefinite"/></path>'''


EFFEKTE = {
    "aus": [zeta(25, 11, 4, 0), zeta(29, 7, 3, 1.2)],
    "freigabe": [funke(8, 9, 4.5, 0), funke(32, 7, 4, 0.4), funke(34, 31, 3.5, 0.8), funke(7, 32, 3, 0.2)],
    "an": [perle(5, 17, -7, -3, 0), perle(35, 17, 7, -3, 0.35), perle(5, 25, -7, 1, 0.7), perle(35, 25, 7, 1, 1.0)],
    "stoerung": [wolke(14, 0, -2), wolke(26, 0.9, 2),
                 perle(6, 21, -3, 6, 0), perle(34, 19, 3, 6, 0.5), perle(33, 30, 3, 5, 1.0), perle(8, 31, -3, 5, 0.25)],
}
WACKELN = ('<animateTransform attributeName="transform" type="translate" values="0 0;-0.7 0;0.7 0;-0.7 0;0.7 0;0 0;0 0" '
           'dur="0.8s" repeatCount="indefinite"/>')


def svg(richtung: str, zustand: str) -> str:
    zeilen = pumpe.svg(richtung, zustand).rstrip("\n").split("\n")
    zeilen[0] = zeilen[0].replace('role="img" aria-labelledby="title"', 'role="img" aria-labelledby="title"')
    zeilen[1] = zeilen[1].replace("<title id=\"title\">Pumpe", "<title id=\"title\">Fun-Pumpe")
    kontur = pumpe.FARBEN[zustand][2]
    kopf, koerper = zeilen[:3], [z.replace(kontur, BRAUN) for z in zeilen[3:-1]]
    if zustand == "stoerung":
        koerper = [f"  <g>{WACKELN}"] + koerper + ["  </g>"]
    return "\n".join(kopf + koerper + EFFEKTE[zustand] + ["</svg>"]) + "\n"


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "symbole" / "fun"
    for richtung in pumpe.RICHTUNGEN:
        for zustand in pumpe.FARBEN:
            p = out / f"Fun_Pumpe_{richtung}_{zustand}.svg"
            p.write_text(svg(richtung, zustand), encoding="utf-8")
            print(p)
