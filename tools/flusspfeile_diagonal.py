#!/usr/bin/env python3
"""Erzeugt symbole/allgemein/flusspfeile/Flusspfeil_diagonal_{richtung}[_an].svg.

Gerade Flusspfeile für diagonale (45°) Leitungen: derselbe Pfeil wie Flusspfeil_rechts (24 × 14), um 45° gedreht.
24 × 24, Pfeilmitte im Bildmittelpunkt (12, 12) – mit der Mitte auf die Rohrachse setzen.
Richtung = Flussrichtung: rechts_oben, rechts_unten, links_unten, links_oben.
Variante _an: drei helle Punkte laufen in Flussrichtung durch den Pfeil (SMIL, 1,2 s), wie bei den geraden Pfeilen.
Aufruf: python tools/flusspfeile_diagonal.py
"""
from pathlib import Path

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "allgemein" / "flusspfeile"
PFEIL = ('<path d="M2,5 L12,5 L12,1 L22,7 L12,13 L12,9 L2,9 Z" fill="#2A2A2A" stroke="#FFFFFF" stroke-opacity="0.7" '
         'stroke-width="1" stroke-linejoin="round"/>')
WINKEL = {"rechts_oben": -45, "rechts_unten": 45, "links_unten": 135, "links_oben": -135}


def punkte() -> str:
    return "".join(
        f'\n    <circle cx="3.5" cy="7" r="1.1" fill="#F2F2F2" opacity="0"><animate attributeName="opacity" values="0;1;1;0" '
        f'keyTimes="0;0.15;0.75;1" dur="1.2s" begin="{b}" repeatCount="indefinite"/><animate attributeName="cx" '
        f'values="3.5;19" dur="1.2s" begin="{b}" repeatCount="indefinite"/></circle>' for b in ("0s", "0.4s", "0.8s"))


def svg(richtung: str, an: bool) -> str:
    kommentar = "Flussrichtungspfeil diagonal (45°) fuer Rohrleitungen" + (
        ", animiert: helle Punkte laufen in Flussrichtung (SMIL); ohne Animation normaler Pfeil" if an else "")
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">\n'
            f'  <!-- {kommentar} -->\n'
            f'  <g transform="translate(12 12) rotate({WINKEL[richtung]}) translate(-12 -7)">\n'
            f'    {PFEIL}{punkte() if an else ""}\n  </g>\n</svg>\n')


def main() -> None:
    for richtung in WINKEL:
        for an in (False, True):
            p = ZIEL / f"Flusspfeil_diagonal_{richtung}{'_an' if an else ''}.svg"
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(svg(richtung, an))
            print(p.name)


if __name__ == "__main__":
    main()
