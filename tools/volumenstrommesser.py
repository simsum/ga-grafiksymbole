#!/usr/bin/env python3
"""Erzeugt symbole/lueftung/volumenstrommesser/Volumenstrommesser_{lage}_{zustand}.svg.

Volumenstrommesser, aufgebaut wie der Kanalrauchmelder, aber mit rundem Kopf (d = 24): Füllung in Zustandsfarbe,
fester grauer Rand, darin ein Zeigerinstrument; schlankes Messrohr mit Messöffnungen zur Kanalmitte.
Aufruf: python tools/volumenstrommesser.py

Alle Dateien 40 × 40, für jede Lage und jeden Zustand gleich; Kopf und Rohr liegen je Lage immer an derselben Stelle.
Lage = Seite des Kanals, auf der das Gerät sitzt; Rohrende auf der Kanalmitte:
  oben    Kopfmitte (20, 12), Rohrende x = 20, y = 40     unten   Kopfmitte (20, 28), Rohrende x = 20, y = 0
  links   Kopfmitte (12, 20), Rohrende x = 40, y = 20     rechts  Kopfmitte (28, 20), Rohrende x = 0,  y = 20

Zustände (Farben aus zustandsfarben.py):
  _normal    hellgrau, Zeiger steht
  _messung   grün, Zeiger pendelt ruhig hin und her (weich, 6 s)
  _stoerung  rot, Füllung pulsiert weich (1,4 s), Warndreieck statt Instrument
"""
from pathlib import Path

from zustandsfarben import AUS, BETRIEB, STOERUNG

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "lueftung" / "volumenstrommesser"
GRAU, DUNKEL = AUS[2], "#4D4D4D"
W = H = 40
FARBEN = {"normal": AUS, "messung": BETRIEB, "stoerung": STOERUNG}
TITEL = {"normal": "Normal", "messung": "Messung", "stoerung": "Störung"}
# Kopfmitte, Messrohr (x, y, b, h), Messöffnungen
LAGEN = {"oben": ((20, 12), (18.5, 23, 3, 17), ((20, 33), (20, 37))),
         "unten": ((20, 28), (18.5, 0, 3, 17), ((20, 3), (20, 7))),
         "links": ((12, 20), (23, 18.5, 17, 3), ((33, 20), (37, 20))),
         "rechts": ((28, 20), (0, 18.5, 17, 3), ((3, 20), (7, 20)))}


def puls(dur: str, tief: float = 0.4) -> str:
    return (f'<animate attributeName="opacity" values="1;{tief};1" keyTimes="0;0.5;1" calcMode="spline" '
            f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="{dur}" repeatCount="indefinite"/>')


def instrument(cx: float, cy: float, messung: bool) -> str:
    """Skalenbogen mit drei Teilstrichen, Zeiger um (cx, cy + 3)."""
    zx, zy = cx, cy + 3
    zeiger = f'<line x1="{zx}" y1="{zy}" x2="{zx}" y2="{zy - 8}" stroke="{DUNKEL}" stroke-width="1.6" stroke-linecap="round"/>'
    anim = (f'<animateTransform attributeName="transform" type="rotate" values="0 {zx} {zy};30 {zx} {zy};15 {zx} {zy};0 {zx} {zy}" '
            'keyTimes="0;0.4;0.7;1" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1;0.45 0 0.55 1" dur="6s" '
            'repeatCount="indefinite"/>') if messung else ""
    return (f'<path d="M{cx - 6.5},{cy + 3} A7,7 0 1 1 {cx + 6.5},{cy + 3}" fill="none" stroke="{DUNKEL}" stroke-width="1.2" '
            'stroke-linecap="round"/>'
            f'<path d="M{cx - 5.4},{cy - 1.4} l1.3,0.8 M{cx},{cy - 4.6} v1.5 M{cx + 5.4},{cy - 1.4} l-1.3,0.8" stroke="{DUNKEL}" '
            'stroke-width="0.9"/>'
            f'<g transform="rotate(-20 {zx} {zy})"><g>{anim}{zeiger}</g></g>'
            f'<circle cx="{zx}" cy="{zy}" r="1.3" fill="{DUNKEL}"/>')


def svg(lage: str, zustand: str) -> str:
    (cx, cy), (rx, ry, rb, rh), loecher = LAGEN[lage]
    oben, unten, _ = FARBEN[zustand]
    s = [f'<defs><linearGradient id="gK" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{oben}"/>'
         f'<stop offset="1" stop-color="{unten}"/></linearGradient></defs>',
         f'<rect x="{rx}" y="{ry}" width="{rb}" height="{rh}" fill="#B5B5B5" stroke="{GRAU}" stroke-width="0.8"/>',
         '<g fill="#4D4D4D">' + "".join(f'<circle cx="{x}" cy="{y}" r="0.7"/>' for x, y in loecher) + '</g>']
    # Kopf: nur die Füllung pulsiert, der graue Rand bleibt fest
    kopf = f'<circle cx="{cx}" cy="{cy}" r="10.5" fill="url(#gK)"/>'
    s.append(f'<g>{puls("1.4s")}{kopf}</g>' if zustand == "stoerung" else kopf)
    s.append(f'<circle cx="{cx}" cy="{cy}" r="10.5" fill="none" stroke="{GRAU}" stroke-width="1.2"/>')
    if zustand == "stoerung":
        s.append(f'<g>{puls("1.4s")}<path d="M{cx},{cy - 7.5} L{cx + 8},{cy + 6} L{cx - 8},{cy + 6} Z" fill="#E2231A" '
                 'stroke="#FFFFFF" stroke-width="1.4" stroke-linejoin="round"/>'
                 f'<rect x="{cx - 0.8}" y="{cy - 3.8}" width="1.6" height="5.6" rx="0.8" fill="#FFFFFF"/>'
                 f'<circle cx="{cx}" cy="{cy + 3.6}" r="0.9" fill="#FFFFFF"/></g>')
    else:
        s.append(instrument(cx, cy, zustand == "messung"))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">\n'
            f'  <title>Volumenstrommesser, Gerät {lage} am Kanal, {TITEL[zustand]}</title>\n  ' + "".join(s) + '\n</svg>\n')


def main() -> None:
    ZIEL.mkdir(parents=True, exist_ok=True)
    for lage in LAGEN:
        for zustand in FARBEN:
            p = ZIEL / f"Volumenstrommesser_{lage}_{zustand}.svg"
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(svg(lage, zustand))
            print(p.name)


if __name__ == "__main__":
    main()
