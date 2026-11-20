#!/usr/bin/env python3
"""Erzeugt symbole/anzeigen/alarm/Heizungsnotschalter_{normal,ausgeloest}.svg.

Anzeige für den Heizungs-Notschalter, aufgebaut wie die Brandalarm-Anzeige (tools/brandalarm.py): eckige
Plakette 24 × 24 mittig in einem 40 × 24-Bild, links und rechts Platz für Alarmwellen. Beide Dateien gleich groß,
Plakette immer bei (8, 0). Darauf ein Not-Aus-Pilztaster von vorn mit kleiner Flamme im Knopf.
Aufruf: python tools/heizungsnotschalter.py

  _normal      hellgrau, Taster und Flamme als dunkelgrauer Umriss, statisch
  _ausgeloest  rot (Zustandsfarbe Störung), Füllung pulsiert (0,6 s), Taster farbig (gelber Ring, roter Knopf,
               weiße Flamme), Alarmwellen links und rechts blinken (2 Hz)
Ohne Animation bleiben Farbe, Taster und Alarmwellen sichtbar.
"""
from pathlib import Path

from brandalarm import FLAMME
from zustandsfarben import AUS, STOERUNG

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "anzeigen" / "alarm"
GRAU = AUS[2]
DUNKEL = "#4D4D4D"
W, H, PX = 40, 24, 8
CX, CY = PX + 12, 12
S = 0.4                       # Skalierung der Flamme (Original 16 hoch, um (12, 12))


def flamme(fill: str, stroke: str, breite: float) -> str:
    return (f'<path d="{FLAMME}" transform="translate({CX} {CY + 0.3}) scale({S}) translate(-12 -12)" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{breite / S:.2f}" stroke-linejoin="round"/>')


def svg(zustand: str) -> str:
    alarm = zustand == "ausgeloest"
    oben, unten, _ = STOERUNG if alarm else AUS
    s = [f'<defs><linearGradient id="gK" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{oben}"/>'
         f'<stop offset="1" stop-color="{unten}"/></linearGradient>'
         '<linearGradient id="gP" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F26A60"/>'
         '<stop offset="1" stop-color="#B8231C"/></linearGradient></defs>']
    feld = f'<rect x="{PX + 1.5}" y="1.5" width="21" height="21" rx="4" fill="url(#gK)"/>'
    if alarm:
        s.append('<g><animate attributeName="opacity" values="1;0.4;1" keyTimes="0;0.5;1" calcMode="spline" '
                 f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="0.6s" repeatCount="indefinite"/>{feld}</g>')
    else:
        s.append(feld)
    s.append(f'<rect x="{PX + 1.5}" y="1.5" width="21" height="21" rx="4" fill="none" stroke="{GRAU}" stroke-width="1.2"/>')
    if alarm:
        # gelber Ring, roter Pilzknopf, weiße Flamme
        s.append(f'<circle cx="{CX}" cy="{CY}" r="8.4" fill="#FFD34D" stroke="#FFFFFF" stroke-width="1.2"/>')
        s.append(f'<circle cx="{CX}" cy="{CY}" r="5.6" fill="url(#gP)" stroke="#9E1F1B" stroke-width="1"/>')
        s.append(flamme("#FFFFFF", "none", 0))
        l, r = PX - 1.5, PX + 25.5
        s.append(f'<g fill="none" stroke="{STOERUNG[1]}" stroke-width="1.4" stroke-linecap="round">'
                 '<animate attributeName="opacity" values="1;0.15" dur="0.5s" calcMode="discrete" repeatCount="indefinite"/>'
                 f'<path d="M{l},7 q-2,5 0,10"/><path d="M{l - 2.5},4.5 q-2.5,7.5 0,15" stroke-opacity="0.6"/>'
                 f'<path d="M{r},7 q2,5 0,10"/><path d="M{r + 2.5},4.5 q2.5,7.5 0,15" stroke-opacity="0.6"/></g>')
    else:
        s.append(f'<circle cx="{CX}" cy="{CY}" r="8.4" fill="none" stroke="{DUNKEL}" stroke-width="1.3"/>')
        s.append(f'<circle cx="{CX}" cy="{CY}" r="5.6" fill="none" stroke="{DUNKEL}" stroke-width="1.3"/>')
        s.append(flamme("none", DUNKEL, 1))
    titel = "ausgelöst" if alarm else "normal"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">\n'
            f'  <title>Heizungs-Notschalter, {titel}</title>\n  ' + "".join(s) + '\n</svg>\n')


def main() -> None:
    ZIEL.mkdir(parents=True, exist_ok=True)
    for zustand in ("normal", "ausgeloest"):
        p = ZIEL / f"Heizungsnotschalter_{zustand}.svg"
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg(zustand))
        print(p.name)


if __name__ == "__main__":
    main()
