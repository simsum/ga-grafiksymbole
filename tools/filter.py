#!/usr/bin/env python3
"""Erzeugt symbole/lueftung/filter/Filter[_Taschen]_{richtung}[_verschmutzt].svg.

Aufruf: python tools/filter.py

  Filter_<richtung>          Luftfilter wie im bestehenden Anlagenbild: graues Gehäuse (quer leicht gewölbt),
                             darin ein heller Keil (senkrechte Anströmkante, Spitze in Strömungsrichtung); statisch
  Filter_Taschen_<richtung>  Taschenfilter von vorn wie im Foto: Rahmen mit zwei Zellen übereinander, je fünf
                             senkrechte Stege zwischen weißen Taschen. Staubteilchen fliegen von der Anströmseite
                             heran und werden vom Filter aufgefangen (SMIL)

  rechts, links  40 × 80 für waagerechte Kanäle (Kanalachse y = 40), Strömung nach rechts bzw. links
  oben, unten    80 × 40 für senkrechte Kanäle (Kanalachse x = 40)

  _verschmutzt   Filterfläche bräunlich mit Schmutzflecken, Staub bleibt hängen; der Filter blinkt leicht gelb
                 (Freigabe-/Warngelb aus zustandsfarben.py, 1 Hz wie die Störungsanzeigen).
                 Ohne Animation bleibt der verschmutzte Filter sichtbar.
"""
from pathlib import Path

from zustandsfarben import FREIGABE

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "lueftung" / "filter"
DREHUNG = {"rechts": 0, "unten": 90, "links": 180, "oben": 270}
KONTUR, KEIL_K = "#808080", "#5A5A5A"
GELB = FREIGABE[1]

DEFS = ('<defs>'
        '<linearGradient id="gH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9A9A9A"/>'
        '<stop offset="0.45" stop-color="#E6E6E6"/><stop offset="1" stop-color="#A6A6A6"/></linearGradient>'
        '<linearGradient id="gK" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF"/>'
        '<stop offset="1" stop-color="#E9E9E9"/></linearGradient>'
        '<linearGradient id="gS" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8E7A5E"/>'
        '<stop offset="0.5" stop-color="#B7A487"/><stop offset="1" stop-color="#D9CDB8"/></linearGradient>'
        '</defs>')

KEIL = "M9,3 L33,40 L9,77 Z"
# Schmutzflecken im Keil (x, y, r) – an der Anströmkante dichter
FLECKEN_KEIL = [(11.5, 10, 1.3), (13, 22, 1.6), (11, 31, 1.1), (14.5, 37, 1.8), (11.5, 46, 1.4), (13.5, 55, 1.2),
                (11, 64, 1.5), (14, 70, 1.0), (18, 18, 0.9), (19, 30, 1.2), (21, 41, 1.0), (18.5, 52, 1.1),
                (17, 62, 0.9), (24, 36, 0.8), (16, 45, 0.7), (16.5, 27, 0.8)]
FLECKEN_TASCHEN = [(10, 12, 1.2), (14, 20, 1.4), (18, 9, 1.0), (22, 28, 1.3), (26, 15, 1.1), (30, 24, 1.0),
                   (10, 50, 1.3), (14, 63, 1.1), (18, 55, 1.4), (22, 46, 1.0), (26, 68, 1.3), (30, 58, 1.0)]
# Staubteilchen: Start y, Größe, Verzögerung
STAUB = [(14, 1.4, 0.0), (28, 1.1, 0.5), (40, 1.6, 0.9), (52, 1.2, 0.3), (66, 1.4, 1.2), (34, 0.9, 1.6),
         (46, 1.0, 2.0), (22, 1.2, 2.3)]


def staub(ziel_x: float, farbe: str = "#6B573D") -> str:
    """Staub fliegt von links (Anströmseite) an die Filterfläche ziel_x und wird dort aufgefangen."""
    return "".join(
        f'<circle cx="2" cy="{y}" r="{r}" fill="{farbe}" opacity="0">'
        f'<animate attributeName="cx" values="-1;{ziel_x};{ziel_x}" keyTimes="0;0.6;1" dur="2.4s" begin="{b}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.75;1" dur="2.4s" begin="{b}s" repeatCount="indefinite"/>'
        '</circle>' for y, r, b in STAUB)


