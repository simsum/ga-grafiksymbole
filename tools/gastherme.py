#!/usr/bin/env python3
"""Erzeugt symbole/hydraulik/erzeuger/Gastherme_*.svg.

Wandhängende Gastherme (Brennwertgerät), neutral gezeichnet, ohne Logos. Aufruf: python tools/gastherme.py

Varianten (alle 120 × 166, gleiche Anschlusspunkte VL x = 30, Gas x = 60, RL x = 90, y = 166):
  Gastherme_vorne_*          geschlossenes Gehäuse mit Schauglas (Brenner) und Bedienfeld
  Gastherme_Schnitt_vorne_*  offenes Gehäuse: Ausdehnungsgefäß, Wärmetauscher mit Rohrwendel und
                             Brennkammer, Gebläse, Gasventil, Leitungen innen
Anschlüsse als Flansche an der Unterkante, von links: Vorlauf (rot), Gas (gelb), Rücklauf (blau).
Abgasstutzen oben mittig.

Zustände:
  _aus        Brenner aus, Status-LED grau
  _an         Betrieb: Flammen flackern, Brennkammer glüht, Gebläse dreht (Schnitt), LED grün (SMIL)
  _stoerung   Störung: rotes Warndreieck und rote Status-LED blinken (1 Hz)
"""
from pathlib import Path

from zustandsfarben import AUS, BETRIEB, STOERUNG

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "hydraulik" / "erzeuger"

W, H = 120, 166
FL = {"rot": "#D7302B", "orange": "#F29A38", "gelb": "#F2C230", "blau": "#2E6BC2"}
LED = {"aus": AUS[2], "an": BETRIEB[1], "stoerung": STOERUNG[1]}

DEFS = """<defs>
<linearGradient id="gB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E6E6E6"/><stop offset="0.07" stop-color="#E0E0E0"/><stop offset="1" stop-color="#999999"/></linearGradient>
<linearGradient id="gG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F0F1F2"/><stop offset="1" stop-color="#D2D5D8"/></linearGradient>
<linearGradient id="gN" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8C8C8C"/><stop offset="0.5" stop-color="#D9D9D9"/><stop offset="1" stop-color="#8C8C8C"/></linearGradient>
<linearGradient id="gF" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#E0302A"/><stop offset="0.45" stop-color="#F29A38"/><stop offset="1" stop-color="#FFD34D"/></linearGradient>
<linearGradient id="gV" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E07B22"/><stop offset="0.45" stop-color="#F7B26A"/><stop offset="1" stop-color="#D96F1A"/></linearGradient>
<linearGradient id="gC" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#A3ABB4"/><stop offset="0.45" stop-color="#E3E6E9"/><stop offset="1" stop-color="#9AA2AB"/></linearGradient>
<radialGradient id="gGl" cx="0.5" cy="0.55" r="0.6"><stop offset="0" stop-color="#FFD34D"/><stop offset="0.6" stop-color="#F29A38"/><stop offset="1" stop-color="#B8231A"/></radialGradient>
</defs>"""


def flansch(x, farbe, y=150):
    return (f'<rect x="{x-3}" y="{y}" width="6" height="5" fill="#8C8C8C" stroke="#6B6B6B" stroke-width="1"/>'
            f'<rect x="{x-8}" y="{y+5}" width="16" height="5" rx="1" fill="{farbe}" stroke="#6B6B6B" stroke-width="1"/>')


def abgas():
    return ('<rect x="51" y="1" width="18" height="17" fill="url(#gN)" stroke="#808080" stroke-width="1"/>'
            '<rect x="47" y="12" width="26" height="6" rx="1" fill="#B5B5B5" stroke="#999999" stroke-width="1"/>')


def flamme(x, y, s=1.0, delay=0.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><g>'
            f'<animateTransform attributeName="transform" type="scale" values="1 1;0.92 1.15;1.05 0.9;1 1" '
            f'dur="0.7s" begin="{delay}s" repeatCount="indefinite"/>'
            '<path d="M0,0 C-6,-1 -6,-8 0,-17 C6,-8 6,-1 0,0 Z" fill="url(#gF)"/>'
            '<path d="M0,0 C-2.6,-0.6 -2.4,-4 0,-7.5 C2.4,-4 2.6,-0.6 0,0 Z" fill="#5DB8F0"/></g></g>')


