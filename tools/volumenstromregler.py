#!/usr/bin/env python3
"""Erzeugt symbole/lueftung/volumenstromregler/Volumenstromregler_{bauart}_{richtung}_{zustand}.svg.

Volumenstromregler im Gerätestil (wie Klimakonvektor, Wärmepumpe, WRG), 140 × 80 (rechts/links)
bzw. 80 × 140 (oben/unten). Aufruf: python tools/volumenstromregler.py [zielordner]

Bauarten (Luftrichtung rechts, für die anderen Richtungen gespiegelt/gedreht wie bisher,
damit der Regler oben bzw. rechts sitzt):
  rund   Rohr (34 px) mit Rundungsverlauf, graue Flanschplatten, eine Regelklappe
  eckig  Rechteckkanal (46 px), graue Flanschplatten, drei gegenläufige Lamellen
Darüber der Kompaktregler: graues Gehäuse, dunkles Display, Status-LED in Zustandsfarbe.
Klappenblätter und Naben wie bei den Klappen (#808080 / #4D4D4D).

Zustände (gleiche Abmessungen, feste Teile an derselben Stelle):
  _aus        Klappe steht, LED grau
  _an         Klappe regelt (pendelt leicht), Luftpfeile laufen in Luftrichtung, LED grün
  _stoerung   Klappe steht, rotes Warndreieck und LED blinken (1 Hz)
Die bisherigen Dateien ohne Zustand (Volumenstromregler_{bauart}_{richtung}.svg) bleiben erhalten,
weil sie in Px-Seiten referenziert sind; sie zeigen das neue Design im Zustand „aus“.
"""
import sys
from pathlib import Path

from zustandsfarben import ZUSTAENDE, STOERUNG

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "lueftung" / "volumenstromregler"

# Richtung: (Breite, Höhe, Transformation lokal → Bild, Abbildung eines lokalen Punkts)
RICHTUNGEN = {
    "rechts": (140, 80, "", lambda x, y: (x, y)),
    "links": (140, 80, "translate(140,0) scale(-1,1)", lambda x, y: (140 - x, y)),
    "oben": (80, 140, "translate(0,140) scale(1,-1) translate(80,0) rotate(90)", lambda x, y: (80 - y, 140 - x)),
    "unten": (80, 140, "translate(80,0) rotate(90)", lambda x, y: (80 - y, x)),
}
TITEL = {"aus": "aus", "an": "Betrieb", "stoerung": "Störung"}

# Bauart: Kanal oben/unten, Reglermitte x, Klappennaben, Blattlänge, Startwinkel je Blatt
BAUARTEN = {
    "rund": dict(y0=32, y1=66, rx=68, naben=[(68, 49)], laenge=32, winkel=[38]),
    "eckig": dict(y0=27, y1=73, rx=66, naben=[(66, 36), (66, 50), (66, 64)], laenge=17, winkel=[66, -66, 66]),
}

DEFS = """<defs>
    <linearGradient id="gG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F0F1F2"/><stop offset="1" stop-color="#D2D5D8"/></linearGradient>
    <linearGradient id="gR" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B3B3B3"/><stop offset="0.38" stop-color="#FFFFFF"/><stop offset="0.6" stop-color="#DEDEDE"/><stop offset="0.86" stop-color="#BEBEBE"/><stop offset="1" stop-color="#B3B3B3"/></linearGradient>
    <radialGradient id="gL" cx="0.4" cy="0.35" r="0.65"><stop offset="0" stop-color="{o}"/><stop offset="1" stop-color="{u}"/></radialGradient>
  </defs>"""


def kanal(b: dict) -> str:
    y0, y1 = b["y0"], b["y1"]
    fuell = "url(#gR)" if b is BAUARTEN["rund"] else "url(#gG)"
    s = [f'<rect x="10" y="{y0}" width="120" height="{y1 - y0}" fill="{fuell}" stroke="#999999" stroke-width="2"/>']
    if b is BAUARTEN["eckig"]:   # Kanalkanten innen angedeutet
        s.append(f'<path d="M12,{y0 + 4} H128 M12,{y1 - 4} H128" stroke="#B5BCC4" stroke-width="1"/>')
    # graue Flanschplatten an beiden Enden
    for x in (6, 129):
        s.append(f'<rect x="{x}" y="{y0 - 5}" width="5" height="{y1 - y0 + 10}" rx="1" fill="#B5B5B5" stroke="#6B6B6B" stroke-width="1"/>')
    return "".join(s)


def klappen(b: dict, an: bool) -> str:
    s = []
    for i, ((cx, cy), w) in enumerate(zip(b["naben"], b["winkel"])):
        h = b["laenge"] / 2
        anim = ""
        if an:   # Klappe regelt: pendelt leicht um die Stellung, Nachbarblätter gegenläufig
            d = 8 if w < 0 else -8
            anim = (f'<animateTransform attributeName="transform" type="rotate" values="{w} {cx} {cy};{w + d} {cx} {cy};{w} {cx} {cy}" '
                    'keyTimes="0;0.5;1" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="4s" repeatCount="indefinite"/>')
        s.append(f'<g transform="rotate({w} {cx} {cy})">{anim}'
                 f'<rect x="{cx - 1.6}" y="{cy - h}" width="3.2" height="{2 * h}" rx="1" fill="#808080"/></g>'
                 f'<circle cx="{cx}" cy="{cy}" r="{3.6 if len(b["naben"]) == 1 else 2.6}" fill="#4D4D4D"/>')
    return "".join(s)


