"""Erzeugt symbole/hydraulik/pumpen/Pumpe_{richtung}_{zustand}.svg.

Pumpe 40 × 40, Kreis mit Förderpfeil (Dreieck). Aufruf: python tools/pumpe.py

Richtungen: oben, rechts, unten, links – das Dreieck ist in jeder Datei fest gedreht
(Niagara kann Bilder nicht drehen).

Zustände:
  _aus        grau
  _freigabe   gelb, pulsiert weich (1,4 s)
  _an         grün, drei lange Segmente drehen, Fließpfeile laufen im Dreieck Richtung Spitze
  _stoerung   rot, pulsiert weich (1,4 s), kleines Warndreieck mit „!“ in der Mitte pulsiert mit
  _an_punkte  wie _an, statt der Fließpfeile laufen drei helle Punkte in einer Spur zur Spitze
              (wie bei Flusspfeil_*_an)
Außenring (1,6 px) und Förderdreieck immer grau (#808080, Kontur „aus“); nur die Füllung zeigt den Zustand,
bei Freigabe und Störung pulsiert nur die Füllung, der Ring bleibt fest.
Animation per SMIL. Ohne Animation (Darstellung ohne SMIL) bleibt die Zustandsfarbe sichtbar,
nur Fließpfeile und Bewegung fehlen.
"""
from pathlib import Path

from zustandsfarben import AUS, ZUSTAENDE

RICHTUNGEN = {"oben": 0, "rechts": 90, "unten": 180, "links": 270}

FARBEN = ZUSTAENDE  # Verlauf oben → unten, Kontur; einheitlich für alle Symbole (tools/zustandsfarben.py)
TITEL = {"aus": "aus", "freigabe": "Freigabe", "an": "Betrieb", "stoerung": "Störung"}

PULS = ('<animate attributeName="opacity" values="1;0.35;1" keyTimes="0;0.5;1" calcMode="spline" '
        'keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="1.4s" repeatCount="indefinite"/>')
DREHUNG = '<animateTransform attributeName="transform" type="rotate" from="0 20 20" to="360 20 20" dur="1.6s" repeatCount="indefinite"/>'
GRAU = AUS[2]   # Außenring und Förderdreieck in allen Zuständen grau (wie beim Ventilator)
DREIECK = f'<path d="M20,5 L32.5,28.5 L7.5,28.5 Z" fill="{GRAU}" stroke="{GRAU}" stroke-width="1.2" stroke-linejoin="round"/>'


def fliesspfeil(beginn: str) -> str:
    return ('<path d="M15.5,26.5 L20,22 L24.5,26.5" fill="none" stroke="#E6E6E6" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.2;0.7;1" dur="1.2s" begin="{beginn}" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -8" dur="1.2s" begin="{beginn}" repeatCount="indefinite"/></path>')


def fliesspunkt(beginn: str) -> str:
    return ('<circle cx="20" cy="26" r="1.5" fill="#E6E6E6" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.75;1" dur="1.2s" begin="{beginn}" repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="26;11" dur="1.2s" begin="{beginn}" repeatCount="indefinite"/></circle>')


def svg(richtung: str, zustand: str, punkte: bool = False) -> str:
    oben, unten, _ = FARBEN[zustand]
    # Nur die Füllung trägt den Zustand und pulsiert; der graue Außenring liegt fest darüber
    kreis = '<circle cx="20" cy="20" r="18" fill="url(#gK)"/>'
    ring = f'<circle cx="20" cy="20" r="18" fill="none" stroke="{GRAU}" stroke-width="1.6"/>'
    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40" role="img" aria-labelledby="title">',
         f'  <title id="title">Pumpe, Förderrichtung {richtung}, {TITEL[zustand]}{", Fließpunkte" if punkte else ""}</title>',
         f'  <defs><linearGradient id="gK" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{oben}"/><stop offset="1" stop-color="{unten}"/></linearGradient></defs>']
    if zustand in ("freigabe", "stoerung"):
        s.append(f'  <g>{PULS}{kreis}</g>')
    else:
        s.append(f'  {kreis}')
    s.append(f'  {ring}')
    if zustand == "an":
        s.append(f'  <circle cx="20" cy="20" r="16" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="2" stroke-linecap="round" stroke-dasharray="22 11.5">{DREHUNG}</circle>')
    s.append(f'  <g transform="rotate({RICHTUNGEN[richtung]} 20 20)">')
    s.append(f'    {DREIECK}')
    if zustand == "an" and punkte:
        s.extend(f'    {fliesspunkt(b)}' for b in ("0s", "0.4s", "0.8s"))
    elif zustand == "an":
        s.append(f'    {fliesspfeil("0s")}')
        s.append(f'    {fliesspfeil("0.6s")}')
    s.append('  </g>')
    if zustand == "stoerung":
        s.append(f'  <g>{PULS}')
        s.append('    <path d="M20,13 L27,25.5 L13,25.5 Z" fill="#E2231A" stroke="#FFFFFF" stroke-width="1.4" stroke-linejoin="round"/>')
        s.append('    <rect x="19.25" y="16.3" width="1.5" height="5.2" rx="0.75" fill="#FFFFFF"/>')
        s.append('    <circle cx="20" cy="23.3" r="0.85" fill="#FFFFFF"/>')
        s.append('  </g>')
    s.append('</svg>')
    return "\n".join(s) + "\n"


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "symbole" / "hydraulik" / "pumpen"
    for richtung in RICHTUNGEN:
        for zustand in FARBEN:
            p = out / f"Pumpe_{richtung}_{zustand}.svg"
            p.write_text(svg(richtung, zustand), encoding="utf-8", newline="\n")
            print(p)
        p = out / f"Pumpe_{richtung}_an_punkte.svg"
        p.write_text(svg(richtung, "an", punkte=True), encoding="utf-8", newline="\n")
        print(p)
