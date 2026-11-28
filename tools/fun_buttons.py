#!/usr/bin/env python3
"""Erzeugt weitere Fun-Buttons unter symbole/fun/navigation/: Waerme, Strom, Ereignisse,
Beleuchtung, Beleuchtung_Schuko, Schuko.

Gleicher Aufbau wie die vorhandenen Fun-Buttons (280 × 72): `normal` gelb, `aktiv` orange mit hellem
Rand und 3 px nach unten versetzt. Links ein Icon im hellen Kreis, rechts die Beschriftung in der
Schrift Chewy (Google Fonts, Apache License 2.0) als Pfad, helle Füllung mit brauner Kontur.

Schriftgröße und Lage sind von den vorhandenen Buttons übernommen (ausgemessen an Heizung, PV,
Übersicht): 38 px, Textmitte x = 164, Grundlinie y = 43,3 (aktiv 46,3). Zu lange Texte werden auf
die nutzbare Breite verkleinert (wie bei Wärmepumpe).

Ist die Beschriftung ein Tupel aus zwei Zeilen, wird sie zweizeilig gesetzt: 25 px, Grundlinien
11,5 px über und 12 px unter der einzeiligen Grundlinie (wie bei Beleuchtung + Schuko, das einzeilig
auf rund 22 px schrumpfen würde).

Die Schriftdatei wird nicht eingecheckt. Ohne --schrift wird Chewy-Regular.ttf einmalig von
github.com/google/fonts nach tools/.schriften/ geladen.

Benötigt fonttools (pip install fonttools).
Aufruf: python tools/fun_buttons.py [--schrift Pfad/zu/Chewy-Regular.ttf]
"""
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

from monatsleiste import schrift_laden, zahl

ROOT = Path(__file__).resolve().parent.parent
ZIEL = ROOT / "symbole" / "fun" / "navigation"

BRAUN = "#2b1600"
SCHRIFT_HELL = "#fffbe6"
GROESSE = 38.0               # px, wie Heizung/PV/Übersicht
TEXT_MITTE = 164.0
TEXT_BREITE_MAX = 187.0      # wie Wärmepumpe (x 70,6 … 257,4)
GRUNDLINIE = 43.3
GROESSE_ZWEIZEILIG = 25.0
ZEILEN_DY = (-11.5, 12.0)    # Grundlinien der beiden Zeilen relativ zu GRUNDLINIE
ICON_Y = 36.0
VERSATZ_AKTIV = 3.0

ZUSTAENDE = {
    "normal": dict(verlauf=("#fff59a", "#ffd23a", "#f29a00"), schatten_y=11, knopf_y=4, rand=""),
    "aktiv": dict(verlauf=("#ffb347", "#ff8a00", "#e05a00"), schatten_y=8, knopf_y=7,
                  rand='<rect x="1.5" y="4.5" width="277" height="60" rx="28" fill="none" stroke="#fff59a" stroke-width="3" opacity=".9"/>'),
}

KREIS = f'<circle r="21" fill="#fff8d6" stroke="{BRAUN}" stroke-width="3.5"/>'

# Thermometer mit roter Säule und zwei Wärmewellen
ICON_WAERME = (
    f'<path d="M-3,6 V-12 a3,3 0 0 1 6,0 V6 a6.5,6.5 0 1 1 -6,0Z" fill="#ffffff" stroke="{BRAUN}" stroke-width="3" stroke-linejoin="round"/>\n'
    '   <rect x="-1.4" y="-6" width="2.8" height="14" fill="#e8401c"/><circle cy="11" r="4.3" fill="#e8401c"/>\n'
    '   <g stroke="#ff6a00" stroke-width="2.2" fill="none" stroke-linecap="round"><path d="M8,-10 q2.5,2 0,4 q-2.5,2 0,4"/><path d="M12.5,-7 q2.5,2 0,4 q-2.5,2 0,4"/></g>'
)

