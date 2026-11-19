#!/usr/bin/env python3
"""Erzeugt symbole/lueftung/rauchmelder/Kanalrauchmelder_{lage}_{zustand}.svg.

Kanalrauchmelder: hellgraues, quadratisches Gehäuse (30 × 30) mit runder Messkammer in Zustandsfarbe (grauer, fester Ring wie bei
Pumpe und Ventilator), Messrohr mit Ansauglöchern ragt in den Kanal. Aufruf: python tools/kanalrauchmelder.py

Lage = Seite des Kanals, auf der das Gerät sitzt:
  oben, unten    48 × 50 für waagerechte Kanäle; Rohrende (Kanalmitte) unten bei y = 50 bzw. oben bei y = 0, x = 24
  links, rechts  52 × 48 für senkrechte Kanäle; Rohrende rechts bei x = 52 bzw. links bei x = 0, y = 24

Zustände (Farben aus zustandsfarben.py):
  _normal      grün, alles in Ordnung, statisch
  _luftstrom   grün, Luftstrom in Ordnung: weißer Ring dreht (wie Pumpe im Betrieb), helle Punkte steigen im Messrohr
               zum Gehäuse (Luft wird angesaugt)
  _wartung     gelb, Messkammer pulsiert weich (1,4 s) mit dunklem Warndreieck
  _alarm       rot, Messkammer pulsiert schnell (0,6 s), Rauch quillt in der Kammer auf, Alarmwellen blinken (2 Hz)
  _stoerung    rot wie alle Störungen, Messkammer pulsiert weich (1,4 s) mit rotem Warndreieck
Ohne Animation bleiben Zustandsfarbe, Warndreieck bzw. Rauch und Alarmwellen sichtbar.
"""
from pathlib import Path

from zustandsfarben import AUS, BETRIEB, FREIGABE, STOERUNG

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "lueftung" / "rauchmelder"
GRAU = AUS[2]
FARBEN = {"normal": BETRIEB, "luftstrom": BETRIEB, "wartung": FREIGABE, "alarm": STOERUNG, "stoerung": STOERUNG}
TITEL = {"normal": "Normal", "luftstrom": "Luftstrom in Ordnung", "wartung": "Wartung", "alarm": "Alarm", "stoerung": "Störung"}

# Geometrie je Lage: Größe, Gehäuse (x, y), Kammermitte, Messrohr (x, y, b, h), Kragen (x, y, b, h),
# Ansauglöcher, Luftweg der Punkte (Start, Ende) als (x, y)
LAGEN = {
    "oben":   dict(w=48, h=50, geh=(9, 2), k=(24, 17), rohr=(21, 30, 6, 20), kragen=(12, 30, 24, 3),
                   loecher=((24, 41), (24, 46)), weg=((24, 48), (24, 32))),
    "unten":  dict(w=48, h=50, geh=(9, 18), k=(24, 33), rohr=(21, 0, 6, 20), kragen=(12, 17, 24, 3),
                   loecher=((24, 4), (24, 9)), weg=((24, 2), (24, 18))),
    "links":  dict(w=52, h=48, geh=(5, 9), k=(20, 24), rohr=(33, 21, 19, 6), kragen=(33, 12, 3, 24),
                   loecher=((43, 24), (48, 24)), weg=((50, 24), (35, 24))),
    "rechts": dict(w=52, h=48, geh=(17, 9), k=(32, 24), rohr=(0, 21, 19, 6), kragen=(16, 12, 3, 24),
                   loecher=((4, 24), (9, 24)), weg=((2, 24), (17, 24))),
}
GB = GH = 30   # quadratisches Gehäuse
R = 11         # Kammerradius


