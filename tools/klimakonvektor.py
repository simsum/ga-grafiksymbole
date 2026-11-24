#!/usr/bin/env python3
"""Erzeugt symbole/lueftung/klimageraete/Klimakonvektor_{richtung}_{zustand}.svg.

Klimakonvektor (Kanalgerät), Draufsicht, 160 × 90 (rechts/links) bzw. 90 × 160 (oben/unten).
Gestaltet wie die übrigen Geräte (Wärmepumpe, WRG): graues Gehäuse mit dezentem Verlauf, Kontur #999999,
dunkle Lüfterräder, ohne Anschlüsse.
Aufruf: python tools/klimakonvektor.py [zielordner]

Aufbau (Ausblas rechts, gedreht für die anderen Richtungen):
  links      Wärmetauscher mit Lamellen
  Mitte      zwei Radialventilatoren (Spiralgehäuse, dunkles Laufrad)
  rechts     Ausblasgitter, Luftrichtungspfeil, Status-LED oben rechts

Zustände (gleiche Abmessungen, feste Teile an derselben Stelle):
  _aus        Laufräder stehen, LED grau
  _an         Laufräder drehen, Luftpfeile laufen zum Ausblas, LED grün
  _stoerung   Laufräder stehen, rotes Warndreieck und LED blinken (1 Hz)
Ohne SMIL bleibt der Zustand an der LED (und am Warndreieck) erkennbar.

Die bisherigen Dateien Klimakonvektor_{richtung}.svg (ohne Zustand) bleiben erhalten, weil sie in Px-Seiten
referenziert sind; sie zeigen das neue Design im Zustand „aus“.
"""
import math
import sys
from pathlib import Path

from zustandsfarben import ZUSTAENDE, STOERUNG

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "lueftung" / "klimageraete"

DREHDAUER = "1.2s"

# Richtung: (Breite, Höhe, Transformation lokal → Bild, Abbildung eines lokalen Punkts)
RICHTUNGEN = {
    "rechts": (160, 90, "", lambda x, y: (x, y)),
    "links": (160, 90, "translate(160,90) rotate(180)", lambda x, y: (160 - x, 90 - y)),
    "oben": (90, 160, "translate(0,160) rotate(-90)", lambda x, y: (y, 160 - x)),
    "unten": (90, 160, "translate(90,0) rotate(90)", lambda x, y: (90 - y, x)),
}
TITEL = {"aus": "aus", "an": "Betrieb", "stoerung": "Störung"}

DEFS = """<defs>
    <linearGradient id="gG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F0F1F2"/><stop offset="1" stop-color="#D2D5D8"/></linearGradient>
    <radialGradient id="gL" cx="0.4" cy="0.35" r="0.65"><stop offset="0" stop-color="{o}"/><stop offset="1" stop-color="{u}"/></radialGradient>
  </defs>"""


def rechteck(abb, x, y, w, h):
    """Lokales Rechteck in Bildkoordinaten (für Teile, deren Verlauf senkrecht bleiben soll)."""
    (x1, y1), (x2, y2) = abb(x, y), abb(x + w, y + h)
    return min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)


def waermetauscher() -> str:
    s = ['<rect x="17" y="13" width="28" height="64" rx="2" fill="#F7F8F9" stroke="#808080" stroke-width="1.4"/>']
    # Lamellen
    s.append('<g stroke="#B5BCC4" stroke-width="0.8">'
             + "".join(f'<line x1="{x}" y1="15" x2="{x}" y2="75"/>' for x in range(20, 44, 3)) + '</g>')
    return "".join(s)


def ventilator(cx: float, cy: float, drehen: bool) -> str:
    """Radialventilator: Spiralgehäuse (Ausblas nach rechts), dunkles Laufrad mit gebogenen Schaufeln."""
    r, rg = 13, 16
    # Gehäuse: Kreis mit tangentialem Ausblasstutzen oben nach rechts (Laufrad dreht im Uhrzeigersinn)
    xs = math.sqrt(rg * rg - 16)
    gehaeuse = (f'<path d="M{cx},{cy - rg} A{rg},{rg} 0 1 0 {cx + xs:.2f},{cy - 4} H{cx + 21} V{cy - rg} Z" '
                'fill="#D9DCDF" stroke="#999999" stroke-width="1.4" stroke-linejoin="round"/>')
    schaufeln = "".join(f'<path d="M0,-5 Q5,-8 4,-12" transform="rotate({a})"/>' for a in range(0, 360, 45))
    anim = (f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="{DREHDAUER}" repeatCount="indefinite"/>'
            if drehen else "")
    return (gehaeuse
            + f'<g transform="translate({cx},{cy})"><circle r="{r}" fill="#2B3440" stroke="#6B7480" stroke-width="1.4"/>'
            f'<g>{anim}<g fill="none" stroke="#8A94A0" stroke-width="1.8" stroke-linecap="round">{schaufeln}</g></g>'
            '<circle r="4" fill="#8A94A0"/><circle r="1.6" fill="#55606D"/></g>')