def bedienfeld(y, h, zustand):
    cy = y + h / 2
    blink = ('<animate attributeName="opacity" values="1;0.15" dur="1s" calcMode="discrete" repeatCount="indefinite"/>'
             if zustand == "stoerung" else "")
    s = (f'<rect x="13" y="{y}" width="94" height="{h}" rx="2" fill="#D9DCDF" stroke="#999999" stroke-width="1.6"/>'
         f'<rect x="19" y="{cy-7}" width="30" height="14" rx="1.5" fill="#2B3440" stroke="#6B7480" stroke-width="1"/>'
         f'<g fill="#55606D"><rect x="23" y="{cy-2}" width="6" height="4" rx="1"/><rect x="31" y="{cy-2}" width="6" height="4" rx="1"/>'
         f'<rect x="39" y="{cy-2}" width="6" height="4" rx="1"/></g>'
         f'<circle cx="57" cy="{cy}" r="3.2" fill="{LED[zustand]}" stroke="#4D4D4D" stroke-width="1">{blink}</circle>')
    for kx in (74, 94):
        s += (f'<circle cx="{kx}" cy="{cy}" r="7" fill="#F2F2F2" stroke="#808080" stroke-width="1.6"/>'
              f'<line x1="{kx}" y1="{cy}" x2="{kx}" y2="{cy-5}" stroke="#666666" stroke-width="1.6" stroke-linecap="round"/>')
    return s


def warnung(cx, cy):
    return ('<g><animate attributeName="opacity" values="1;0.15" dur="1s" calcMode="discrete" repeatCount="indefinite"/>'
            f'<path d="M{cx},{cy-24} L{cx+26},{cy+20} L{cx-26},{cy+20} Z" fill="#D7302B" stroke="#FFFFFF" stroke-width="3" stroke-linejoin="round"/>'
            f'<rect x="{cx-3}" y="{cy-12}" width="6" height="20" rx="3" fill="#FFFFFF"/>'
            f'<circle cx="{cx}" cy="{cy+14}" r="3.5" fill="#FFFFFF"/></g>')


def gehaeuse():
    return ('<rect x="6" y="18" width="108" height="132" rx="4" fill="url(#gG)" stroke="#999999" stroke-width="2"/>'
            '<rect x="7" y="19" width="106" height="6" fill="url(#gB)"/>'
            '<line x1="7" y1="25" x2="113" y2="25" stroke="#B5B5B5" stroke-width="1.2"/>')


def geschlossen(z):
    s = abgas() + flansch(30, FL["rot"]) + flansch(60, FL["gelb"]) + flansch(90, FL["blau"]) + gehaeuse()
    s += '<rect x="13" y="31" width="94" height="80" rx="3" fill="#E9EBED" stroke="#B5B5B5" stroke-width="1.2"/>'
    # Schauglas
    s += '<circle cx="60" cy="70" r="22" fill="#2B3440" stroke="#6B7480" stroke-width="2"/>'
    if z == "an":
        s += '<circle cx="60" cy="70" r="19" fill="url(#gGl)" opacity="0.35"><animate attributeName="opacity" values="0.3;0.45;0.3" dur="1.4s" repeatCount="indefinite"/></circle>'
        s += flamme(50, 80, 0.75, 0) + flamme(60, 80, 0.95, 0.2) + flamme(70, 80, 0.75, 0.4)
    s += '<rect x="44" y="80" width="32" height="5" rx="1.5" fill="#8A94A0" stroke="#55606D" stroke-width="1"/>'
    s += bedienfeld(116, 28, z)
    if z == "stoerung":
        s += warnung(60, 68)
    return s


