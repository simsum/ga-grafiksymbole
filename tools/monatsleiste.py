#!/usr/bin/env python3
"""Erzeugt symbole/fun/navigation/Fun_Monatsleiste.svg: Monatsleiste im Stil der Fun-Buttons.

1200 × 64, zwölf gleich breite Monatsfelder in Jahreszeitenfarben, Glanzstreifen, Schatten,
abgerundete Enden. Die Monatsnamen stehen wie die Beschriftung der Fun-Buttons in der Schrift
Chewy (Google Fonts, Apache License 2.0): helle Füllung mit brauner Kontur, als Pfade (kein <text>).

Die Schriftdatei wird nicht eingecheckt. Ohne --schrift wird Chewy-Regular.ttf einmalig von
github.com/google/fonts nach tools/.schriften/ geladen.

Benötigt fonttools (pip install fonttools).
Aufruf: python tools/monatsleiste.py [--schrift Pfad/zu/Chewy-Regular.ttf] [Zieldatei]
"""
import sys
import urllib.request
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
ZIEL = ROOT / "symbole" / "fun" / "navigation" / "Fun_Monatsleiste.svg"
SCHRIFT_URL = "https://github.com/google/fonts/raw/main/apache/chewy/Chewy-Regular.ttf"
SCHRIFT_CACHE = Path(__file__).resolve().parent / ".schriften" / "Chewy-Regular.ttf"

MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August",
          "September", "Oktober", "November", "Dezember"]
FARBEN = ["#5C5CA8", "#5D66CC", "#6E74C8", "#4FAE62", "#68B67C", "#7ABE8A",
          "#B5875C", "#B08E94", "#A3A3AB", "#8150A0", "#A458C0", "#A879C0"]
BRAUN = "#2b1600"
SCHRIFT_HELL = "#fffbe6"     # wie die Beschriftung der Fun-Buttons
KONTUR = 4                   # Strichstärke der Schriftkontur (Buttons: 5 bei größerer Schrift)
GRUNDLINIE = 39
MAX_GROESSE = 24
PLATZ_MITTE, PLATZ_RAND = 82.0, 72.0   # nutzbare Breite je Feld (Randfelder wegen der Rundung schmaler)
SEG_B = 1188 / 12


def zahl(x: float) -> str:
    return f"{x:.2f}".rstrip("0").rstrip(".")


def schattieren(farbe: str, f: float) -> str:
    """f > 0 hellt Richtung Weiß auf, f < 0 dunkelt ab (wie bisher in monatsleiste.ps1)."""
    n = int(farbe[1:], 16)
    rgb = ((n >> 16) & 255, (n >> 8) & 255, n & 255)
    neu = [round(x + (255 - x) * f) if f > 0 else round(x * (1 + f)) for x in rgb]
    return "#{:02X}{:02X}{:02X}".format(*neu)


def schrift_laden(pfad: Path | None) -> TTFont:
    if pfad is None:
        pfad = SCHRIFT_CACHE
        if not pfad.exists():
            pfad.parent.mkdir(parents=True, exist_ok=True)
            print(f"Lade {SCHRIFT_URL} ...")
            urllib.request.urlretrieve(SCHRIFT_URL, pfad)
    return TTFont(pfad)


def monatsnamen(font: TTFont) -> str:
    """Alle Monatsnamen als ein Pfad; einheitliche Größe, so dass der längste Name in sein Feld passt."""
    upm = font["head"].unitsPerEm
    gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
    breite = lambda t: sum(hmtx[cmap[ord(c)]][0] for c in t)
    groesse = min([MAX_GROESSE] + [(PLATZ_RAND if i in (0, 11) else PLATZ_MITTE) / breite(m) * upm
                                   for i, m in enumerate(MONATE)])
    s = groesse / upm
    pen = SVGPathPen(gs, zahl)
    for i, m in enumerate(MONATE):
        mitte = 4 + i * SEG_B + SEG_B / 2 + (4 if i == 0 else -4 if i == 11 else 0)
        x = mitte - breite(m) * s / 2
        for c in m:
            g = cmap[ord(c)]
            gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, GRUNDLINIE)))
            x += hmtx[g][0] * s
    return pen.getCommands()


def svg(font: TTFont) -> str:
    defs = segs = trenner = ""
    for i, farbe in enumerate(FARBEN):
        defs += (f'<linearGradient id="m{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{schattieren(farbe, 0.45)}"/>'
                 f'<stop offset=".5" stop-color="{farbe}"/><stop offset="1" stop-color="{schattieren(farbe, -0.3)}"/></linearGradient>\n    ')
        x = zahl(4 + i * SEG_B)
        segs += f'<rect x="{x}" y="4" width="{zahl(SEG_B + 0.5)}" height="52" fill="url(#m{i})"/>\n    '
        if i > 0:
            if i % 3 == 0:
                trenner += f'<line x1="{x}" y1="4" x2="{x}" y2="56" stroke="{BRAUN}" stroke-width="4"/>\n    '
            else:
                trenner += f'<line x1="{x}" y1="4" x2="{x}" y2="56" stroke="{BRAUN}" stroke-width="1.5" opacity=".55"/>\n    '
    d = monatsnamen(font)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 64" width="1200" height="64">
  <!-- Monatsleiste im Fun-Button-Stil, Schrift Chewy (Apache License 2.0) als Pfade, hell mit brauner Kontur -->
  <defs>
    {defs}<clipPath id="kapsel"><rect x="4" y="4" width="1188" height="52" rx="20"/></clipPath>
  </defs>
  <rect x="6" y="9" width="1188" height="52" rx="20" fill="#1a0d00" opacity=".45"/>
  <g clip-path="url(#kapsel)">
    {segs}{trenner}</g>
  <path d="M28,11 H1172" stroke="#ffffff" stroke-width="4" stroke-linecap="round" opacity=".45"/>
  <path d="{d}" fill="none" stroke="{BRAUN}" stroke-width="{KONTUR}" stroke-linejoin="round"/>
  <path d="{d}" fill="{SCHRIFT_HELL}"/>
  <rect x="4" y="4" width="1188" height="52" rx="20" fill="none" stroke="{BRAUN}" stroke-width="5"/>
</svg>
'''


def main() -> int:
    args = sys.argv[1:]
    schrift = None
    if args[:1] == ["--schrift"]:
        schrift, args = Path(args[1]), args[2:]
    ziel = Path(args[0]) if args else ZIEL
    ziel.write_text(svg(schrift_laden(schrift)), encoding="utf-8", newline="\n")
    print(ziel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