def ausblas() -> str:
    """Ausblasgitter an der rechten Gehäusekante."""
    s = ['<rect x="144" y="11" width="10" height="68" rx="1.5" fill="#E6E6E6" stroke="#999999" stroke-width="1.2"/>']
    s.append('<g fill="#4D4D4D">' + "".join(f'<rect x="146.5" y="{y}" width="5" height="2.4" rx="1"/>' for y in range(15, 76, 6)) + '</g>')
    return "".join(s)


def luftpfeil(an: bool) -> str:
    pfeil = '<path d="M112,45 H136 M129,38 L136,45 L129,52" fill="none" stroke="#4D4D4D" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
    if not an:
        return pfeil
    s = [pfeil.replace('stroke="#4D4D4D"', 'stroke="#4D4D4D" stroke-opacity="0.25"')]
    for beginn in ("0s", "0.4s", "0.8s"):
        s.append('<path d="M-4,-6 L2,0 L-4,6" fill="none" stroke="#4D4D4D" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" opacity="0">'
                 f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.2;0.75;1" dur="1.2s" begin="{beginn}" repeatCount="indefinite"/>'
                 f'<animateTransform attributeName="transform" type="translate" values="112 45;138 45" dur="1.2s" begin="{beginn}" repeatCount="indefinite"/></path>')
    return "".join(s)


def led(zustand: str) -> str:
    kontur = ZUSTAENDE[zustand][2]
    kreis = f'<circle cx="128" cy="14" r="3.6" fill="url(#gL)" stroke="{kontur}" stroke-width="1"/>'
    if zustand == "stoerung":
        return ('<g><animate attributeName="opacity" values="1;0.15" dur="1s" calcMode="discrete" repeatCount="indefinite"/>'
                f'{kreis}</g>')
    return kreis


def warnung(cx: float, cy: float) -> str:
    return ('<g><animate attributeName="opacity" values="1;0.15" dur="1s" calcMode="discrete" repeatCount="indefinite"/>'
            f'<g transform="translate({cx} {cy})">'
            f'<path d="M0,-21 L23,18 L-23,18 Z" fill="{STOERUNG[1]}" stroke="#FFFFFF" stroke-width="3" stroke-linejoin="round"/>'
            '<rect x="-3" y="-10" width="6" height="18" rx="3" fill="#FFFFFF"/><circle cx="0" cy="13" r="3.2" fill="#FFFFFF"/></g></g>')


def svg(richtung: str, zustand: str) -> str:
    W, H, trafo, abb = RICHTUNGEN[richtung]
    oben, unten, _ = ZUSTAENDE[zustand]
    gx, gy, gw, gh = rechteck(abb, 10, 5, 146, 80)
    innen = [waermetauscher(),
             ventilator(84, 26, zustand == "an"), ventilator(84, 64, zustand == "an"),
             ausblas(), luftpfeil(zustand == "an"), led(zustand)]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title">',
         f'  <title id="title">Klimakonvektor (Kanalgerät), Draufsicht, Ausblas {richtung}, {TITEL[zustand]}</title>',
         '  ' + DEFS.format(o=oben, u=unten),
         # Gehäuse in Bildkoordinaten, damit der Verlauf in jeder Richtung von oben nach unten läuft
         f'  <rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="3" fill="url(#gG)" stroke="#999999" stroke-width="2"/>',
         f'  <g{f" transform={chr(34)}{trafo}{chr(34)}" if trafo else ""}>',
         *(f'    {t}' for t in innen),
         '  </g>']
    if zustand == "stoerung":
        cx, cy = abb(84, 45)
        s.append(f'  {warnung(cx, cy)}')
    s.append('</svg>')
    return "\n".join(s) + "\n"


def main() -> None:
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ZIEL
    ziel.mkdir(parents=True, exist_ok=True)
    for richtung in RICHTUNGEN:
        for zustand in ("aus", "an", "stoerung"):
            p = ziel / f"Klimakonvektor_{richtung}_{zustand}.svg"
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(svg(richtung, zustand))
            print(p.name)
        # bisheriger Name ohne Zustand = Zustand „aus“ (Kompatibilität)
        p = ziel / f"Klimakonvektor_{richtung}.svg"
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg(richtung, "aus"))
        print(p.name)


if __name__ == "__main__":
    main()
