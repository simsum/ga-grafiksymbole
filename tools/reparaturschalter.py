#!/usr/bin/env python3
"""Erzeugt symbole/anzeigen/schalter/Reparaturschalter_{ein,aus}.svg.

Reparaturschalter als eckige Plakette 24 × 24 (wie Kanalrauchmelder und Brandalarm), darin ein klassischer
Hauptschalter: gelber Grund, roter Drehgriff, Markierungen „I“ (oben) und „0“ (rechts). Beide Dateien gleich groß,
alle Teile an derselben Stelle. Aufruf: python tools/reparaturschalter.py

  _ein  Griff senkrecht auf „I“, Plakette hellgrau, statisch
  _aus  Griff waagerecht auf „0“ (Reparatur), Plakette gelb (Zustandsfarbe Freigabe/Wartung) und pulsiert weich
        (1,4 s), kleines Vorhängeschloss unten links: gesichert
"""
from pathlib import Path

from zustandsfarben import AUS, FREIGABE

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "anzeigen" / "schalter"
GRAU = AUS[2]


def svg(zustand: str) -> str:
    ein = zustand == "ein"
    oben, unten, _ = AUS if ein else FREIGABE
    s = [f'<defs><linearGradient id="gK" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{oben}"/>'
         f'<stop offset="1" stop-color="{unten}"/></linearGradient></defs>']
    # Plakette: nur die Füllung pulsiert, der graue Rand bleibt fest
    feld = '<rect x="1.5" y="1.5" width="21" height="21" rx="4" fill="url(#gK)"/>'
    if ein:
        s.append(feld)
    else:
        s.append('<g><animate attributeName="opacity" values="1;0.4;1" keyTimes="0;0.5;1" calcMode="spline" '
                 f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="1.4s" repeatCount="indefinite"/>{feld}</g>')
    s.append(f'<rect x="1.5" y="1.5" width="21" height="21" rx="4" fill="none" stroke="{GRAU}" stroke-width="1.2"/>')
    # Hauptschalter: gelber Grund, Markierungen I und 0, roter Griff
    s.append('<circle cx="12" cy="12" r="8" fill="#F2C230" stroke="#4D4D4D" stroke-width="1"/>')
    s.append('<path d="M12,4.6 v1.8" stroke="#4D4D4D" stroke-width="0.9"/>'
             '<circle cx="18.6" cy="12" r="0.9" fill="none" stroke="#4D4D4D" stroke-width="0.7"/>')
    s.append(f'<g transform="rotate({0 if ein else 90} 12 12)"><rect x="10.3" y="5.6" width="3.4" height="12.8" rx="1.7" '
             'fill="#D7302B" stroke="#8E1C14" stroke-width="0.8"/><circle cx="12" cy="12" r="1.2" fill="#FFFFFF" fill-opacity="0.8"/></g>')
    if not ein:
        s.append('<g transform="translate(3.2 13.6)"><path d="M1.6,3 V1.9 a1.6,1.6 0 0 1 3.2,0 V3" fill="none" '
                 'stroke="#2A2A2A" stroke-width="0.9"/><rect x="0.8" y="3" width="4.8" height="3.8" rx="0.7" fill="#2A2A2A"/></g>')
    titel = "Ein" if ein else "Aus (Reparatur, gesichert)"
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" role="img">\n'
            f'  <title>Reparaturschalter, {titel}</title>\n  ' + "".join(s) + '\n</svg>\n')


def main() -> None:
    ZIEL.mkdir(parents=True, exist_ok=True)
    for zustand in ("ein", "aus"):
        p = ZIEL / f"Reparaturschalter_{zustand}.svg"
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg(zustand))
        print(p.name)


if __name__ == "__main__":
    main()