# Blitz mit Gesicht (wie Sonne bei PV und Flamme bei Heizung)
ICON_STROM = (
    '<path d="M3,-17 L-10,2 H-1 L-4,17 L10,-3 H1 Z" fill="#ffd23a" stroke="#c26a00" stroke-width="3" stroke-linejoin="round"/>\n'
    f'   <circle cx="-2" cy="-1" r="1.3" fill="{BRAUN}"/><circle cx="3" cy="-1" r="1.3" fill="{BRAUN}"/>\n'
    f'   <path d="M-2,2.5 Q0.5,4.5 3,2.5" fill="none" stroke="{BRAUN}" stroke-width="1.3" stroke-linecap="round"/>'
)

# Logbuch: Klemmbrett mit drei Einträgen (grün, rot, orange)
ICON_EREIGNISSE = (
    f'<rect x="-11" y="-13" width="22" height="27" rx="2.5" fill="#ffffff" stroke="{BRAUN}" stroke-width="3.2"/>\n'
    f'   <rect x="-5" y="-16" width="10" height="6" rx="2" fill="#ffb347" stroke="{BRAUN}" stroke-width="2.4"/>\n'
    f'   <g stroke="{BRAUN}" stroke-width="2.4" stroke-linecap="round">'
    '<line x1="-2" y1="-3" x2="7" y2="-3"/><line x1="-2" y1="3" x2="7" y2="3"/><line x1="-2" y1="9" x2="5" y2="9"/></g>\n'
    '   <circle cx="-6" cy="-3" r="1.8" fill="#3aa84a"/><circle cx="-6" cy="3" r="1.8" fill="#e8401c"/><circle cx="-6" cy="9" r="1.8" fill="#ffb347"/>'
)

# Glühbirne mit Gesicht, Glanzlicht, vier Lichtstrahlen und grauem Sockel
ICON_BELEUCHTUNG = (
    '<g stroke="#ff9a1a" stroke-width="2.4" stroke-linecap="round">'
    '<line x1="-12.5" y1="-14.5" x2="-14.8" y2="-16.8"/><line x1="12.5" y1="-14.5" x2="14.8" y2="-16.8"/>'
    '<line x1="-15.5" y1="-5" x2="-18.3" y2="-5"/><line x1="15.5" y1="-5" x2="18.3" y2="-5"/></g>\n'
    '   <path d="M-4.5,7 C-4.5,2.5 -10,0 -10,-6 A10,10 0 1 1 10,-6 C10,0 4.5,2.5 4.5,7 Z" fill="#ffe14d" stroke="#c26a00" stroke-width="3" stroke-linejoin="round"/>\n'
    '   <path d="M-6.5,-9.5 A6.5,6.5 0 0 1 -2.5,-12.8" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" opacity=".85"/>\n'
    f'   <rect x="-5.5" y="7" width="11" height="7" rx="1.6" fill="#c9c2b4" stroke="{BRAUN}" stroke-width="2.4"/>\n'
    f'   <line x1="-5" y1="10.5" x2="5" y2="10.5" stroke="{BRAUN}" stroke-width="1.6"/>\n'
    f'   <path d="M-2.8,14 h5.6 l-1.2,2.6 h-3.2 Z" fill="{BRAUN}" stroke="{BRAUN}" stroke-width="1.4" stroke-linejoin="round"/>\n'
    f'   <circle cx="-3" cy="-5" r="1.3" fill="{BRAUN}"/><circle cx="3" cy="-5" r="1.3" fill="{BRAUN}"/>\n'
    f'   <path d="M-2.5,-1.5 Q0,0.8 2.5,-1.5" fill="none" stroke="{BRAUN}" stroke-width="1.3" stroke-linecap="round"/>'
)

# Schuko-Steckdose: Steckerlöcher als Augen, darunter ein Lächeln, oben/unten Erdungsbügel
ICON_SCHUKO = (
    f'<circle r="15" fill="#ffffff" stroke="{BRAUN}" stroke-width="3"/>\n'
    f'   <circle r="10.5" fill="#e9e3d6" stroke="{BRAUN}" stroke-width="2"/>\n'
    f'   <rect x="-3.5" y="-12.6" width="7" height="3.2" rx="1" fill="#c9c2b4" stroke="{BRAUN}" stroke-width="1.6"/>'
    f'<rect x="-3.5" y="9.4" width="7" height="3.2" rx="1" fill="#c9c2b4" stroke="{BRAUN}" stroke-width="1.6"/>\n'
    f'   <circle cx="-4.6" cy="-1.5" r="2.3" fill="{BRAUN}"/><circle cx="4.6" cy="-1.5" r="2.3" fill="{BRAUN}"/>\n'
    f'   <path d="M-3,3.2 Q0,5.8 3,3.2" fill="none" stroke="{BRAUN}" stroke-width="1.5" stroke-linecap="round"/>'
)

