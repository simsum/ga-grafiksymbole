#!/usr/bin/env python3
"""Erzeugt symbole/fun/hydraulik/erzeuger/Fun_Waermepumpe_Luft_Wasser_{rechts,links}_<zustand>_animiert.svg.

Fun-Variante der Luft/Wasser-Wärmepumpe (tools/waermepumpe.py): gleiche Größe (180 × 168) und Anschlusspunkte,
Gehäusekontur in Fun-Braun, der Lüfter wird zum Gesicht (Nabe = Nase). Gesichtszüge weiß mit brauner
Außenkontur, damit sie auf dem dunklen Lüfter lesbar sind. Animation per SMIL.

  _aus       Augen zu, schläft; „Zzz“ steigt auf
  _an        große Augen (blinzeln), Lächeln, Bäckchen; Lüfter dreht, Windlinien wie bei der normalen Wärmepumpe
  _stoerung  X-Augen, Zickzack-Mund; Gerät wackelt, Rauch steigt aus dem Lüfter,
             kleines Warndreieck im Schaltkasten, rote Status-LED blinkt
  _abtau     besorgte Augen, Zähneklappern; Gerät zittert, Eiszapfen an der Oberkante, Reif auf dem Lüfter,
             Schneeflocke im Schaltkasten, blaue Status-LED

Ohne Animation bleiben Gesicht, Zustandsanzeigen und Effekte (in Ausgangslage) sichtbar.
Aufruf: python tools/fun_waermepumpe.py
"""
import re
from pathlib import Path

import waermepumpe as wp

BRAUN = "#3B2412"
W = wp.W
FY = 79                    # Lüftermitte y
ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "fun" / "hydraulik" / "erzeuger"


def fun_kontur(svg: str) -> str:
    """Gehäusekonturen in Fun-Braun, etwas kräftiger."""
    for alt, neu in (('stroke="#999999" stroke-width="2"', f'stroke="{BRAUN}" stroke-width="2.6"'),
                     ('stroke="#999999" stroke-width="1.6"', f'stroke="{BRAUN}" stroke-width="2"'),
                     ('stroke="#999999" stroke-width="1.2"', f'stroke="{BRAUN}" stroke-width="1.6"'),
                     ('stroke="#2E3237"', f'stroke="{BRAUN}"'), ('stroke="#6B6B6B"', f'stroke="{BRAUN}"')):
        svg = svg.replace(alt, neu)
    return svg


def einsetzen(svg: str, danach: str, huelle: str = "") -> str:
    """danach: Ebenen über dem Gerät; huelle: Animation, die das ganze Gerät samt Ebenen bewegt."""
    kopf, rest = svg.split("</defs>", 1)
    rumpf = rest.rsplit("</svg>", 1)[0] + danach
    if huelle:
        rumpf = f"\n  <g>{huelle}{rumpf}</g>\n"
    return f"{kopf}</defs>{rumpf}</svg>\n"


# ---------- Gesicht ----------
def augen(cx: float, cy: float, abstand: float, art: str, r: float = 6) -> str:
    xs = (cx - abstand / 2, cx + abstand / 2)
    if art == "zu":
        return "".join(f'<path d="M{x - r},{cy} q{r},{r * 0.9} {2 * r},0" fill="none" stroke="{BRAUN}" stroke-width="2.2" stroke-linecap="round"/>' for x in xs)
    if art == "x":
        return "".join(f'<path d="M{x - r * .8},{cy - r * .8} l{r * 1.6},{r * 1.6} M{x + r * .8},{cy - r * .8} l{-r * 1.6},{r * 1.6}" '
                       f'stroke="{BRAUN}" stroke-width="2.2" stroke-linecap="round"/>' for x in xs)
    teile = []
    for x in xs:
        dy = 0.6 * r if art == "sorge" else 0
        teile.append(f'<ellipse cx="{x}" cy="{cy}" rx="{r}" ry="{r * 1.15:.1f}" fill="#FFFFFF" stroke="{BRAUN}" stroke-width="1.6"/>')
        teile.append(f'<circle cx="{x}" cy="{cy + dy:.1f}" r="{r * .5}" fill="#3B2413">'
                     f'<animate attributeName="r" values="{r * .5};{r * .5};0.4;{r * .5}" keyTimes="0;0.92;0.96;1" dur="4s" repeatCount="indefinite"/></circle>')
        if art == "sorge":
            neigung = r * .7 if x < cx else -r * .7
            teile.append(f'<path d="M{x - r},{cy - r * 1.7:.1f} l{2 * r},{neigung:.1f}" stroke="{BRAUN}" stroke-width="1.6" stroke-linecap="round"/>')
    return "".join(teile)


