#!/usr/bin/env python3
"""Erzeugt symbole/lueftung/frostschutz/Frostschutzwaechter_{normal,frostgefahr}.svg.

Frostschutzwächter zum Überlegen auf ein Heizregister (40 × 80): 68 × 80, die linken 40 px decken das Register ab.
Rechts oben außerhalb des Registers sitzt eine eckige Plakette (24 × 24, Zustandsfarbe, fester grauer Rand,
weiße Schneeflocke); aus ihr läuft das Kupfer-Kapillarrohr in runden Bögen über das Register. Hintergrund
transparent. Im Px mit derselben linken oberen Ecke wie das Register einsetzen. Aufruf: python tools/frostschutz.py

  _normal       grün, statisch
  _frostgefahr  rot (Zustandsfarbe Störung), Plakette pulsiert schnell (0,6 s), Schneeflocke dreht sich,
                Kapillarrohr vereist und pulsiert, Eiskristalle blitzen auf (SMIL)
Beide Dateien gleich groß, alle Teile an derselben Stelle.
"""
from pathlib import Path

from zustandsfarben import AUS, BETRIEB, STOERUNG

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "lueftung" / "frostschutz"
GRAU = AUS[2]
KUPFER, KUPFER_DUNKEL, EIS = "#B8733A", "#6B4A2A", "#DDF1FF"
W, H = 68, 80
PX = 44   # Plakette links oben bei (44, 0)


def maeander() -> str:
    """Startet in der Plakette, läuft oben nach links ins Register, dann 7 Bahnen y = 6 … 78 mit Radius 6."""
    d = "M50,6"
    for i in range(7):
        links = i % 2 == 0
        d += f" H{3 if i == 6 else (9 if links else 31)}"
        if i < 6:
            d += f" a6,6 0 0 {0 if links else 1} 0,12"
    return d


def flocke(cx: float, cy: float, r: float, farbe: str, sw: float, anim: str = "") -> str:
    arme = "".join(f'<path d="M0,{-r} V{r} M{-r * 0.35:.2f},{-r * 0.8:.2f} L0,{-r * 0.55:.2f} L{r * 0.35:.2f},{-r * 0.8:.2f} '
                   f'M{-r * 0.35:.2f},{r * 0.8:.2f} L0,{r * 0.55:.2f} L{r * 0.35:.2f},{r * 0.8:.2f}" transform="rotate({a})"/>'
                   for a in (0, 60, 120))
    return (f'<g transform="translate({cx} {cy})"><g fill="none" stroke="{farbe}" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round">{anim}{arme}</g></g>')


def svg(zustand: str) -> str:
    frost = zustand == "frostgefahr"
    oben, unten, _ = STOERUNG if frost else BETRIEB
    d = maeander()
    s = [f'<defs><linearGradient id="gK" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{oben}"/>'
         f'<stop offset="1" stop-color="{unten}"/></linearGradient></defs>',
         # Kapillarrohr
         f'<path d="{d}" fill="none" stroke="{KUPFER_DUNKEL}" stroke-width="2.2" stroke-linecap="round" stroke-opacity="0.8"/>',
         f'<path d="{d}" fill="none" stroke="{KUPFER}" stroke-width="1.2" stroke-linecap="round"/>']
    if frost:
        s.append(f'<path d="{d}" fill="none" stroke="{EIS}" stroke-width="2.2" stroke-linecap="round">'
                 '<animate attributeName="opacity" values="0.95;0.35;0.95" dur="1.2s" repeatCount="indefinite"/></path>')
        for x, y, b in ((10, 18, "0s"), (30, 30, "0.4s"), (16, 42, "0.8s"), (26, 54, "1.2s"), (12, 66, "0.6s")):
            s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.2;0.8;1" dur="1.8s" '
                     f'begin="{b}" repeatCount="indefinite"/>{flocke(x, y, 3.2, "#FFFFFF", 1.6)}{flocke(x, y, 3.2, "#2F7FD8", 0.8)}</g>')
    # Plakette: nur die Füllung pulsiert, der graue Rand bleibt fest
    feld = f'<rect x="{PX + 1.5}" y="1.5" width="21" height="21" rx="4" fill="url(#gK)"/>'
    if frost:
        s.append('<g><animate attributeName="opacity" values="1;0.45;1" keyTimes="0;0.5;1" calcMode="spline" '
                 f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="0.6s" repeatCount="indefinite"/>{feld}</g>')
    else:
        s.append(feld)
    s.append(f'<rect x="{PX + 1.5}" y="1.5" width="21" height="21" rx="4" fill="none" stroke="{GRAU}" stroke-width="1.2"/>')
    dreh = ('<animateTransform attributeName="transform" type="rotate" from="0" to="60" dur="1.5s" repeatCount="indefinite"/>'
            if frost else "")
    s.append(flocke(PX + 12, 12, 6.5, "#FFFFFF", 1.5, dreh))
    titel = "Frostgefahr" if frost else "Normal"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">\n'
            f'  <title>Frostschutzwächter mit Kapillarrohr, {titel}</title>\n  ' + "".join(s) + '\n</svg>\n')


def main() -> None:
    ZIEL.mkdir(parents=True, exist_ok=True)
    for zustand in ("normal", "frostgefahr"):
        p = ZIEL / f"Frostschutzwaechter_{zustand}.svg"
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg(zustand))
        print(p.name)


if __name__ == "__main__":
    main()