def puls(dur: str, tief: float = 0.35) -> str:
    return (f'<animate attributeName="opacity" values="1;{tief};1" keyTimes="0;0.5;1" calcMode="spline" '
            f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="{dur}" repeatCount="indefinite"/>')


def blink(dur: str = "1s") -> str:
    return f'<animate attributeName="opacity" values="1;0.15" dur="{dur}" calcMode="discrete" repeatCount="indefinite"/>'


def svg(lage: str, zustand: str) -> str:
    g = LAGEN[lage]
    oben, unten, _ = FARBEN[zustand]
    cx, cy = g["k"]
    gx, gy = g["geh"]
    s = ['<defs><linearGradient id="gG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F0F1F2"/>'
         '<stop offset="1" stop-color="#D2D5D8"/></linearGradient>'
         f'<linearGradient id="gR" x1="0" y1="0" x2="{1 if lage in ("oben", "unten") else 0}" y2="{0 if lage in ("oben", "unten") else 1}">'
         '<stop offset="0" stop-color="#8C8C8C"/><stop offset="0.5" stop-color="#E0E0E0"/><stop offset="1" stop-color="#8C8C8C"/></linearGradient>'
         f'<linearGradient id="gK" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{oben}"/>'
         f'<stop offset="1" stop-color="{unten}"/></linearGradient></defs>']
    # Messrohr mit Ansauglöchern
    rx, ry, rb, rh = g["rohr"]
    s.append(f'<rect x="{rx}" y="{ry}" width="{rb}" height="{rh}" fill="url(#gR)" stroke="#6B6B6B" stroke-width="1"/>')
    s.append('<g fill="#4D4D4D">' + "".join(f'<circle cx="{x}" cy="{y}" r="1"/>' for x, y in g["loecher"]) + '</g>')
    if zustand == "luftstrom":
        (x0, y0), (x1, y1) = g["weg"]
        att, v0, v1 = ("cy", y0, y1) if x0 == x1 else ("cx", x0, x1)
        for b in ("0s", "0.4s", "0.8s"):
            s.append(f'<circle cx="{x0}" cy="{y0}" r="1.3" fill="#FFFFFF" opacity="0">'
                     f'<animate attributeName="{att}" values="{v0};{v1}" dur="1.2s" begin="{b}" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.8;1" dur="1.2s" begin="{b}" '
                     'repeatCount="indefinite"/></circle>')
    # Gehäuse und Kragen
    s.append(f'<rect x="{gx}" y="{gy}" width="{GB}" height="{GH}" rx="4" fill="url(#gG)" stroke="{GRAU}" stroke-width="1.4"/>')
    kx, ky, kb, kh = g["kragen"]
    s.append(f'<rect x="{kx}" y="{ky}" width="{kb}" height="{kh}" rx="1" fill="#B5B5B5" stroke="{GRAU}" stroke-width="0.8"/>')
    # Messkammer: Füllung in Zustandsfarbe (pulsiert ggf.), grauer Ring fest
    kammer = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#gK)"/>'
    if zustand == "alarm":
        s.append(f'<g>{puls("0.6s", 0.45)}{kammer}</g>')
    elif zustand in ("stoerung", "wartung"):
        s.append(f'<g>{puls("1.4s")}{kammer}</g>')
    else:
        s.append(kammer)
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{GRAU}" stroke-width="1.4"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="6.5" fill="none" stroke="#FFFFFF" stroke-opacity="0.75" stroke-width="1"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="2.4" fill="#FFFFFF" fill-opacity="0.85"/>')
    if zustand == "luftstrom":
        s.append(f'<circle cx="{cx}" cy="{cy}" r="9.2" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1.6" '
                 f'stroke-linecap="round" stroke-dasharray="12 7.3"><animateTransform attributeName="transform" type="rotate" '
                 f'from="0 {cx} {cy}" to="360 {cx} {cy}" dur="1.6s" repeatCount="indefinite"/></circle>')
    if zustand == "alarm":
        for i, b in enumerate(("0s", "0.5s", "1s")):   # Rauch quillt in der Kammer auf
            s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0.95;0" dur="1.5s" begin="{b}" repeatCount="indefinite"/>'
                     f'<animateTransform attributeName="transform" type="translate" values="0 4;0 -4" dur="1.5s" begin="{b}" repeatCount="indefinite"/>'
                     f'<path d="M{cx - 6 + i * 2},{cy + 2} a2.6,2.6 0 0 1 2,-4 a3.2,3.2 0 0 1 5.5,0.5 a2.4,2.4 0 0 1 1,4.2 h-7 '
                     'a2,2 0 0 1 -1.5,-0.7 z" fill="#5A5A5A" stroke="#3A3A3A" stroke-width="0.6"/></g>')
        # Alarmwellen links und rechts neben dem Gehäuse
        l, r_, m = gx - 1.5, gx + GB + 1.5, gy + GH / 2
        s.append(f'<g fill="none" stroke="{STOERUNG[1]}" stroke-width="1.6" stroke-linecap="round">{blink("0.5s")}'
                 f'<path d="M{l},{m - 7} q-2.5,7 0,14"/><path d="M{l - 2.5},{m - 10} q-3,10 0,20" stroke-opacity="0.6"/>'
                 f'<path d="M{r_},{m - 7} q2.5,7 0,14"/><path d="M{r_ + 2.5},{m - 10} q3,10 0,20" stroke-opacity="0.6"/></g>')
    if zustand in ("stoerung", "wartung"):
        dreieck = "#E2231A" if zustand == "stoerung" else "#4D4D4D"
        s.append(f'<g>{puls("1.4s")}<path d="M{cx},{cy - 7} L{cx + 7.5},{cy + 6} L{cx - 7.5},{cy + 6} Z" fill="{dreieck}" '
                 'stroke="#FFFFFF" stroke-width="1.4" stroke-linejoin="round"/>'
                 f'<rect x="{cx - 0.8}" y="{cy - 3.5}" width="1.6" height="5.5" rx="0.8" fill="#FFFFFF"/>'
                 f'<circle cx="{cx}" cy="{cy + 3.6}" r="0.9" fill="#FFFFFF"/></g>')
    w, h = g["w"], g["h"]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">\n'
            f'  <title>Kanalrauchmelder, Gerät {lage} am Kanal, {TITEL[zustand]}</title>\n  ' + "".join(s) + '\n</svg>\n')


def main() -> None:
    ZIEL.mkdir(parents=True, exist_ok=True)
    for lage in LAGEN:
        for zustand in FARBEN:
            p = ZIEL / f"Kanalrauchmelder_{lage}_{zustand}.svg"
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(svg(lage, zustand))
            print(p.name)


if __name__ == "__main__":
    main()