def mund(cx: float, cy: float, art: str, b: float = 16) -> str:
    if art == "laecheln":
        return (f'<path d="M{cx - b / 2},{cy} q{b / 2},{b * .6} {b},0" fill="#C8463C" stroke="{BRAUN}" stroke-width="1.8" stroke-linejoin="round"/>'
                f'<g fill="#F2A3A0" opacity=".8"><ellipse cx="{cx - b * .95}" cy="{cy - 1}" rx="2.6" ry="1.6"/>'
                f'<ellipse cx="{cx + b * .95}" cy="{cy - 1}" rx="2.6" ry="1.6"/></g>')
    if art == "schlaf":
        return f'<ellipse cx="{cx}" cy="{cy + 1}" rx="2" ry="1.4" fill="{BRAUN}"/>'
    if art == "zickzack":
        s = b / 4
        return (f'<path d="M{cx - b / 2},{cy} l{s},-2 l{s},4 l{s},-4 l{s},2" fill="none" stroke="{BRAUN}" stroke-width="1.8" '
                f'stroke-linejoin="round" stroke-linecap="round"/>')
    # klappern: Zähne, Fugen bleiben dunkel (#3B2413 wird von hell() nicht aufgehellt)
    return (f'<rect x="{cx - b / 2}" y="{cy - 2.5}" width="{b}" height="5" rx="1.5" fill="#FFFFFF" stroke="{BRAUN}" stroke-width="1.4"/>'
            f'<path d="M{cx - b / 4},{cy - 2.5} v5 M{cx},{cy - 2.5} v5 M{cx + b / 4},{cy - 2.5} v5 M{cx - b / 2},{cy} h{b}" stroke="#3B2413" stroke-width=".9"/>')


def hell(s: str) -> str:
    """Gesichtszüge auf dem dunklen Lüfter: braune, breitere Unterkontur, darüber dieselben Linien in Weiß."""
    breit = re.sub(r'stroke-width="([\d.]+)"', lambda m: f'stroke-width="{float(m.group(1)) + 2.4:.1f}"', s)
    weiss = s.replace(f'stroke="{BRAUN}"', 'stroke="#FFFFFF"').replace(f'rx="2" ry="1.4" fill="{BRAUN}"', 'rx="2" ry="1.4" fill="#FFFFFF"')
    return breit + weiss


# ---------- Effekte ----------
def zzz(x: float, y: float) -> str:
    teile = []
    for i, (g, b) in enumerate(((6, 0), (4.5, 1.2), (3.5, 2.4))):
        teile.append(f'<g transform="translate({x + i * 6} {y - i * 7})">'
                     f'<animateTransform attributeName="transform" type="translate" values="{x} {y};{x + 8} {y - 22}" dur="3.6s" begin="{b}s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="0;1;0" dur="3.6s" begin="{b}s" repeatCount="indefinite"/>'
                     f'<path d="M0,0 h{g} l-{g},{g} h{g}" fill="none" stroke="{BRAUN}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
                     f'<path d="M0,0 h{g} l-{g},{g} h{g}" fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></g>')
    return "".join(teile)


def rauch(x: float, y: float) -> str:
    teile = []
    for i, b in enumerate((0, 0.8, 1.6)):
        teile.append(f'<g transform="translate({x + i * 8 - 8} {y - i * 6})" opacity="{0.9 - i * 0.25:.2f}">'
                     f'<animateTransform attributeName="transform" type="translate" values="{x - 4} {y};{x + 6} {y - 26}" dur="2.4s" begin="{b}s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="0;.95;0" dur="2.4s" begin="{b}s" repeatCount="indefinite"/>'
                     f'<path d="M-6,0 a4,4 0 0 1 3,-6 a5,5 0 0 1 8,1 a4,4 0 0 1 1,7 h-10 a3,3 0 0 1 -2,-2 z" fill="#7A7A7A" stroke="{BRAUN}" stroke-width="1.4" stroke-linejoin="round"/></g>')
    return "".join(teile)


