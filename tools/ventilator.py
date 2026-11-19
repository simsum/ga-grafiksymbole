#!/usr/bin/env python3
"""Erzeugt symbole/lueftung/ventilatoren/Ventilator_{richtung}_{zustand}.svg.

Ventilator 60 × 60 (gezeichnet im 40er-Raster wie die Pumpe, viewBox 0 0 40 40), aufgebaut wie die Pumpe (tools/pumpe.py): Kreis in Zustandsfarbe, statt des Förderdreiecks
das Ventilatorzeichen nach DIN EN 12792: zwei Linien von Kreisrand zu Kreisrand, die in Förderrichtung
zusammenlaufen. Aufruf: python tools/ventilator.py

Richtungen: oben, rechts, unten, links (fest gedreht, Niagara kann Bilder nicht drehen).

Zustände wie bei der Pumpe:
  _aus        grau
  _freigabe   gelb, Füllung pulsiert weich (1,4 s), Außenring bleibt fest
  _an         grün, drei lange Segmente drehen, Luftpfeile laufen zwischen den Linien in Förderrichtung
  _stoerung   rot, Füllung pulsiert weich (1,4 s), kleines Warndreieck mit „!“ in der Mitte pulsiert mit
  _an_punkte  wie _an, statt der Luftpfeile laufen drei helle Punkte zur engen Seite
Kreiskontur und Linien immer grau (Kontur „aus“; Linien 1,4 px), Luftpfeile hell (#E6E6E6) wie bei der Pumpe.

Variante Ventilator_Fluegel_{richtung}_{zustand}: statt des umlaufenden Rings ein angedeutetes Lüfterrad
(drei helle Flügel um eine Nabe) hinter den Linien, dreht bei _an; in den anderen Zuständen steht es.
Luftpfeile und Punkte hier dunkel (#4D4D4D), damit sie sich von den hellen Flügeln abheben; auch mit _an_punkte.
Ohne Animation bleibt die Zustandsfarbe sichtbar, nur Luftpfeile und Bewegung fehlen.
"""
import math
from pathlib import Path

from zustandsfarben import AUS
from pumpe import DREHUNG, FARBEN, PULS, RICHTUNGEN, TITEL, fliesspunkt

LINIE = AUS[2]   # Grau der Kontur im Zustand „aus“
ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "lueftung" / "ventilatoren"


def kreispunkt(grad: float, r: float = 18) -> tuple[float, float]:
    a = math.radians(grad)
    return 20 + r * math.cos(a), 20 + r * math.sin(a)


# Förderrichtung „oben“: Linien beginnen unten weit auseinander (±55° neben der Senkrechten)
# und enden oben enger (±20°), beide Enden auf dem Kreisrand
_UL, _OL = kreispunkt(125), kreispunkt(250)
_UR, _OR = kreispunkt(55), kreispunkt(290)
def zeichen(farbe: str) -> str:
    """Die beiden Linien, in allen Zuständen grau."""
    return (f'<path d="M{_UL[0]:.2f},{_UL[1]:.2f} L{_OL[0]:.2f},{_OL[1]:.2f} M{_UR[0]:.2f},{_UR[1]:.2f} L{_OR[0]:.2f},{_OR[1]:.2f}" '
            f'fill="none" stroke="{farbe}" stroke-width="1.4" stroke-linecap="round"/>')


def fluegel(drehen: bool) -> str:
    """Angedeutetes Lüfterrad: drei helle Flügel um eine Nabe, hinter den Linien; dreht im Betrieb."""
    blatt = 'M20,20 C17,16 16.5,9 20,4.5 C23.5,7 24,13 20,20 Z'
    teile = "".join(f'<path d="{blatt}" transform="rotate({a} 20 20)"/>' for a in (0, 120, 240))
    anim = DREHUNG if drehen else ""
    return (f'<g fill="#FFFFFF" fill-opacity="0.5" stroke="#FFFFFF" stroke-opacity="0.75" stroke-width="0.8" stroke-linejoin="round">'
            f'<g>{anim}{teile}</g></g><circle cx="20" cy="20" r="2.6" fill="#FFFFFF" fill-opacity="0.8"/>')


