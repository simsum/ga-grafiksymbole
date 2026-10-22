#!/usr/bin/env python3
"""Erzeugt die Klappensymbole unter symbole/lueftung/klappen/ in fünf Stellungen.

Stellungen: 1_zu, 2_25, 3_50, 4_75, 5_auf. Das Klappenblatt steht bei "zu" quer zur
Kanalachse (90°) und bei "auf" längs (0°); dazwischen 67,5° / 45° / 22,5°.
Die Maße sind aus den Klappen AC0531 und AC0511/AC0512/AC0521/AC0522 der SBC-Icon-
Galerie (Honeywell) abgeleitet.

Benötigt resvg-py für die PNGs (pip install resvg-py).

Aufruf: python tools/klappen.py [Zielordner]
"""
import sys
from pathlib import Path

import resvg_py

ROOT = Path(__file__).resolve().parent.parent
STELLUNGEN = [("1_zu", 90), ("2_25", 67.5), ("3_50", 45), ("4_75", 22.5), ("5_auf", 0)]

VERLAUF = ('<stop offset="0" stop-color="#B3B3B3"/><stop offset="0.3822" stop-color="#FFFFFF"/>'
           '<stop offset="0.6044" stop-color="#DEDEDE"/><stop offset="0.8588" stop-color="#BEBEBE"/>'
           '<stop offset="1" stop-color="#B3B3B3"/>')
BLATT, NABE = "#808080", "#4D4D4D"

# Familien: Name -> Breite, Höhe, Kanalachse ("y" senkrecht, "x" waagerecht), Gehäuse, Blätter
FAMILIEN = {
    "Klappe_senkrecht_klein": dict(
        b=30, h=60, achse="y", rahmen="grau",
        naben=[(15, 30)], r=4.6, laenge=(33.5, 33.5), dicke=2.3),
    "Klappe_senkrecht_gross": dict(
        b=40, h=80, achse="y", rahmen="grau",
        naben=[(20, 40)], r=6.1, laenge=(44.7, 44.7), dicke=3.1),
    "Klappe_senkrecht_3blatt_klein": dict(
        b=30, h=60, achse="y", rahmen="dunkel",
        naben=[(15, 10.8), (15, 30), (15, 49.2)], r=4.3, laenge=(22.1, 16.3), dicke=2.6),
    "Klappe_waagerecht_3blatt_klein": dict(
        b=60, h=30, achse="x", rahmen="dunkel",
        naben=[(10.8, 15), (30, 15), (49.2, 15)], r=4.3, laenge=(22.1, 16.3), dicke=2.6),
}


def svg(name: str, f: dict, winkel: float) -> str:
    b, h = f["b"], f["h"]
    # Verlauf quer zur kurzen Seite
    x2, y2 = (1, 0) if b < h else (0, 1)
    if f["rahmen"] == "grau":
        gehaeuse = (f'<rect fill="url(#gKlappe)" x="{0.4 + 0.4:g}" y="0.4" width="{b - 1.5:g}" height="{h - 0.7:g}"/>\n'
                    f'  <path d="M{b - 0.4:g},{h}H0.4V0h{b - 0.8:g}V{h}L{b - 0.4:g},{h}z M1.1,{h - 0.7:g}h{b - 2.3:g}V0.7H1.1V{h - 0.7:g}L1.1,{h - 0.7:g}z" fill="#979797"/>')
    else:
        gehaeuse = (f'<rect fill="url(#gKlappe)" x="0.4" y="0.4" width="{b - 0.7:g}" height="{h - 0.7:g}" '
                    f'stroke="#333333" stroke-width="0.3" stroke-linejoin="round"/>')
    anteil = (90 - winkel) / 90          # 0 = zu, 1 = auf
    laenge = f["laenge"][0] + (f["laenge"][1] - f["laenge"][0]) * anteil
    blaetter, naben = "", ""
    for cx, cy in f["naben"]:
        # Blatt liegt zunächst quer zur Kanalachse, Drehung gegen den Uhrzeigersinn Richtung "auf"
        if f["achse"] == "y":
            rect = (cx - laenge / 2, cy - f["dicke"] / 2, laenge, f["dicke"])
            dreh = -(90 - winkel)
        else:
            rect = (cx - f["dicke"] / 2, cy - laenge / 2, f["dicke"], laenge)
            dreh = 90 - winkel
        blaetter += (f'<rect x="{rect[0]:.2f}" y="{rect[1]:.2f}" width="{rect[2]:.2f}" height="{rect[3]:.2f}" '
                     f'fill="{BLATT}" transform="rotate({dreh:g} {cx:g} {cy:g})"/>')
        naben += f'<circle cx="{cx:g}" cy="{cy:g}" r="{f["r"]:g}" fill="{NABE}"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{b}" height="{h}" viewBox="0 0 {b} {h}">
  <!-- {name}: Klappenblatt {winkel:g} Grad zur Kanalachse (zu = quer, auf = laengs) -->
  <defs>
    <linearGradient id="gKlappe" gradientUnits="objectBoundingBox" x1="0" y1="0" x2="{x2}" y2="{y2}">{VERLAUF}</linearGradient>
    <clipPath id="cKanal"><rect x="1.1" y="0.7" width="{b - 2.2:g}" height="{h - 1.4:g}"/></clipPath>
  </defs>
  {gehaeuse}
  <g clip-path="url(#cKanal)">{blaetter}</g>
  {naben}
</svg>
'''


def main() -> int:
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "symbole" / "lueftung" / "klappen"
    ziel.mkdir(parents=True, exist_ok=True)
    for fam, f in FAMILIEN.items():
        for suffix, winkel in STELLUNGEN:
            name = f"{fam}_{suffix}"
            s = svg(name, f, winkel)
            (ziel / f"{name}.svg").write_text(s, encoding="utf-8")
            (ziel / f"{name}.png").write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=s, width=f["b"], height=f["h"])))
            print(ziel / f"{name}.svg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