def eiszapfen() -> str:
    teile = ['<path d="M6,6 h168" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity=".9"/>']
    for x, laenge in ((16, 9), (30, 6), (52, 12), (78, 7), (98, 10), (122, 6), (150, 11), (166, 7)):
        teile.append(f'<path d="M{x - 3},8 L{x},{8 + laenge} L{x + 3},8 Z" fill="#DDF1FF" stroke="#5A9BD6" stroke-width="1" stroke-linejoin="round"/>')
    return "".join(teile)


def warndreieck(px: float) -> str:
    return (f'<path d="M{px},24 L{px + 12},46 L{px - 12},46 Z" fill="#D7302B" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>'
            f'<rect x="{px - 1.4}" y="30" width="2.8" height="9" rx="1.4" fill="#FFFFFF"/><circle cx="{px}" cy="42.4" r="1.6" fill="#FFFFFF"/>')


def schneeflocke(px: float) -> str:
    return (f'<g transform="translate({px} 37)" fill="none" stroke="#2F7FD0" stroke-width="2" stroke-linecap="round">'
            + "".join(f'<path d="M0,-11 V11 M-3,-10 L0,-7 L3,-10 M-3,10 L0,7 L3,10" transform="rotate({a})"/>' for a in (0, 60, 120)) + "</g>")


WACKELN = '<animateTransform attributeName="transform" type="rotate" values="0 90 156;-1.5 90 156;1.5 90 156;-1 90 156;0 90 156" dur="0.6s" repeatCount="indefinite"/>'
ZITTERN = '<animateTransform attributeName="transform" type="translate" values="0 0;-1 0;1 0;-1 0;0 0" dur="0.25s" repeatCount="indefinite"/>'


def svg(seite: str, zustand: str) -> str:
    rechts = seite == "rechts"
    fx = 68 if rechts else W - 68            # Lüftermitte
    px = 151 if rechts else W - 151          # Mitte Schaltkasten
    lx = 145 if rechts else W - 145 - 12     # Status-LED
    sx = 1 if rechts else -1                 # Richtung der Effekte (vom Lüfter weg Richtung Schaltkasten)

    basis = fun_kontur(wp.svg(seite, "an" if zustand == "an" else "aus"))
    basis = basis.replace("<title id=\"title\">Luft/Wasser", "<title id=\"title\">Fun: Luft/Wasser")
    gesicht = {"aus": augen(fx, FY - 14, 30, "zu") + mund(fx, FY + 18, "schlaf"),
               "an": augen(fx, FY - 14, 30, "auf") + mund(fx, FY + 16, "laecheln"),
               "stoerung": augen(fx, FY - 14, 30, "x") + mund(fx, FY + 18, "zickzack"),
               "abtau": augen(fx, FY - 14, 30, "sorge") + mund(fx, FY + 18, "klappern")}[zustand]
    led = {"stoerung": f'<rect x="{lx}" y="74" width="12" height="5" rx="1.5" fill="#E2231A">'
                       f'<animate attributeName="opacity" values="1;.2" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>',
           "abtau": f'<rect x="{lx}" y="74" width="12" height="5" rx="1.5" fill="#2F9BE8">'
                    f'<animate attributeName="opacity" values="1;.35;1" dur="2s" repeatCount="indefinite"/></rect>'}.get(zustand, "")
    vorn = {"aus": "", "an": "",
            "stoerung": warndreieck(px),
            "abtau": f'<circle cx="{fx}" cy="{FY}" r="49" fill="#CFE8FF" opacity=".35"/>' + schneeflocke(px)}[zustand]
    effekt = {"aus": zzz(fx + sx * 32 - (8 if not rechts else 0), FY - 31), "an": "",
              "stoerung": rauch(fx + sx * 32, FY - 27), "abtau": eiszapfen()}[zustand]
    huelle = {"stoerung": WACKELN, "abtau": ZITTERN}.get(zustand, "")
    return einsetzen(basis, "  " + led + vorn + hell(gesicht) + effekt + "\n", huelle)


def main() -> None:
    ZIEL.mkdir(parents=True, exist_ok=True)
    for seite in ("rechts", "links"):
        for zustand in ("aus", "an", "stoerung", "abtau"):
            p = ZIEL / f"Fun_Waermepumpe_Luft_Wasser_{seite}_{zustand}_animiert.svg"
            p.write_text(svg(seite, zustand), encoding="utf-8", newline="\n")
            print(p)


if __name__ == "__main__":
    main()