def schnitt(z):
    s = abgas() + flansch(30, FL["rot"]) + flansch(60, FL["gelb"]) + flansch(90, FL["blau"]) + gehaeuse()
    s += '<rect x="11" y="28" width="98" height="90" rx="2" fill="#F7F8F9" stroke="#B5B5B5" stroke-width="1.2"/>'
    # Rohre innen (laufen hinter dem Bedienfeld weiter)
    s += ('<g fill="none" stroke-width="4" stroke-linejoin="round">'
          '<path d="M46,50 H33 V122" stroke="#D7302B"/>'
          '<path d="M61,110 V122" stroke="#C9A21E"/>'
          '<path d="M76,90 H90 V122" stroke="#2E6BC2"/></g>')
    # Ausdehnungsgefäß
    s += '<rect x="14" y="33" width="14" height="66" rx="7" fill="url(#gV)" stroke="#B5651D" stroke-width="1.2"/>'
    # Abgasweg vom Wärmetauscher zum Abgasstutzen
    s += '<rect x="53" y="25" width="14" height="10" fill="url(#gN)" stroke="#808080" stroke-width="1"/>'
    # Wärmetauscher (Zylinder mit Rohrwendel)
    s += '<rect x="44" y="34" width="34" height="62" rx="5" fill="url(#gC)" stroke="#6B7480" stroke-width="1.4"/>'
    s += '<rect x="52" y="44" width="18" height="44" rx="3" fill="#2B3440" stroke="#55606D" stroke-width="1"/>'
    if z == "an":
        s += '<rect x="53" y="45" width="16" height="42" rx="2.5" fill="url(#gGl)" opacity="0.8"><animate attributeName="opacity" values="0.65;0.95;0.65" dur="1.2s" repeatCount="indefinite"/></rect>'
    s += '<rect x="58" y="46" width="6" height="40" rx="2" fill="#8A94A0" stroke="#55606D" stroke-width="0.8"/>'
    if z == "an":
        for i, yy in enumerate((56, 68, 80)):
            s += f'<g transform="rotate(-90 58 {yy})">{flamme(58, yy, 0.45, i*0.15)}</g>'
            s += f'<g transform="rotate(90 64 {yy})">{flamme(64, yy, 0.45, i*0.15+0.1)}</g>'
    for i in range(7):
        y = 38 + i * 8.2
        s += f'<rect x="41" y="{y}" width="9" height="5" rx="2.5" fill="#C9CDD2" stroke="#6B7480" stroke-width="0.9"/>'
        s += f'<rect x="72" y="{y}" width="9" height="5" rx="2.5" fill="#C9CDD2" stroke="#6B7480" stroke-width="0.9"/>'
    # Gebläse
    s += '<rect x="78" y="40" width="8" height="8" fill="#8A94A0" stroke="#55606D" stroke-width="1"/>'
    s += '<circle cx="95" cy="44" r="11" fill="#55606D" stroke="#2B3440" stroke-width="1.4"/>'
    if z == "an":
        s += '<g><animateTransform attributeName="transform" type="rotate" from="0 95 44" to="360 95 44" dur="1.2s" repeatCount="indefinite"/>'
    else:
        s += '<g>'
    for a in (0, 90, 180, 270):
        s += f'<ellipse cx="95" cy="38" rx="2.6" ry="5" fill="#8A94A0" transform="rotate({a} 95 44)"/>'
    s += '</g><circle cx="95" cy="44" r="3" fill="#2B3440"/>'
    # Gasventil
    s += '<rect x="53" y="100" width="16" height="12" rx="2" fill="#F2C230" stroke="#8C6D00" stroke-width="1.2"/>'
    s += '<rect x="57" y="96" width="8" height="4" fill="#4D4D4D"/>'
    s += bedienfeld(118, 28, z)
    if z == "stoerung":
        s += warnung(61, 66)
    return s


def svg(inhalt, titel):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">'
            f'<title>{titel}</title>{DEFS}{inhalt}</svg>')


TITEL = {"aus": "aus", "an": "Betrieb", "stoerung": "Störung"}

if __name__ == "__main__":
    for name, fn, titel in (("Gastherme_vorne", geschlossen, "Gastherme (Wandgerät), Vorderansicht"),
                            ("Gastherme_Schnitt_vorne", schnitt, "Gastherme (Wandgerät), Schnitt")):
        for z in ("aus", "an", "stoerung"):
            datei = ZIEL / f"{name}_{z}.svg"
            with open(datei, "w", encoding="utf-8", newline="\n") as f:
                f.write(svg(fn(z), f"{titel}, {TITEL[z]}") + "\n")
            print(datei.relative_to(ZIEL.parent.parent.parent))
