"""Erzeugt symbole/hydraulik/Pumpe_{richtung}_{zustand} (SVG + PNG, resvg-py).

Pumpe 40 × 40, Kreis mit Förderpfeil (Dreieck). Aufruf: python tools/pumpe.py

Richtungen: oben, rechts, unten, links – das Dreieck ist in jeder Datei fest gedreht
(Niagara kann Bilder nicht drehen).

Zustände:
  _aus        grau
  _freigabe   gelb, pulsiert weich (1,4 s)
  _an         grün, drei lange Segmente drehen, Fließpfeile laufen im Dreieck Richtung Spitze
  _stoerung   rot, pulsiert weich (1,4 s), kleines Warndreieck mit „!“ in der Mitte pulsiert mit
Animation per SMIL. Ohne Animation (PNG, oder SVG ohne SMIL) bleibt die Zustandsfarbe sichtbar,
nur Fließpfeile und Bewegung fehlen.
"""
from pathlib import Path

RICHTUNGEN = {"oben": 0, "rechts": 90, "unten": 180, "links": 270}

FARBEN = {  # Verlauf oben → unten, Kontur
    "aus": ("#EDEDED", "#A6A6A6", "#808080"),
    "freigabe": ("#FFEB8F", "#E3B200", "#A88400"),
    "an": ("#A8DC96", "#3E9A3A", "#2F7A2C"),
    "stoerung": ("#F5A3A0", "#D7302B", "#9E1F1B"),
}
TITEL = {"aus": "aus", "freigabe": "Freigabe", "an": "Betrieb", "stoerung": "Störung"}

PULS = ('<animate attributeName="opacity" values="1;0.35;1" keyTimes="0;0.5;1" calcMode="spline" '
        'keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="1.4s" repeatCount="indefinite"/>')
DREHUNG = '<animateTransform attributeName="transform" type="rotate" from="0 20 20" to="360 20 20" dur="1.6s" repeatCount="indefinite"/>'
DREIECK = '<path d="M20,5 L32.5,28.5 L7.5,28.5 Z" fill="#4D4D4D" stroke="#4D4D4D" stroke-width="1.2" stroke-linejoin="round"/>'


def fliesspfeil(beginn: str) -> str:
    return ('<path d="M15.5,26.5 L20,22 L24.5,26.5" fill="none" stroke="#E6E6E6" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.2;0.7;1" dur="1.2s" begin="{beginn}" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -8" dur="1.2s" begin="{beginn}" repeatCount="indefinite"/></path>')


def svg(richtung: str, zustand: str) -> str:
    oben, unten, kontur = FARBEN[zustand]
    kreis = f'<circle cx="20" cy="20" r="18" fill="url(#gK)" stroke="{kontur}" stroke-width="1.6"/>'
    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40" role="img" aria-labelledby="title">',
         f'  <title id="title">Pumpe, Förderrichtung {richtung}, {TITEL[zustand]}</title>',
         f'  <defs><linearGradient id="gK" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{oben}"/><stop offset="1" stop-color="{unten}"/></linearGradient></defs>']
    if zustand in ("freigabe", "stoerung"):
        s.append(f'  <g>{PULS}{kreis}</g>')
    else:
        s.append(f'  {kreis}')
    if zustand == "an":
        s.append(f'  <circle cx="20" cy="20" r="16" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="2" stroke-linecap="round" stroke-dasharray="22 11.5">{DREHUNG}</circle>')
    s.append(f'  <g transform="rotate({RICHTUNGEN[richtung]} 20 20)">')
    s.append(f'    {DREIECK}')
    if zustand == "an":
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
    import resvg_py
    out = Path(__file__).resolve().parent.parent / "symbole" / "hydraulik"
    for richtung in RICHTUNGEN:
        for zustand in FARBEN:
            p = out / f"Pumpe_{richtung}_{zustand}.svg"
            p.write_text(svg(richtung, zustand), encoding="utf-8")
            p.with_suffix(".png").write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=svg(richtung, zustand))))
            print(p)
