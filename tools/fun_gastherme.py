#!/usr/bin/env python3
"""Erzeugt symbole/fun/hydraulik/erzeuger/Fun_Gastherme_vorne_<zustand>_animiert.svg.

Fun-Variante der Gastherme (tools/gastherme.py, Vorderansicht): gleiche Größe (120 × 166) und Anschlusspunkte
(VL x = 30, Gas x = 60, RL x = 90), Gehäuse, Abgasstutzen, Bedienfeld und Flansche wie die normale Gastherme.
Die Frontplatte bekommt ein Gesicht, das Schauglas mit dem Brenner sitzt als „Bauch“ darunter.
Gesichtszüge und Effekte wie bei der Fun-Wärmepumpe (tools/fun_waermepumpe.py). Animation per SMIL.

  _aus       Augen zu, schläft; „Zzz“ steigt auf; Schauglas dunkel
  _an        große Augen (blinzeln), Lächeln, Bäckchen; Flammen im Schauglas flackern, LED grün
  _stoerung  X-Augen, Zickzack-Mund; Therme wackelt, Rauch steigt aus dem Abgasstutzen,
             Warndreieck im Schauglas, rote Status-LED blinkt

Ohne Animation bleiben Gesicht, Zustandsanzeigen und Effekte (in Ausgangslage) sichtbar.
Aufruf: python tools/fun_gastherme.py
"""
from pathlib import Path

import gastherme as gt
from fun_waermepumpe import augen, mund, rauch, zzz

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "fun" / "hydraulik" / "erzeuger"
GX, GY, GR = 60, 84, 17          # Schauglas
WACKELN = ('<animateTransform attributeName="transform" type="rotate" '
           'values="0 60 160;-2 60 160;2 60 160;-1.2 60 160;0 60 160" dur="0.6s" repeatCount="indefinite"/>')
TITEL = {"aus": "aus", "an": "Betrieb", "stoerung": "Störung"}


def schauglas(z: str) -> str:
    s = f'<circle cx="{GX}" cy="{GY}" r="{GR}" fill="#2B3440" stroke="#6B7480" stroke-width="2"/>'
    if z == "an":
        s += (f'<circle cx="{GX}" cy="{GY}" r="{GR - 2}" fill="url(#gGl)" opacity="0.35">'
              '<animate attributeName="opacity" values="0.3;0.5;0.3" dur="1.4s" repeatCount="indefinite"/></circle>')
        s += gt.flamme(GX - 8, GY + 8, 0.55, 0) + gt.flamme(GX, GY + 8, 0.72, 0.2) + gt.flamme(GX + 8, GY + 8, 0.55, 0.4)
    s += f'<rect x="{GX - 13}" y="{GY + 8}" width="26" height="4" rx="1.5" fill="#8A94A0" stroke="#55606D" stroke-width="1"/>'
    if z == "stoerung":
        s += ('<g><animate attributeName="opacity" values="1;0.15" dur="1s" calcMode="discrete" repeatCount="indefinite"/>'
              f'<path d="M{GX},{GY - 13} L{GX + 13},{GY + 9} L{GX - 13},{GY + 9} Z" fill="#D7302B" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>'
              f'<rect x="{GX - 1.6}" y="{GY - 6}" width="3.2" height="9" rx="1.6" fill="#FFFFFF"/>'
              f'<circle cx="{GX}" cy="{GY + 5.5}" r="1.8" fill="#FFFFFF"/></g>')
    return s


def svg(z: str) -> str:
    gesicht = {"aus": augen(60, 47, 34, "zu", 7) + mund(60, 60, "schlaf"),
               "an": augen(60, 46, 34, "auf", 7) + mund(60, 58, "laecheln", 18),
               "stoerung": augen(60, 47, 34, "x", 7) + mund(60, 61, "zickzack", 18)}[z]
    effekt = {"aus": zzz(84, 44), "an": "", "stoerung": rauch(80, 28)}[z]
    s = (gt.abgas() + gt.flansch(30, gt.FL["rot"]) + gt.flansch(60, gt.FL["gelb"]) + gt.flansch(90, gt.FL["blau"])
         + gt.gehaeuse()
         + '<rect x="13" y="31" width="94" height="80" rx="3" fill="#E9EBED" stroke="#B5B5B5" stroke-width="1.2"/>'
         + gesicht + schauglas(z) + gt.bedienfeld(116, 28, z) + effekt)
    if z == "stoerung":
        s = f"<g>{WACKELN}{s}</g>"
    return gt.svg(s, f"Fun: Gastherme (Wandgerät), Vorderansicht, {TITEL[z]}") + "\n"


def main() -> None:
    ZIEL.mkdir(parents=True, exist_ok=True)
    for z in ("aus", "an", "stoerung"):
        p = ZIEL / f"Fun_Gastherme_vorne_{z}_animiert.svg"
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg(z))
        print(p)


if __name__ == "__main__":
    main()
