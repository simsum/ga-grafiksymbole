#!/usr/bin/env python3
"""Erzeugt symbole/anzeigen/alarm/Brandalarm_{normal,alarm}.svg.

Brandalarm-Anzeige: eckige Plakette 24 × 24 (wie Kanalrauchmelder und Frostschutzwächter) mittig in einem
40 × 24-Bild, links und rechts Platz für Alarmwellen. Beide Dateien gleich groß, Plakette immer bei (8, 0).
Aufruf: python tools/brandalarm.py

  _normal  hellgrau, dunkelgraue Flamme als Umriss, statisch
  _alarm   rot (Zustandsfarbe Störung), Füllung pulsiert schnell (0,6 s), gefüllte Flamme (Rot → Orange → Gelb,
           heller Kern) flackert, Alarmwellen links und rechts blinken (2 Hz)
Ohne Animation bleiben Farbe, Flamme und Alarmwellen sichtbar.
"""
from pathlib import Path

from zustandsfarben import AUS, STOERUNG

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "anzeigen" / "alarm"
GRAU = AUS[2]
W, H, PX = 40, 24, 8
FLAMME = ("M12,4 C13.6,7.6 17.4,9.6 17.2,14 C17,17.6 14.8,20 12,20 C9.1,20 6.8,17.8 6.9,14.9 C7,12.6 8.4,11.3 9.3,10 "
          "C9.5,11.8 10.3,12.9 11.3,13.2 C10.8,10 11,7 12,4 Z")
KERN = "M12,13 C13,14.4 14.4,15.4 14.2,17 C14,18.4 13.1,19.2 12,19.2 C10.8,19.2 9.9,18.3 10,17.1 C10.1,15.8 11.4,15 12,13 Z"


def svg(zustand: str) -> str:
    alarm = zustand == "alarm"
    oben, unten, _ = STOERUNG if alarm else AUS
    s = [f'<defs><linearGradient id="gK" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{oben}"/>'
         f'<stop offset="1" stop-color="{unten}"/></linearGradient>'
         '<linearGradient id="gF" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#E0302A"/>'
         '<stop offset="0.5" stop-color="#F29A38"/><stop offset="1" stop-color="#FFD34D"/></linearGradient></defs>']
    # Plakette: nur die Füllung pulsiert, der graue Rand bleibt fest
    feld = f'<rect x="{PX + 1.5}" y="1.5" width="21" height="21" rx="4" fill="url(#gK)"/>'
    if alarm:
        s.append('<g><animate attributeName="opacity" values="1;0.4;1" keyTimes="0;0.5;1" calcMode="spline" '
                 f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="0.6s" repeatCount="indefinite"/>{feld}</g>')
    else:
        s.append(feld)
    s.append(f'<rect x="{PX + 1.5}" y="1.5" width="21" height="21" rx="4" fill="none" stroke="{GRAU}" stroke-width="1.2"/>')
    if alarm:
        # Flamme flackert (Skalierung um den Fußpunkt), Alarmwellen blinken
        s.append(f'<g transform="translate({PX + 12} 20)"><g><animateTransform attributeName="transform" type="scale" '
                 'values="1 1;0.94 1.08;1.04 0.94;1 1" dur="0.5s" repeatCount="indefinite"/>'
                 f'<g transform="translate(-12 -20)"><path d="{FLAMME}" fill="url(#gF)" stroke="#FFFFFF" stroke-width="1.3" '
                 f'stroke-linejoin="round"/><path d="{KERN}" fill="#FFF3B0"/></g></g></g>')
        l, r = PX - 1.5, PX + 25.5
        s.append(f'<g fill="none" stroke="{STOERUNG[1]}" stroke-width="1.4" stroke-linecap="round">'
                 '<animate attributeName="opacity" values="1;0.15" dur="0.5s" calcMode="discrete" repeatCount="indefinite"/>'
                 f'<path d="M{l},7 q-2,5 0,10"/><path d="M{l - 2.5},4.5 q-2.5,7.5 0,15" stroke-opacity="0.6"/>'
                 f'<path d="M{r},7 q2,5 0,10"/><path d="M{r + 2.5},4.5 q2.5,7.5 0,15" stroke-opacity="0.6"/></g>')
    else:
        s.append(f'<path d="{FLAMME}" transform="translate({PX} 0)" fill="none" stroke="#4D4D4D" stroke-width="1.5" '
                 'stroke-linejoin="round"/>')
    titel = "Alarm" if alarm else "Normal"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">\n'
            f'  <title>Brandalarm, {titel}</title>\n  ' + "".join(s) + '\n</svg>\n')


def main() -> None:
    ZIEL.mkdir(parents=True, exist_ok=True)
    for zustand in ("normal", "alarm"):
        p = ZIEL / f"Brandalarm_{zustand}.svg"
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg(zustand))
        print(p.name)


if __name__ == "__main__":
    main()
