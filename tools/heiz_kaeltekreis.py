#!/usr/bin/env python3
"""Erzeugt symbole/hydraulik/kreise/{Heizkreis,Kaeltekreis}_{plastisch,flach}_{aus,an_punkte,an_verlauf,an_beides}.svg.

Ringsymbol für einen Heiz- bzw. Kältekreis, 70 × 70, Mitte transparent, graue Konturen innen und außen.
Ringfarben aus den Rohr-/Flanschfarben: Heizkreis Vorlauf rot #F04F46 (links) → Rücklauf blau #4A86D4 (rechts),
Kältekreis Kälte-Vorlauf #2E6BC2 (links) → Kälte-Rücklauf #7CA6DE (rechts). Die Rohre gehören nicht zum Symbol;
sie setzen links und rechts auf halber Höhe (y = 35) am Ring an. Aufruf: python tools/heiz_kaeltekreis.py

Stil:   plastisch  heller Rohrprofil-Streifen in der Ringmitte und Lichtschimmer
        flach      nur Farbverlauf und Konturen
Zustand: _aus         nicht aktiv, statisch
         _an_punkte   drei helle Punkte kreisen ruhig im Ring (18 s)
         _an_verlauf  der Farbverlauf dreht sich langsam um den Ring (24 s; animiert gradientTransform)
         _an_beides   Punkte und Farbverlauf zusammen
Alle Varianten gleich groß, alles an derselben Stelle.
"""
from pathlib import Path

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "hydraulik" / "kreise"
C, R, B = 35, 30, 8          # Mitte, Radius der Ringmitte, Ringbreite
KONTUR = "#808080"
KREISE = {
    "Heizkreis": [("0", "#F04F46"), ("0.5", "#B97AB4"), ("1", "#4A86D4")],
    "Kaeltekreis": [("0", "#2E6BC2"), ("0.5", "#5589D0"), ("1", "#7CA6DE")],
}
ZUSTAENDE = {"aus": "", "an_punkte": "P", "an_verlauf": "V", "an_beides": "PV"}
TITEL = {"aus": "nicht aktiv", "an_punkte": "aktiv (Punkte kreisen)", "an_verlauf": "aktiv (Farbverlauf dreht)",
         "an_beides": "aktiv (Punkte und Farbverlauf)"}


def svg(name: str, stil: str, zustand: str) -> str:
    anim = ZUSTAENDE[zustand]
    stops = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in KREISE[name])
    dreh = (f'<animateTransform attributeName="gradientTransform" type="rotate" from="0 {C} {C}" to="360 {C} {C}" '
            'dur="24s" repeatCount="indefinite"/>') if "V" in anim else ""
    s = [f'<defs><linearGradient id="gR" gradientUnits="userSpaceOnUse" x1="{C - R - B}" y1="{C}" x2="{C + R + B}" y2="{C}">'
         f'{stops}{dreh}</linearGradient>'
         '<radialGradient id="gI" cx="0.5" cy="0.5" r="0.5"><stop offset="0.75" stop-color="#FFFFFF" stop-opacity="0"/>'
         '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0.45"/></radialGradient></defs>',
         f'<circle cx="{C}" cy="{C}" r="{R}" fill="none" stroke="url(#gR)" stroke-width="{B}"/>']
    if stil == "plastisch":
        s.append(f'<circle cx="{C}" cy="{C}" r="{R}" fill="none" stroke="#FFFFFF" stroke-opacity="0.3" stroke-width="{B * 0.55:.1f}"/>')
        s.append(f'<circle cx="{C}" cy="{C}" r="{R}" fill="none" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="{B * 0.22:.1f}"/>')
        s.append(f'<circle cx="{C}" cy="{C}" r="{R + B / 2 - 0.5}" fill="url(#gI)" opacity="0.6"/>')
    s.append(f'<circle cx="{C}" cy="{C}" r="{R + B / 2}" fill="none" stroke="{KONTUR}" stroke-width="1.4"/>')
    s.append(f'<circle cx="{C}" cy="{C}" r="{R - B / 2}" fill="none" stroke="{KONTUR}" stroke-width="1.4"/>')
    if "P" in anim:
        s.append(f'<g><animateTransform attributeName="transform" type="rotate" from="0 {C} {C}" to="360 {C} {C}" dur="18s" '
                 'repeatCount="indefinite"/>' + "".join(
                     f'<circle cx="{C}" cy="{C - R}" r="1.6" fill="#FFFFFF" fill-opacity="0.9" transform="rotate({w} {C} {C})"/>'
                     for w in (0, 120, 240)) + '</g>')
    titel = "Heizkreis" if name == "Heizkreis" else "Kältekreis"
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="70" height="70" viewBox="0 0 70 70" role="img">\n'
            f'  <title>{titel}, {stil}, {TITEL[zustand]}</title>\n  ' + "".join(s) + '\n</svg>\n')


def main() -> None:
    ZIEL.mkdir(parents=True, exist_ok=True)
    for name in KREISE:
        for stil in ("plastisch", "flach"):
            for zustand in ZUSTAENDE:
                p = ZIEL / f"{name}_{stil}_{zustand}.svg"
                with open(p, "w", encoding="utf-8", newline="\n") as f:
                    f.write(svg(name, stil, zustand))
                print(p.name)


if __name__ == "__main__":
    main()