# Glühbirne und Steckdose verkleinert und versetzt nebeneinander
ICON_BELEUCHTUNG_SCHUKO = (
    f'<g transform="translate(-6.5,-2) scale(.68)">{ICON_BELEUCHTUNG.replace(chr(10) + "   ", "")}</g>\n'
    f'   <g transform="translate(8,6.5) scale(.56)">{ICON_SCHUKO.replace(chr(10) + "   ", "")}</g>'
)

BUTTONS = [
    ("Waerme", "Wärme", ICON_WAERME),
    ("Strom", "Strom", ICON_STROM),
    ("Ereignisse", "Ereignisse", ICON_EREIGNISSE),
    ("Beleuchtung", "Beleuchtung", ICON_BELEUCHTUNG),
    ("Beleuchtung_Schuko", ("Beleuchtung", "+ Schuko"), ICON_BELEUCHTUNG_SCHUKO),
    ("Schuko", "Schuko", ICON_SCHUKO),
]


def text_pfad(font: TTFont, text: str | tuple[str, str]) -> str:
    """Text als Pfad, Ursprung = Textmitte auf der Grundlinie. Ein Tupel wird zweizeilig gesetzt."""
    if isinstance(text, tuple):
        return "".join(zeile_pfad(font, z, GROESSE_ZWEIZEILIG, dy) for z, dy in zip(text, ZEILEN_DY))
    return zeile_pfad(font, text, GROESSE, 0.0)


def zeile_pfad(font: TTFont, text: str, groesse: float, dy: float) -> str:
    """Eine Zeile als Pfad, horizontal zentriert, Grundlinie bei y = dy."""
    upm = font["head"].unitsPerEm
    gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
    breite = sum(hmtx[cmap[ord(c)]][0] for c in text)
    s = min(groesse / upm, TEXT_BREITE_MAX / breite)
    pen = SVGPathPen(gs, zahl)
    x = -breite * s / 2
    for c in text:
        g = cmap[ord(c)]
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, dy)))
        x += hmtx[g][0] * s
    return pen.getCommands()


def svg(zustand: str, icon: str, d: str) -> str:
    z = ZUSTAENDE[zustand]
    dy = VERSATZ_AKTIV if zustand == "aktiv" else 0.0
    v0, v1, v2 = z["verlauf"]
    rand = f'\n  {z["rand"]}' if z["rand"] else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 72" width="280" height="72">
  <defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{v0}"/><stop offset=".5" stop-color="{v1}"/><stop offset="1" stop-color="{v2}"/></linearGradient></defs>
  <rect x="6" y="{z["schatten_y"]}" width="270" height="60" rx="26" fill="#1a0d00" opacity=".45"/>
  <rect x="4" y="{z["knopf_y"]}" width="270" height="60" rx="26" fill="url(#bg)" stroke="{BRAUN}" stroke-width="5"/>
  <path d="M30,{8 + z["knopf_y"]} H244" stroke="#ffffff" stroke-width="5" stroke-linecap="round" opacity=".55"/>{rand}
  <g transform="translate(40,{zahl(ICON_Y + dy)})">{KREIS}
   {icon}</g>
  <g transform="translate({zahl(TEXT_MITTE)},{zahl(GRUNDLINIE + dy)})">
    <path d="{d}" fill="none" stroke="{BRAUN}" stroke-width="5" stroke-linejoin="round"/>
    <path d="{d}" fill="{SCHRIFT_HELL}"/></g>
</svg>
'''


def main() -> int:
    args = sys.argv[1:]
    schrift = Path(args[1]) if args[:1] == ["--schrift"] else None
    font = schrift_laden(schrift)
    for name, text, icon in BUTTONS:
        d = text_pfad(font, text)
        for zustand in ZUSTAENDE:
            ziel = ZIEL / f"Fun_Button_{name}_{zustand}.svg"
            ziel.write_text(svg(zustand, icon, d), encoding="utf-8", newline="\n")
            print(ziel.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
