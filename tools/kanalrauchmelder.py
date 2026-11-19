#!/usr/bin/env python3
"""Erzeugt symbole/lueftung/rauchmelder/Kanalrauchmelder_{lage}_{zustand}.svg.

Kanalrauchmelder kompakt, passend zum Frostschutzwächter: eckige Plakette 24 × 24 in Zustandsfarbe mit festem
grauem Rand, darin „RM“ (als Pfad, dunkelgrau); ein schlankes Messrohr führt zur Kanalmitte.
Aufruf: python tools/kanalrauchmelder.py

Alle Dateien 40 × 40, für jede Lage und jeden Zustand gleich; Plakette und Rohr liegen je Lage immer an
derselben Stelle (kein Springen beim Umschalten).
Lage = Seite des Kanals, auf der das Gerät sitzt; Rohrende auf der Kanalmitte:
  oben    Plakette (8, 0),  Rohrende x = 20, y = 40     unten   Plakette (8, 16), Rohrende x = 20, y = 0
  links   Plakette (0, 8),  Rohrende x = 40, y = 20     rechts  Plakette (16, 8), Rohrende x = 0,  y = 20

Zustände (Farben aus zustandsfarben.py):
  _normal      hellgrau, „RM“, statisch
  _luftstrom   grün, „RM“, helle Punkte steigen im Messrohr zur Plakette (Luft wird angesaugt)
  _wartung     gelb, Füllung pulsiert weich (1,4 s), dunkles Warndreieck
  _alarm       rot, Füllung pulsiert schnell (0,6 s); statt „RM“ quellen graue Rauchballen auf,
               Alarmwellen neben der Plakette blinken (2 Hz)
  _stoerung    rot, Füllung pulsiert weich (1,4 s), rotes Warndreieck
"""
from pathlib import Path

from zustandsfarben import AUS, BETRIEB, FREIGABE, STOERUNG

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "lueftung" / "rauchmelder"
GRAU = AUS[2]
W = H = 40
FARBEN = {"normal": AUS, "luftstrom": BETRIEB, "wartung": FREIGABE, "alarm": STOERUNG, "stoerung": STOERUNG}
TITEL = {"normal": "Normal", "luftstrom": "Luftstrom in Ordnung", "wartung": "Wartung", "alarm": "Alarm", "stoerung": "Störung"}
# Plakette (x, y) links oben, Messrohr (x, y, b, h), Luftweg der Punkte (Start, Ende)
LAGEN = {"oben": ((8, 0), (18.5, 23, 3, 17), ((20, 39), (20, 25))),
         "unten": ((8, 16), (18.5, 0, 3, 17), ((20, 1), (20, 15))),
         "links": ((0, 8), (23, 18.5, 17, 3), ((39, 20), (25, 20))),
         "rechts": ((16, 8), (0, 18.5, 17, 3), ((1, 20), (15, 20)))}
# „RM“ als Strichpfad (kein <text>), im 24er-Feld gezeichnet
RM = "M5.5,17 V7 H9 a2.6,2.6 0 0 1 0,5.2 H5.5 M8.6,12.2 L11.2,17 M13,17 V7 L16.25,12.6 L19.5,7 V17"