def flecken(punkte) -> str:
    return ('<g fill="#5E4B33"><animate attributeName="opacity" values="0.55;0.9;0.55" dur="2.4s" repeatCount="indefinite"/>'
            + "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>' for x, y, r in punkte) + '</g>')


def gelb_blinken(form: str) -> str:
    """Leichtes gelbes Blinken über der Filterfläche, 1 Hz wie bei Störung (diskret)."""
    return (f'<g fill="{GELB}" opacity="0"><animate attributeName="opacity" values="0.45;0" dur="1s" '
            f'calcMode="discrete" repeatCount="indefinite"/>{form}</g>')


def keil(verschmutzt: bool) -> str:
    """Einfacher Filter wie im bestehenden Anlagenbild."""
    fill = "url(#gS)" if verschmutzt else "url(#gK)"
    s = f'<path d="{KEIL}" fill="{fill}" stroke="{KEIL_K}" stroke-width="1.2" stroke-linejoin="round"/>'
    if verschmutzt:
        s += flecken(FLECKEN_KEIL) + gelb_blinken(f'<path d="{KEIL}"/>') + staub(10.5)
    return s


def taschen(verschmutzt: bool) -> str:
    """Taschenfilter von vorn: Rahmen, zwei Zellen übereinander, senkrechte Stege zwischen den Taschen."""
    s = [f'<rect x="6" y="4" width="28" height="72" rx="1" fill="#C8C8C8" stroke="{KEIL_K}" stroke-width="1"/>']
    fill = "#CDBB9C" if verschmutzt else "#FFFFFF"
    for y0 in (6, 41):
        s.append(f'<rect x="8" y="{y0}" width="24" height="33" fill="{fill}" stroke="{KEIL_K}" stroke-width="0.8"/>')
        s.extend(f'<rect x="{x - 0.6}" y="{y0}" width="1.2" height="33" fill="#9A9A9A"/>' for x in (12, 16, 20, 24, 28))
        s.append(f'<rect x="8" y="{y0}" width="24" height="33" fill="url(#gH)" opacity="0.18"/>')
    s.append(f'<rect x="6" y="38.5" width="28" height="3" fill="#A6A6A6" stroke="{KEIL_K}" stroke-width="0.8"/>')
    if verschmutzt:
        s.append(flecken(FLECKEN_TASCHEN))
        s.append(gelb_blinken('<rect x="8" y="6" width="24" height="33"/><rect x="8" y="41" width="24" height="33"/>'))
        s.append(staub(7))
    else:
        s.append(staub(7, "#7A7A7A"))   # sauber: graue Partikel in der Luft, werden aufgefangen
    return "".join(s)


def filter_inhalt(verschmutzt: bool, mit_taschen: bool) -> str:
    s = f'<rect x="1" y="1" width="38" height="78" fill="url(#gH)" stroke="{KONTUR}" stroke-width="1.2"/>'
    return s + (taschen(verschmutzt) if mit_taschen else keil(verschmutzt))


def svg(richtung: str, verschmutzt: bool, mit_taschen: bool = False) -> str:
    waagerecht = richtung in ("rechts", "links")
    w, h = (40, 80) if waagerecht else (80, 40)
    # Gezeichnet für „rechts“ (40 × 80); um die Mitte gedreht und ins Zielformat verschoben
    tf = f'translate({w / 2} {h / 2}) rotate({DREHUNG[richtung]}) translate(-20 -40)'
    titel = f'Luftfilter{", Taschenfilter" if mit_taschen else ""}, Strömung {richtung}{", verschmutzt" if verschmutzt else ""}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">\n'
            f'  <title>{titel}</title>\n  {DEFS}\n  <g transform="{tf}">{filter_inhalt(verschmutzt, mit_taschen)}</g>\n</svg>\n')


def main() -> None:
    ZIEL.mkdir(parents=True, exist_ok=True)
    for f in ZIEL.glob("Filter_*.svg"):
        f.unlink()
    for mit_taschen in (False, True):
        name = "Filter_Taschen" if mit_taschen else "Filter"
        for richtung in DREHUNG:
            for verschmutzt in (False, True):
                p = ZIEL / f"{name}_{richtung}{'_verschmutzt' if verschmutzt else ''}.svg"
                with open(p, "w", encoding="utf-8", newline="\n") as f:
                    f.write(svg(richtung, verschmutzt, mit_taschen))
                print(p.name)


if __name__ == "__main__":
    main()