def luftpfeil(beginn: str, farbe: str) -> str:
    """Kleiner Winkel wandert zwischen den Linien zur engen Seite (hell wie der Fließpfeil der Pumpe)."""
    return (f'<path d="M15.5,28 L20,23.5 L24.5,28" fill="none" stroke="{farbe}" stroke-width="1.8" stroke-linecap="round" '
            'stroke-linejoin="round" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.2;0.7;1" dur="1.2s" begin="{beginn}" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -14" dur="1.2s" begin="{beginn}" repeatCount="indefinite"/></path>')


def svg(richtung: str, zustand: str, punkte: bool = False, mit_fluegel: bool = False) -> str:
    oben, unten, kontur = FARBEN[zustand]
    pfeil = "#4D4D4D" if mit_fluegel else "#E6E6E6"   # auf den hellen Flügeln dunkel, sonst hell wie bei der Pumpe
    # Nur die Füllung pulsiert; der graue Außenring liegt fest darüber
    kreis = '<circle cx="20" cy="20" r="18" fill="url(#gK)"/>'
    ring = f'<circle cx="20" cy="20" r="18" fill="none" stroke="{LINIE}" stroke-width="1.6"/>'
    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 40 40" role="img" aria-labelledby="title">',
         f'  <title id="title">Ventilator{" mit Lüfterflügel" if mit_fluegel else ""}, Förderrichtung {richtung}, {TITEL[zustand]}{", Fließpunkte" if punkte else ""}</title>',
         f'  <defs><linearGradient id="gK" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{oben}"/><stop offset="1" stop-color="{unten}"/></linearGradient></defs>']
    s.append(f'  <g>{PULS}{kreis}</g>' if zustand in ("freigabe", "stoerung") else f'  {kreis}')
    s.append(f'  {ring}')
    if mit_fluegel:
        s.append(f'  {fluegel(zustand == "an")}')
    elif zustand == "an":
        s.append(f'  <circle cx="20" cy="20" r="16" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="2" '
                 f'stroke-linecap="round" stroke-dasharray="22 11.5">{DREHUNG}</circle>')
    s.append(f'  <g transform="rotate({RICHTUNGEN[richtung]} 20 20)">')
    s.append(f'    {zeichen(LINIE)}')
    if zustand == "an" and punkte:
        s.extend(f'    {fliesspunkt(b)}'.replace("#E6E6E6", "#4D4D4D" if mit_fluegel else "#FFFFFF") for b in ("0s", "0.4s", "0.8s"))
    elif zustand == "an":
        s.append(f'    {luftpfeil("0s", pfeil)}')
        s.append(f'    {luftpfeil("0.6s", pfeil)}')
    s.append('  </g>')
    if zustand == "stoerung":
        s.append(f'  <g>{PULS}')
        s.append('    <path d="M20,13 L27,25.5 L13,25.5 Z" fill="#E2231A" stroke="#FFFFFF" stroke-width="1.4" stroke-linejoin="round"/>')
        s.append('    <rect x="19.25" y="16.3" width="1.5" height="5.2" rx="0.75" fill="#FFFFFF"/>')
        s.append('    <circle cx="20" cy="23.3" r="0.85" fill="#FFFFFF"/>')
        s.append('  </g>')
    s.append('</svg>')
    return "\n".join(s) + "\n"


def schreib(p: Path, inhalt: str) -> None:
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(inhalt)
    print(p.name)


def main() -> None:
    ZIEL.mkdir(parents=True, exist_ok=True)
    for richtung in RICHTUNGEN:
        for zustand in FARBEN:
            schreib(ZIEL / f"Ventilator_{richtung}_{zustand}.svg", svg(richtung, zustand))
        schreib(ZIEL / f"Ventilator_{richtung}_an_punkte.svg", svg(richtung, "an", punkte=True))
        for zustand in FARBEN:
            schreib(ZIEL / f"Ventilator_Fluegel_{richtung}_{zustand}.svg", svg(richtung, zustand, mit_fluegel=True))
        schreib(ZIEL / f"Ventilator_Fluegel_{richtung}_an_punkte.svg", svg(richtung, "an", punkte=True, mit_fluegel=True))


if __name__ == "__main__":
    main()