def regler(b: dict, zustand: str) -> str:
    rx, y0 = b["rx"], b["y0"]
    x0, oben = rx - 18, y0 - 26
    kontur = ZUSTAENDE[zustand][2]
    led = f'<circle cx="{rx + 9}" cy="{oben + 10.5}" r="3.6" fill="url(#gL)" stroke="{kontur}" stroke-width="1"/>'
    if zustand == "stoerung":
        led = f'<g><animate attributeName="opacity" values="1;0.15" dur="1s" calcMode="discrete" repeatCount="indefinite"/>{led}</g>'
    return (f'<rect x="{rx - 3}" y="{y0 - 6}" width="6" height="6" fill="#8C8C8C" stroke="#6B6B6B" stroke-width="1"/>'
            f'<rect x="{x0}" y="{oben}" width="36" height="21" rx="3" fill="url(#gG)" stroke="#999999" stroke-width="1.6"/>'
            f'<rect x="{x0 + 5}" y="{oben + 6}" width="14" height="9" rx="1.2" fill="#2B3440" stroke="#6B7480" stroke-width="0.8"/>'
            f'{led}')


def luftpfeil(b: dict, an: bool) -> str:
    y = (b["y0"] + b["y1"]) / 2
    pfeil = (f'<path d="M92,{y} H116 M109,{y - 7} L116,{y} L109,{y + 7}" fill="none" stroke="#4D4D4D" stroke-width="2.6" '
             'stroke-linecap="round" stroke-linejoin="round"/>')
    if not an:
        return pfeil
    s = [pfeil.replace('stroke="#4D4D4D"', 'stroke="#4D4D4D" stroke-opacity="0.25"')]
    for beginn in ("0s", "0.4s", "0.8s"):
        s.append('<path d="M-4,-6 L2,0 L-4,6" fill="none" stroke="#4D4D4D" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" opacity="0">'
                 f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.2;0.75;1" dur="1.2s" begin="{beginn}" repeatCount="indefinite"/>'
                 f'<animateTransform attributeName="transform" type="translate" values="92 {y};118 {y}" dur="1.2s" begin="{beginn}" repeatCount="indefinite"/></path>')
    return "".join(s)


def warnung(cx: float, cy: float) -> str:
    return ('<g><animate attributeName="opacity" values="1;0.15" dur="1s" calcMode="discrete" repeatCount="indefinite"/>'
            f'<g transform="translate({cx} {cy})">'
            f'<path d="M0,-17 L19,15 L-19,15 Z" fill="{STOERUNG[1]}" stroke="#FFFFFF" stroke-width="2.6" stroke-linejoin="round"/>'
            '<rect x="-2.5" y="-8" width="5" height="15" rx="2.5" fill="#FFFFFF"/><circle cx="0" cy="10.5" r="2.7" fill="#FFFFFF"/></g></g>')


def svg(bauart: str, richtung: str, zustand: str) -> str:
    b = BAUARTEN[bauart]
    W, H, trafo, abb = RICHTUNGEN[richtung]
    oben, unten, _ = ZUSTAENDE[zustand]
    an = zustand == "an"
    innen = [kanal(b), klappen(b, an), regler(b, zustand), luftpfeil(b, an)]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title">',
         f'  <title id="title">Volumenstromregler {bauart}, Luftrichtung {richtung}, {TITEL[zustand]}</title>',
         '  ' + DEFS.format(o=oben, u=unten),
         f'  <g{f" transform={chr(34)}{trafo}{chr(34)}" if trafo else ""}>',
         *(f'    {t}' for t in innen),
         '  </g>']
    if zustand == "stoerung":
        cx, cy = abb(b["rx"], (b["y0"] + b["y1"]) / 2)
        s.append(f'  {warnung(cx, cy)}')
    s.append('</svg>')
    return "\n".join(s) + "\n"


def schreib(p: Path, inhalt: str) -> None:
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(inhalt)
    print(p.name)


def main() -> None:
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ZIEL
    ziel.mkdir(parents=True, exist_ok=True)
    for bauart in BAUARTEN:
        for richtung in RICHTUNGEN:
            for zustand in ("aus", "an", "stoerung"):
                schreib(ziel / f"Volumenstromregler_{bauart}_{richtung}_{zustand}.svg", svg(bauart, richtung, zustand))
            # bisheriger Name ohne Zustand = Zustand „aus“ (Kompatibilität)
            schreib(ziel / f"Volumenstromregler_{bauart}_{richtung}.svg", svg(bauart, richtung, "aus"))


if __name__ == "__main__":
    main()