def puls(dur: str, tief: float = 0.4) -> str:
    return (f'<animate attributeName="opacity" values="1;{tief};1" keyTimes="0;0.5;1" calcMode="spline" '
            f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="{dur}" repeatCount="indefinite"/>')


def blink(dur: str) -> str:
    return f'<animate attributeName="opacity" values="1;0.15" dur="{dur}" calcMode="discrete" repeatCount="indefinite"/>'


def rm(px: float, py: float) -> str:
    return (f'<path d="{RM}" transform="translate({px} {py}) translate(12.5 12) scale(0.7) translate(-12.5 -12)" '
            'fill="none" stroke="#4D4D4D" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')


def rauch(px: float, py: float) -> str:
    """Alarm: graue Rauchballen quellen unten auf, wachsen, steigen nach rechts oben und verblassen."""
    s = ""
    for b in ("0s", "0.4s", "0.8s"):
        s += (f'<circle cx="{px + 10}" cy="{py + 13}" r="2.6" fill="#5A5A5A" stroke="#FFFFFF" stroke-width="1" opacity="0.85">'
              f'<animate attributeName="cx" values="{px + 8};{px + 15}" dur="1.2s" begin="{b}" repeatCount="indefinite"/>'
              f'<animate attributeName="cy" values="{py + 18};{py + 6}" dur="1.2s" begin="{b}" repeatCount="indefinite"/>'
              f'<animate attributeName="r" values="1.6;4" dur="1.2s" begin="{b}" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.7;1" dur="1.2s" begin="{b}" '
              'repeatCount="indefinite"/></circle>')
    return s


def svg(lage: str, zustand: str) -> str:
    (px, py), (rx, ry, rb, rh), ((x0, y0), (x1, y1)) = LAGEN[lage]
    oben, unten, _ = FARBEN[zustand]
    s = [f'<defs><linearGradient id="gK" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{oben}"/>'
         f'<stop offset="1" stop-color="{unten}"/></linearGradient></defs>',
         f'<rect x="{rx}" y="{ry}" width="{rb}" height="{rh}" fill="#B5B5B5" stroke="{GRAU}" stroke-width="0.8"/>']
    if zustand == "luftstrom":
        att, v0, v1 = ("cy", y0, y1) if x0 == x1 else ("cx", x0, x1)
        for b in ("0s", "0.4s", "0.8s"):
            s.append(f'<circle cx="{x0}" cy="{y0}" r="1.1" fill="#FFFFFF" opacity="0"><animate attributeName="{att}" '
                     f'values="{v0};{v1}" dur="1.2s" begin="{b}" repeatCount="indefinite"/><animate attributeName="opacity" '
                     f'values="0;1;1;0" keyTimes="0;0.15;0.8;1" dur="1.2s" begin="{b}" repeatCount="indefinite"/></circle>')
    # Plakette: nur die Füllung pulsiert, der graue Rand bleibt fest
    feld = f'<rect x="{px + 1.5}" y="{py + 1.5}" width="21" height="21" rx="4" fill="url(#gK)"/>'
    dauer = {"alarm": "0.6s", "wartung": "1.4s", "stoerung": "1.4s"}.get(zustand)
    s.append(f'<g>{puls(dauer)}{feld}</g>' if dauer else feld)
    s.append(f'<rect x="{px + 1.5}" y="{py + 1.5}" width="21" height="21" rx="4" fill="none" stroke="{GRAU}" stroke-width="1.2"/>')
    cx, cy = px + 12, py + 12
    if zustand in ("wartung", "stoerung"):
        f = "#4D4D4D" if zustand == "wartung" else "#E2231A"
        s.append(f'<g>{puls("1.4s")}<path d="M{cx},{cy - 7.5} L{cx + 8},{cy + 6} L{cx - 8},{cy + 6} Z" fill="{f}" '
                 'stroke="#FFFFFF" stroke-width="1.4" stroke-linejoin="round"/>'
                 f'<rect x="{cx - 0.8}" y="{cy - 3.8}" width="1.6" height="5.6" rx="0.8" fill="#FFFFFF"/>'
                 f'<circle cx="{cx}" cy="{cy + 3.6}" r="0.9" fill="#FFFFFF"/></g>')
    elif zustand == "alarm":
        s.append(rauch(px, py))
        l, r_ = px - 1.5, px + 25.5
        s.append(f'<g fill="none" stroke="{STOERUNG[1]}" stroke-width="1.4" stroke-linecap="round">{blink("0.5s")}'
                 f'<path d="M{l},{cy - 5} q-2,5 0,10"/><path d="M{l - 2.5},{cy - 7.5} q-2.5,7.5 0,15" stroke-opacity="0.6"/>'
                 f'<path d="M{r_},{cy - 5} q2,5 0,10"/><path d="M{r_ + 2.5},{cy - 7.5} q2.5,7.5 0,15" stroke-opacity="0.6"/></g>')
    else:
        s.append(rm(px, py))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">\n'
            f'  <title>Kanalrauchmelder, Gerät {lage} am Kanal, {TITEL[zustand]}</title>\n  ' + "".join(s) + '\n</svg>\n')


def main() -> None:
    ZIEL.mkdir(parents=True, exist_ok=True)
    for f in ZIEL.glob("Kanalrauchmelder_*.svg"):
        f.unlink()
    for lage in LAGEN:
        for zustand in FARBEN:
            p = ZIEL / f"Kanalrauchmelder_{lage}_{zustand}.svg"
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(svg(lage, zustand))
            print(p.name)


if __name__ == "__main__":
    main()
