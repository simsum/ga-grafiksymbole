#!/usr/bin/env python3
"""Erzeugt symbole/hydraulik/zaehler/<Zaehler>_{Messrad,Ultraschall}_{waagerecht,senkrecht}_{aus,an}.svg.

Zusätzliche Zählerdarstellungen neben den bestehenden Zählern mit Rollenzählwerk (die bleiben unverändert).
Gleiche Größe und Rohrachse wie diese: waagerecht 60 × 65, senkrecht 65 × 60, Rohrachse 15.
Unter (bzw. neben) dem Rohr eine runde Plakette mit dem Medium. Aufruf: python tools/zaehler_messrad_ultraschall.py

  Messrad      Gehäuse mit rundem Sichtfenster auf dem Rohr, darin ein Turbinenrad; _an: Rad dreht ruhig (3 s)
  Ultraschall  glattes Rohrstück mit zwei schrägen Schallköpfen, V-förmiger Schallweg über den Rohrboden;
               _an: Köpfe leuchten abwechselnd auf, Schallimpulse laufen den Weg entlang (1,6 s)
  _aus         steht, statisch

Medien: Waermemengenzaehler (rote Flamme), Kaeltemengenzaehler (blaue Schneeflocke), Wasserzaehler (blauer Tropfen),
Gaszaehler (gelbe Flamme, wie der Gasflansch).
"""
from pathlib import Path

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "hydraulik" / "zaehler"
GV = ('<defs><linearGradient id="gV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E6E6E6"/><stop offset="0.07" '
      'stop-color="#E0E0E0"/><stop offset="1" stop-color="#999999"/></linearGradient>'
      '<radialGradient id="gG" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#55606D"/>'
      '<stop offset="1" stop-color="#2B3440"/></radialGradient></defs>')

FLAMME = ('<path d="M0,-11 C5,-5 8,-1 7,4 C6,8.5 3,10.5 0,10.5 C-4.5,10.5 -7.5,7.5 -7.5,3 C-7.5,-1.5 -4,-3.5 -3,-8 C-1,-5 '
          '0,-3.5 1,-1.5 C2.2,-4.5 1.5,-8 0,-11 Z" fill="{a}"/><path d="M0,0 C2.5,2.5 3.5,4.5 3,6.5 C2.5,8.5 1,9.5 0,9.5 '
          'C-2,9.5 -3.5,8 -3.5,6 C-3.5,4 -1.5,2.5 0,0 Z" fill="{i}"/>')


def schneeflocke() -> str:
    arm = 'M0,-8 V8 M-2.8,-6.4 L0,-4.4 L2.8,-6.4 M-2.8,6.4 L0,4.4 L2.8,6.4'
    return ('<g fill="none" stroke="#2F7FD8" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
            + "".join(f'<path d="{arm}" transform="rotate({w})"/>' for w in (0, 60, 120)) + '</g>')


MEDIEN = {  # Dateiname, Titel, Piktogramm um (0, 0), Maßstab
    "waerme": ("Waermemengenzaehler", "Wärmemengenzähler", FLAMME.format(a="#E0302A", i="#FFB020"), 0.55),
    "kaelte": ("Kaeltemengenzaehler", "Kältemengenzähler", schneeflocke(), 0.85),
    "wasser": ("Wasserzaehler", "Wasserzähler",
               '<path d="M0,-9 C3.6,-3.6 6,-0.6 6,2.4 a6,6 0 0 1 -12,0 C-6,-0.6 -3.6,-3.6 0,-9 Z" fill="#4A86D4" '
               'stroke="#2E6BC2" stroke-width="1"/>', 0.9),
    "gas": ("Gaszaehler", "Gaszähler", FLAMME.format(a="#F2C230", i="#FFF1A8").replace(
        'fill="#F2C230"/>', 'fill="#F2C230" stroke="#A88400" stroke-width="1.2" stroke-linejoin="round"/>'), 0.55),
}


def messrad(an: bool) -> str:
    s = ['<rect x="19" y="4" width="22" height="22" rx="4" fill="url(#gV)" stroke="#999999" stroke-width="2"/>',
         '<circle cx="30" cy="15" r="8.5" fill="url(#gG)" stroke="#6B7480" stroke-width="1.4"/>']
    blatt = 'M30,15 C28.2,12.5 28.4,9.6 30,7.6 C31.6,9.6 31.8,12.5 30,15 Z'
    anim = ('<animateTransform attributeName="transform" type="rotate" from="0 30 15" to="360 30 15" dur="3s" '
            'repeatCount="indefinite"/>') if an else ""
    s.append('<g fill="#C9CED4" stroke="#8A94A0" stroke-width="0.5"><g>' + anim +
             "".join(f'<path d="{blatt}" transform="rotate({w} 30 15)"/>' for w in (0, 60, 120, 180, 240, 300)) + '</g></g>')
    s.append('<circle cx="30" cy="15" r="1.8" fill="#8A94A0" stroke="#55606D" stroke-width="0.6"/>')
    s.append('<path d="M24.5,11 a7,7 0 0 1 6,-3.8" fill="none" stroke="#FFFFFF" stroke-opacity="0.45" stroke-width="1.2" '
             'stroke-linecap="round"/>')
    return "".join(s)


def ultraschall(an: bool) -> str:
    weg = "M19,10 L30,20 L41,10"
    s = [f'<path d="{weg}" fill="none" stroke="#4A86D4" stroke-opacity="0.5" stroke-width="1.1" stroke-dasharray="1.5 1.5"/>']
    if an:
        for b in ("0s", "0.8s"):
            s.append(f'<path d="{weg}" fill="none" stroke="#2F7FD8" stroke-width="2.4" stroke-linecap="round" '
                     f'stroke-dasharray="5 40" stroke-dashoffset="5"><animate attributeName="stroke-dashoffset" values="5;-31" '
                     f'dur="1.6s" begin="{b}" repeatCount="indefinite"/></path>')
    for x, w, b in ((19, -40, "0s"), (41, 40, "0.8s")):
        s.append(f'<g transform="rotate({w} {x} 8)"><rect x="{x - 3.5}" y="1.5" width="7" height="8" rx="1.5" fill="#55606D" '
                 f'stroke="#2B3440" stroke-width="1"/><rect x="{x - 2.5}" y="8.5" width="5" height="2" fill="#8A94A0"/></g>')
        if an:
            s.append(f'<circle cx="{x}" cy="5.5" r="1.3" fill="#7CD0FF" opacity="0"><animate attributeName="opacity" '
                     f'values="0;1;0;0" keyTimes="0;0.1;0.3;1" dur="1.6s" begin="{b}" repeatCount="indefinite"/></circle>')
    return "".join(s)


def svg(medium: str, bauart: str, achse: str, an: bool) -> str:
    _, titel, piktogramm, massstab = MEDIEN[medium]
    # Rohr, Flansche, Messteil und Halter – gezeichnet waagerecht (Rohrachse y = 15)
    rohr = ('<rect x="4" y="9" width="52" height="12" fill="url(#gV)" stroke="#999999" stroke-width="2" stroke-linejoin="round"/>'
            '<rect x="1.5" y="3.5" width="4" height="23" rx="1" fill="url(#gV)" stroke="#999999" stroke-width="2"/>'
            '<rect x="54.5" y="3.5" width="4" height="23" rx="1" fill="url(#gV)" stroke="#999999" stroke-width="2"/>'
            '<rect x="29.4" y="21" width="1.2" height="12" fill="#808080" stroke="#808080" stroke-width="2"/>'
            + (messrad(an) if bauart == "Messrad" else ultraschall(an)))
    if achse == "waagerecht":
        w, h, px, py, teile = 60, 65, 30, 46, rohr
    else:   # an der Diagonalen gespiegelt: Rohrachse x = 15, Plakette rechts; Plakette bleibt aufrecht
        w, h, px, py, teile = 65, 60, 46, 30, f'<g transform="matrix(0 1 1 0 0 0)">{rohr}</g>'
    plakette = (f'<circle cx="{px}" cy="{py}" r="12" fill="#F2F2F2" stroke="#808080" stroke-width="2"/>'
                f'<g transform="translate({px} {py}) scale({massstab})">{piktogramm}</g>')
    zustand = "Durchfluss" if an else "steht"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">\n'
            f'  <title>{titel} ({bauart}), {achse}, {zustand}</title>\n  {GV}\n  {teile}{plakette}\n</svg>\n')


def main() -> None:
    for medium, (name, *_rest) in MEDIEN.items():
        for bauart in ("Messrad", "Ultraschall"):
            for achse in ("waagerecht", "senkrecht"):
                for an in (False, True):
                    p = ZIEL / f"{name}_{bauart}_{achse}_{'an' if an else 'aus'}.svg"
                    with open(p, "w", encoding="utf-8", newline="\n") as f:
                        f.write(svg(medium, bauart, achse, an))
                    print(p.name)


if __name__ == "__main__":
    main()
