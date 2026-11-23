#!/usr/bin/env python3
"""Erzeugt Fun-Symbole zu Datum, Uhrzeit und Sonnenstand unter symbole/fun/anzeigen/.

Gedacht für die Ausgänge des Niagara-Bausteins date-time-info (isDay, isCivilTwilight, isNight,
sunrise/sunset, isWeekend, isDaylightSaving, month). Stil wie die übrigen Fun-Anzeigen:
48 × 48, dunkelbraune Kontur #3B2412, Gesichter, animiert per SMIL, kein <text>, kein clipPath.

Tageszeit (Umschaltung über isDay / isCivilTwilight / isNight)
    Fun_Sonne_tag            Sonne lacht, Strahlen drehen langsam, zwinkert
    Fun_Sonne_daemmerung     Sonne guckt knapp über den Horizont, Strahlen glimmen
    Fun_Mond_nacht           Mondsichel schläft, schaukelt, Z steigen auf, Sterne funkeln
Sonnenereignisse (fest neben die Uhrzeiten sunrise / sunset)
    Fun_Sonnenaufgang        halbe Sonne am Horizont, Pfeil nach oben
    Fun_Sonnenuntergang      halbe Sonne, müde, Pfeil nach unten
Wochentag (isWeekend)
    Fun_Kalender_werktag     Kalenderblatt liest konzentriert, Stift tippt
    Fun_Kalender_wochenende  Kalenderblatt mit Sonnenbrille, hüpft, Konfetti
Zeitumstellung (isDaylightSaving)
    Fun_Wecker_sommerzeit    Wecker mit Sonnen-Plakette, klingelt leicht
    Fun_Wecker_winterzeit    Wecker mit Schneeflocken-Plakette, Schnee fällt
Jahreszeit (aus month, meteorologisch)
    Fun_Jahreszeit_{fruehling,sommer,herbst,winter}  Baum mit Gesicht
Kalenderwoche (calendarWeek, weekday)
    Fun_Wochenraupe_{1..7}   140 × 56, Raupe mit sieben Segmenten (Mo–So), heutiger Tag gelb und hüpft,
                             hält ein leeres Schild für die KW als Niagara-Label (x = 22 … 86, y = 4 … 24)
    Fun_Kalenderwoche_{gerade,ungerade}  Kalenderblatt mit zwei Figuren Hand in Hand bzw. einer, die winkt
Jahreslauf (month, daysRemainingInYear)
    Fun_Erdbahn_{1..12}      72 × 48, Erde mit Gesicht auf der Bahn um die Sonne, Position nach Monat
    Fun_Rakete_{ruhe,bald,start}  Silvester-Countdown: schläft, zappelt mit Funken, startet mit Feuerwerk

Alle Varianten einer Familie haben dieselbe Größe, feste Teile liegen an derselben Stelle.

Aufruf: python tools/fun_datum_zeit.py [Zielordner]
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
K = "#3B2412"                    # Kontur der Fun-Symbole
SW = 2.5                         # Hauptkontur
GELB, GELB_DUNKEL = "#FFD23F", "#FFB300"
ORANGE = "#FF8A3D"
ROT = "#E8442E"
BLAU = "#4AA8F0"
WANGE = "#F28B6E"


def n(x: float) -> str:
    return f"{x:.2f}".rstrip("0").rstrip(".")


def svg(kommentar: str, inhalt: str) -> str:
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">\n'
            f"  <!-- {kommentar} (SMIL) -->\n{inhalt}</svg>\n")


def wiederhole(attr: str, werte: str, dauer: str, begin: str = "", key: str = "") -> str:
    b = f' begin="{begin}"' if begin else ""
    k = f' keyTimes="{key}"' if key else ""
    return f'<animate attributeName="{attr}" values="{werte}"{k} dur="{dauer}"{b} repeatCount="indefinite"/>'


def bewege(typ: str, werte: str, dauer: str, begin: str = "", key: str = "") -> str:
    b = f' begin="{begin}"' if begin else ""
    k = f' keyTimes="{key}"' if key else ""
    return (f'<animateTransform attributeName="transform" type="{typ}" values="{werte}"{k} '
            f'dur="{dauer}"{b} repeatCount="indefinite"/>')


# --- Gesichtsteile -------------------------------------------------------------------------

def augen(x1, x2, y, r=1.6, zwinkern=False, dauer="4s"):
    """Runde Augen mit Glanzpunkt; optional zwinkern (ry kurz auf 0,2)."""
    out = ""
    for x in (x1, x2):
        anim = wiederhole("ry", f"{r};{r};0.2;{r}", dauer, key="0;0.9;0.95;1") if zwinkern else ""
        out += f'<ellipse cx="{n(x)}" cy="{n(y)}" rx="{r}" ry="{r}" fill="{K}">{anim}</ellipse>'
        out += f'<circle cx="{n(x + .5)}" cy="{n(y - .6)}" r=".5" fill="#FFFFFF"/>'
    return out


def augen_zu(x1, x2, y, b=2.2):
    """Geschlossene Augen als Bögen nach unten (schlafend/zufrieden)."""
    return "".join(f'<path d="M{n(x - b)},{n(y)} q{n(b)},{n(b * .9)} {n(2 * b)},0" fill="none" '
                   f'stroke="{K}" stroke-width="1.4" stroke-linecap="round"/>' for x in (x1, x2))


def augen_muede(x1, x2, y, b=2):
    """Halb geschlossene Augen: Lid als Strich, darunter halbe Pupille."""
    out = ""
    for x in (x1, x2):
        out += f'<path d="M{n(x - b)},{n(y)} a{n(b)},{n(b)} 0 0 0 {n(2 * b)},0 z" fill="{K}"/>'
        out += (f'<path d="M{n(x - b - .4)},{n(y)} h{n(2 * b + .8)}" stroke="{K}" stroke-width="1.4" '
                f'stroke-linecap="round"/>')
    return out


def mund(x, y, b=3.5, h=2.6):
    return (f'<path d="M{n(x - b)},{n(y)} q{n(b)},{n(h)} {n(2 * b)},0" fill="none" stroke="{K}" '
            f'stroke-width="1.6" stroke-linecap="round"/>')


def grinsen(x, y, b=4, h=4.5):
    """Offener, breiter Mund."""
    return (f'<path d="M{n(x - b)},{n(y)} q{n(b)},{n(h)} {n(2 * b)},0 z" fill="#B23A2A" stroke="{K}" '
            f'stroke-width="1.4" stroke-linejoin="round"/>')


def wangen(x1, x2, y):
    return "".join(f'<ellipse cx="{n(x)}" cy="{n(y)}" rx="2" ry="1.2" fill="{WANGE}" opacity="0.8"/>'
                   for x in (x1, x2))


def sonnenbrille(x, y):
    """Sonnenbrille wie beim Thermometer warm, Mitte x, Oberkante y."""
    return (f'<path d="M{n(x - 7)},{n(y)} h14 v3.2 q-2,2 -4.4,0 v-1 h-5.2 v1 q-2.4,2 -4.4,0 z" fill="{K}"/>'
            f'<path d="M{n(x - 5.6)},{n(y + .8)} l1.6,0" stroke="#FFFFFF" stroke-width=".8" stroke-linecap="round" opacity=".8"/>'
            f'<path d="M{n(x + 1.6)},{n(y + .8)} l1.6,0" stroke="#FFFFFF" stroke-width=".8" stroke-linecap="round" opacity=".8"/>')


def stern(x, y, r, farbe="#FFE08A", kontur=True, anim=""):
    """Vierzackiger Stern."""
    i = r * .35
    d = (f"M{n(x)},{n(y - r)} L{n(x + i)},{n(y - i)} L{n(x + r)},{n(y)} L{n(x + i)},{n(y + i)} "
         f"L{n(x)},{n(y + r)} L{n(x - i)},{n(y + i)} L{n(x - r)},{n(y)} L{n(x - i)},{n(y - i)} Z")
    s = f' stroke="{K}" stroke-width="1" stroke-linejoin="round"' if kontur else ""
    return f'<path d="{d}" fill="{farbe}"{s}>{anim}</path>'


def schneeflocke(x, y, r, farbe="#FFFFFF", kontur=K, sw=1.1):
    """Sechsstrahlige Schneeflocke als Linien (mit Kontur darunter, damit sie auf Weiß sichtbar ist)."""
    d = ""
    for i in range(3):
        a = math.radians(90 + 60 * i)
        dx, dy = r * math.cos(a), r * math.sin(a)
        d += f"M{n(x - dx)},{n(y - dy)} L{n(x + dx)},{n(y + dy)} "
    return (f'<path d="{d}" stroke="{kontur}" stroke-width="{n(sw + 1.4)}" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="{farbe}" stroke-width="{n(sw)}" stroke-linecap="round"/>')


def strahl(cx, cy, winkel, r1, r2, farbe=GELB_DUNKEL):
    """Strahl als Kapsel: braune Linie, darüber schmaler in Farbe."""
    a = math.radians(winkel)
    x1, y1 = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
    x2, y2 = cx + r2 * math.cos(a), cy + r2 * math.sin(a)
    d = f"M{n(x1)},{n(y1)} L{n(x2)},{n(y2)}"
    return (f'<path d="{d}" stroke="{K}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="{farbe}" stroke-width="2.2" stroke-linecap="round"/>')


# --- Tageszeit --------------------------------------------------------------------------------

def sonne_tag() -> str:
    strahlen = "".join(strahl(24, 24, w, 15, 20.5) for w in range(0, 360, 45))
    return svg("Sonne Tag: lacht, Strahlen drehen langsam, zwinkert", f"""\
  <g>{bewege("rotate", "0 24 24;360 24 24", "24s")}
   {strahlen}
  </g>
  <circle cx="24" cy="24" r="11.5" fill="{GELB}" stroke="{K}" stroke-width="{SW}"/>
  <path d="M16.5,21 q1.5,-5 6,-6.5" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" opacity="0.7"/>
  {augen(20, 28, 22.5, zwinkern=True)}
  {mund(24, 27)}
  {wangen(17.5, 30.5, 26.5)}
""")


HORIZONT_Y = 34


def horizont(spiegel_farbe: str) -> str:
    """Horizontlinie mit schimmernden Spiegelstreifen darunter."""
    y = HORIZONT_Y
    return (f'<path d="M4,{y} H44" stroke="{K}" stroke-width="{SW}" stroke-linecap="round"/>'
            f'<g stroke="{spiegel_farbe}" stroke-width="2" stroke-linecap="round">'
            f'<path d="M14,{y + 4.5} h20">{wiederhole("opacity", "1;0.35;1", "2.4s")}</path>'
            f'<path d="M18,{y + 9} h12">{wiederhole("opacity", "0.35;1;0.35", "2.4s")}</path></g>')


def sonne_daemmerung() -> str:
    # Sonne Mitte (24, 39), r = 12, sichtbar nur der Abschnitt über dem Horizont (7 px hoch)
    cx, cy, r = 24, 39, 12
    h = cy - HORIZONT_Y
    b = math.sqrt(r * r - h * h)
    kappe = f"M{n(cx - b)},{HORIZONT_Y} A{r},{r} 0 0 1 {n(cx + b)},{HORIZONT_Y} Z"
    strahlen = "".join(strahl(cx, cy, w, 15, 19, "#FFC46B") for w in (-150, -120, -90, -60, -30))
    return svg("Sonne Daemmerung: guckt ueber den Horizont, Strahlen glimmen, Sterne", f"""\
  <g opacity="0.5">{wiederhole("opacity", "0.25;0.75;0.25", "3s")}
   {strahlen}
  </g>
  <path d="{kappe}" fill="#FFA23A" stroke="{K}" stroke-width="{SW}" stroke-linejoin="round"/>
  {augen(20.5, 27.5, 30, r=1.4, zwinkern=True, dauer="3s")}
  {horizont("#FFA23A")}
  {stern(9, 9, 2.6, anim=wiederhole("opacity", "1;0.2;1", "1.8s"))}
  {stern(39, 6, 2, anim=wiederhole("opacity", "0.2;1;0.2", "1.8s"))}
""")


def mondsichel(cx1, cy1, r1, cx2, cy2, r2) -> str:
    """Sichel = Kreis 1 ohne Kreis 2 (als Pfad über die Schnittpunkte, ohne clipPath)."""
    dx, dy = cx2 - cx1, cy2 - cy1
    d = math.hypot(dx, dy)
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(r1 * r1 - a * a)
    mx, my = cx1 + a * dx / d, cy1 + a * dy / d
    p1 = (mx + h * dy / d, my - h * dx / d)
    p2 = (mx - h * dy / d, my + h * dx / d)
    # äußerer Bogen von p1 nach p2 (großer Bogen um Kreis 1), innerer zurück (kleiner Bogen um Kreis 2)
    return (f"M{n(p1[0])},{n(p1[1])} A{r1},{r1} 0 1 0 {n(p2[0])},{n(p2[1])} "
            f"A{r2},{r2} 0 0 1 {n(p1[0])},{n(p1[1])} Z")


def z_pfad(x, y, s):
    """Buchstabe Z als Linienzug (kein <text>)."""
    return f"M{n(x)},{n(y)} h{n(s)} l{n(-s)},{n(s)} h{n(s)}"


def mond_nacht() -> str:
    sichel = mondsichel(21, 26, 15, 30, 19, 12.5)
    zs = ""
    for i, (x, y, s) in enumerate(((33, 26, 4), (37, 19, 5))):
        anim = (bewege("translate", "0 0;3 -9", "3s", begin=f"{i * 1.5}s")
                + wiederhole("opacity", "0;1;1;0", "3s", begin=f"{i * 1.5}s", key="0;0.15;0.7;1"))
        zs += (f'<path d="{z_pfad(x, y, s)}" fill="none" stroke="{K}" stroke-width="1.6" stroke-linecap="round" '
               f'stroke-linejoin="round" opacity="0">{anim}</path>')
    return svg("Mond Nacht: Mondsichel schlaeft und schaukelt, Z steigen auf, Sterne funkeln", f"""\
  <g>{bewege("rotate", "-4 21 26;4 21 26;-4 21 26", "4s")}
   <path d="{sichel}" fill="#FFE08A" stroke="{K}" stroke-width="{SW}" stroke-linejoin="round"/>
   <path d="M10,22 q1,-6 6,-9" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
   <path d="M11.5,27 q1.8,1.8 3.6,0" fill="none" stroke="{K}" stroke-width="1.4" stroke-linecap="round"/>
   <path d="M13.5,33 q2.2,1.8 4.4,-0.5" fill="none" stroke="{K}" stroke-width="1.5" stroke-linecap="round"/>
   <ellipse cx="10.5" cy="31" rx="1.6" ry="1" fill="{WANGE}" opacity="0.8"/>
  </g>
  {zs}
  {stern(40, 37, 2.6, anim=wiederhole("opacity", "1;0.2;1", "1.6s"))}
  {stern(29, 7, 2, anim=wiederhole("opacity", "0.2;1;0.2", "1.6s"))}
  {stern(43, 9, 1.6, anim=wiederhole("opacity", "1;0.3;1", "2.2s"))}
""")


# --- Sonnenaufgang / -untergang -----------------------------------------------------------

def sonne_ereignis(auf: bool) -> str:
    cx, cy, r = 21, HORIZONT_Y, 12
    farbe = GELB if auf else ORANGE
    halb = f"M{cx - r},{cy} A{r},{r} 0 0 1 {cx + r},{cy} Z"
    strahlen = "".join(strahl(cx, cy, w, 15, 19, GELB_DUNKEL if auf else "#FF6A2A")
                       for w in (-160, -125, -90, -55, -20))
    if auf:
        gesicht = augen(17, 25, 27.5, zwinkern=True) + mund(21, 30.4, b=3, h=2.2)
        pfeil = f"M40,8 l-5.5,7 h3.5 v9 h4 v-9 h3.5 z"
        weg = "0 3;0 -2"
        kommentar = "Sonnenaufgang: halbe Sonne wach, Pfeil steigt"
    else:
        gesicht = augen_muede(17, 25, 27.5) + f'<ellipse cx="21" cy="31" rx="1.4" ry="1.2" fill="{K}"/>'
        pfeil = f"M40,24 l-5.5,-7 h3.5 v-9 h4 v9 h3.5 z"
        weg = "0 -3;0 2"
        kommentar = "Sonnenuntergang: halbe Sonne muede, Pfeil sinkt"
    return svg(kommentar, f"""\
  <g>{wiederhole("opacity", "0.55;1;0.55", "2.4s")}
   {strahlen}
  </g>
  <path d="{halb}" fill="{farbe}" stroke="{K}" stroke-width="{SW}" stroke-linejoin="round"/>
  {gesicht}
  {horizont(farbe)}
  <path d="{pfeil}" fill="{GELB_DUNKEL if auf else ORANGE}" stroke="{K}" stroke-width="1.8" stroke-linejoin="round">{bewege("translate", weg, "1.6s")}{wiederhole("opacity", "0;1;1;0", "1.6s", key="0;0.2;0.75;1")}</path>
""")


# --- Kalender -------------------------------------------------------------------------------

def kalenderblatt(kopf: str) -> str:
    return (f'<rect x="8" y="9" width="32" height="33" rx="4" fill="#FFFFFF" stroke="{K}" stroke-width="{SW}"/>'
            f'<path d="M8,18 V13 a4,4 0 0 1 4,-4 h24 a4,4 0 0 1 4,4 V18 Z" fill="{kopf}" stroke="{K}" '
            f'stroke-width="{SW}" stroke-linejoin="round"/>'
            f'<rect x="14.5" y="5" width="3.5" height="8" rx="1.75" fill="#FFFFFF" stroke="{K}" stroke-width="1.8"/>'
            f'<rect x="30" y="5" width="3.5" height="8" rx="1.75" fill="#FFFFFF" stroke="{K}" stroke-width="1.8"/>')


def kalender_werktag() -> str:
    # Pupillen wandern hin und her (liest), Stift rechts tippt
    pupillen = ""
    for x in (19, 29):
        pupillen += (f'<circle cx="{x}" cy="27" r="2.6" fill="#FFFFFF" stroke="{K}" stroke-width="1.2"/>'
                     f'<circle cx="{x - 1}" cy="27.5" r="1.3" fill="{K}">'
                     f'{wiederhole("cx", f"{x - 1};{x + 1};{x + 1};{x - 1};{x - 1}", "3s", key="0;0.4;0.5;0.9;1")}</circle>')
    return svg("Kalender Werktag: liest konzentriert, Stift tippt", f"""\
  {kalenderblatt("#4A86D4")}
  <path d="M15.5,22.5 l6,0.8 M32.5,22.5 l-6,0.8" stroke="{K}" stroke-width="1.5" stroke-linecap="round"/>
  {pupillen}
  <path d="M21,35 q3,1.2 6,0" fill="none" stroke="{K}" stroke-width="1.6" stroke-linecap="round"/>
  <g>{bewege("rotate", "0 39 44;-12 39 44;0 39 44;0 39 44", "1.2s", key="0;0.2;0.4;1")}
   <path d="M37.5,44 l-1,-13 a2.5,2.5 0 0 1 5,0 l-1,13 l-1.5,3 z" fill="#FFC41F" stroke="{K}" stroke-width="1.5" stroke-linejoin="round"/>
   <path d="M36.6,32.5 h4.8" stroke="{K}" stroke-width="1.2"/>
  </g>
""")


def kalender_wochenende() -> str:
    konfetti = ""
    for i, (x, farbe, dreh) in enumerate(((6, "#2ECC40", 200), (43, BLAU, -220), (24, "#FFC41F", 180))):
        start = -1 if i < 2 else -2
        konfetti += (f'<rect x="{x - 1.4}" y="{start}" width="2.8" height="1.8" rx=".4" fill="{farbe}" stroke="{K}" '
                     f'stroke-width=".7" opacity="0">'
                     f'{bewege("translate", "0 0;0 26", "2.4s", begin=f"{i * .8}s")}'
                     f'{wiederhole("opacity", "0;1;1;0", "2.4s", begin=f"{i * .8}s", key="0;0.1;0.75;1")}</rect>')
    return svg("Kalender Wochenende: Sonnenbrille, grinst, huepft, Konfetti", f"""\
  <g>{bewege("translate", "0 1;0 -1;0 1", "1s")}
   {kalenderblatt(ROT)}
   {sonnenbrille(24, 23.5)}
   {grinsen(24, 31.5)}
   {wangen(15.5, 32.5, 31)}
  </g>
  {konfetti}
""")


# --- Wecker ---------------------------------------------------------------------------------

def wecker(sommer: bool) -> str:
    glocke = "#FF8A3D" if sommer else "#7CB8F2"
    glocken = ""
    for cx, w in ((12.5, -40), (35.5, 40)):
        glocken += (f'<path d="M{cx - 6},{n(13.5)} a6,6 0 0 1 12,0 z" fill="{glocke}" stroke="{K}" '
                    f'stroke-width="2" stroke-linejoin="round" transform="rotate({w} {cx} 13.5)"/>')
    striche = ('<path d="M24,15 v2.6 M24,39 v-2.6 M12,27 h2.6 M36,27 h-2.6" stroke="#3B2412" '
               'stroke-width="1.6" stroke-linecap="round"/>')
    if sommer:
        strahlen = "".join(strahl(36, 36.5, w, 6.3, 8) for w in range(0, 360, 60))
        plakette = (f'<g>{bewege("rotate", "0 36 36.5;360 36 36.5", "10s")}{strahlen}</g>'
                    f'<circle cx="36" cy="36.5" r="4.8" fill="{GELB}" stroke="{K}" stroke-width="1.8"/>')
        gesicht = augen(19.5, 28.5, 23.5, zwinkern=True) + mund(24, 29.5, b=3.5, h=2.8)
        extra = ""
        kommentar = "Wecker Sommerzeit: Sonnen-Plakette, klingelt leicht"
    else:
        plakette = (f'<circle cx="36" cy="36.5" r="6.5" fill="#DDEEFF" stroke="{K}" stroke-width="1.8"/>'
                    + schneeflocke(36, 36.5, 4, farbe=BLAU, kontur="#FFFFFF", sw=1.2))
        gesicht = (augen(19.5, 28.5, 23.5, r=1.4)
                   + f'<path d="M20.5,30 l1,-1 l1,1 l1,-1 l1,1 l1,-1 l1,1" fill="none" stroke="{K}" '
                     f'stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/>')
        extra = ""
        for i, (x, y) in enumerate(((5, 22), (43, 18), (8, 38))):
            extra += (f'<g opacity="0">{bewege("translate", "0 -6;0 6", "2.4s", begin=f"{i * .8}s")}'
                      f'{wiederhole("opacity", "0;1;1;0", "2.4s", begin=f"{i * .8}s", key="0;0.15;0.75;1")}'
                      f'{schneeflocke(x, y, 2.2, sw=.9)}</g>')
        kommentar = "Wecker Winterzeit: Schneeflocken-Plakette, bibbert, Schnee faellt"
    wackeln = (bewege("rotate", "0 24 27;-5 24 27;5 24 27;-5 24 27;0 24 27;0 24 27", "2.5s",
                      key="0;0.05;0.1;0.15;0.2;1") if sommer
               else bewege("translate", "0 0;-0.6 0;0.6 0;-0.3 0;0 0", "0.35s"))
    return svg(kommentar, f"""\
  <g>{wackeln}
   {glocken}
   <path d="M16,38 l-3,5 M32,38 l3,5" stroke="{K}" stroke-width="{SW}" stroke-linecap="round"/>
   <circle cx="24" cy="27" r="14" fill="#FFFFFF" stroke="{K}" stroke-width="{SW}"/>
   <circle cx="24" cy="27" r="11" fill="none" stroke="{glocke}" stroke-width="1.4" opacity="0.6"/>
   {striche}
   {gesicht}
  </g>
  {plakette}
  {extra}
""")


# --- Jahreszeit -----------------------------------------------------------------------------

KRONE = ((24, 14, 9), (15, 21, 8), (33, 21, 8), (24, 24, 9))


def krone(farbe: str) -> str:
    """Wolkenförmige Baumkrone: erst alle Kreise dick in Kontur, darüber gefüllt (vereinigter Umriss)."""
    unten = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{K}" stroke="{K}" stroke-width="5"/>' for x, y, r in KRONE)
    oben = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{farbe}"/>' for x, y, r in KRONE)
    return unten + oben


def stamm() -> str:
    return (f'<path d="M20.5,44 L22,29 h4 L27.5,44 Z" fill="#9A6332" stroke="{K}" stroke-width="2" '
            f'stroke-linejoin="round"/>')


def boden(farbe: str) -> str:
    return f'<ellipse cx="24" cy="44" rx="17" ry="2.6" fill="{farbe}" stroke="{K}" stroke-width="1.6"/>'


def bluete(x, y, anim=""):
    blatt = "".join(f'<circle cx="{n(x + 1.6 * math.cos(math.radians(a)))}" cy="{n(y + 1.6 * math.sin(math.radians(a)))}" '
                    f'r="1.3" fill="#F7A1C4"/>' for a in range(-90, 270, 72))
    return f'<g>{anim}{blatt}<circle cx="{x}" cy="{y}" r=".9" fill="#FFD23F"/></g>'


def blatt_pfad(x, y):
    return f"M{n(x)},{n(y)} q3,-3 6,0 q-3,3 -6,0 z"


def jahreszeit(zeit: str) -> str:
    gesicht = augen(20, 28, 18, zwinkern=True) + mund(24, 22, b=3, h=2.4) + wangen(16.5, 31.5, 21.5)
    schwanken = bewege("rotate", "-2 24 44;2 24 44;-2 24 44", "3s")
    extra, deko, boden_farbe = "", "", "#8FD16A"
    if zeit == "fruehling":
        farbe = "#9EDB74"
        for i, (x, y) in enumerate(((13, 17), (33, 13), (36, 25), (12, 26), (25, 8))):
            pop = wiederhole("opacity", "0.4;1;0.4", "2s", begin=f"{i * .4}s")
            deko += bluete(x, y, pop)
        kommentar = "Jahreszeit Fruehling: Baum mit Blueten, schwankt"
    elif zeit == "sommer":
        farbe = "#4FB348"
        for x, y in ((14, 25), (34, 15), (32, 27), (16, 14)):
            deko += (f'<circle cx="{x}" cy="{y}" r="2.3" fill="{ROT}" stroke="{K}" stroke-width="1"/>'
                     f'<circle cx="{x - .7}" cy="{y - .7}" r=".6" fill="#FFFFFF" opacity=".8"/>')
        gesicht = sonnenbrille(24, 16) + mund(24, 22, b=3.2, h=2.6) + wangen(16.5, 31.5, 21.5)
        kommentar = "Jahreszeit Sommer: Baum mit Aepfeln und Sonnenbrille, schwankt"
    elif zeit == "herbst":
        farbe = "#F29A38"
        for x, y, r in ((14, 24, 3.2), (33, 14, 2.6), (31, 27, 2.4)):
            deko += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#E0662A" opacity=".8"/>'
        boden_farbe = "#C9A16B"
        for i, (x, y, f) in enumerate(((9, 28, "#E0662A"), (36, 30, "#FFC41F"), (30, 33, ROT))):
            b = f"{i * 1.1}s"
            extra += (f'<path d="{blatt_pfad(x, y)}" fill="{f}" stroke="{K}" stroke-width=".9" opacity="0">'
                      f'<animateTransform attributeName="transform" type="translate" values="0 0;3 5;-2 10;1 13" '
                      f'dur="3.3s" begin="{b}" repeatCount="indefinite"/>'
                      f'{wiederhole("opacity", "0;1;1;0", "3.3s", begin=b, key="0;0.1;0.8;1")}</path>')
        gesicht = augen(20, 28, 18, zwinkern=True) + mund(24, 22.5, b=2.4, h=1.4) + wangen(16.5, 31.5, 21.5)
        kommentar = "Jahreszeit Herbst: Baum verliert bunte Blaetter"
    else:
        farbe = "#E6F0FA"
        boden_farbe = "#FFFFFF"
        deko = (f'<path d="M8.5,21 q2,-3 5,-2 q2,-4 6,-4.5 q1.5,-6.5 9,-4.5 q4,-1 5,3.5 q4,0 5,4.5" fill="none" '
                f'stroke="#A9C8E8" stroke-width="1.6" stroke-linecap="round" opacity=".9"/>')
        gesicht = (augen(20, 28, 18, r=1.4)
                   + f'<path d="M20.5,23 l1,-1 l1,1 l1,-1 l1,1 l1,-1 l1,1" fill="none" stroke="{K}" '
                     f'stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/>'
                   + wangen(16.5, 31.5, 21.5))
        schwanken = bewege("translate", "0 0;-0.6 0;0.6 0;-0.3 0;0 0", "0.35s")
        for i, (x, y) in enumerate(((6, 6), (42, 4), (41, 30), (5, 32))):
            b = f"{i * .7}s"
            extra += (f'<g opacity="0">{bewege("translate", "0 0;0 10", "2.8s", begin=b)}'
                      f'{wiederhole("opacity", "0;1;1;0", "2.8s", begin=b, key="0;0.15;0.75;1")}'
                      f'{schneeflocke(x, y, 2.2, farbe="#FFFFFF", kontur="#7CA6DE", sw=.9)}</g>')
        kommentar = "Jahreszeit Winter: verschneiter Baum bibbert, Schnee faellt"
    return svg(kommentar, f"""\
  {boden(boden_farbe)}
  <g>{schwanken}
   {stamm()}
   {krone(farbe)}
   {deko}
   {gesicht}
  </g>
  {extra}
""")



# --- Kalenderwoche ----------------------------------------------------------------------------

def raupe(heute: int) -> str:
    """Wochenraupe 140 × 56, heute = 1 (Montag) … 7 (Sonntag)."""
    segmente = ""
    for i in range(7):
        cx = 12 + 14 * i
        farbe = "#FFC41F" if i + 1 == heute else ("#B7E58F" if i >= 5 else "#8FD16A")
        anim = bewege("translate", "0 0;0 -3.5;0 0", "0.9s") if i + 1 == heute else ""
        segmente += (f'<g>{anim}<path d="M{cx - 3},49 v3 M{cx + 3},49 v3" stroke="{K}" stroke-width="2" '
                     f'stroke-linecap="round"/><circle cx="{cx}" cy="42" r="8" fill="{farbe}" stroke="{K}" '
                     f'stroke-width="{SW}"/><circle cx="{cx - 2.5}" cy="39" r="1.6" fill="#FFFFFF" opacity=".6"/></g>')
    kopf = (f'<path d="M112,26 L107,14 M122,26 L128,13" stroke="{K}" stroke-width="2" stroke-linecap="round"/>'
            f'<circle cx="107" cy="14" r="2.4" fill="#FFC41F" stroke="{K}" stroke-width="1.6"/>'
            f'<circle cx="128" cy="13" r="2.4" fill="#FFC41F" stroke="{K}" stroke-width="1.6"/>'
            f'<circle cx="117" cy="36" r="12" fill="#9EDB74" stroke="{K}" stroke-width="{SW}"/>'
            + augen(113, 122, 33, zwinkern=True) + mund(117.5, 38.5, b=3.5, h=2.8) + wangen(109.5, 125.5, 38))
    schild = (f'<path d="M40,35 L42,24 M68,35 L66,24" stroke="{K}" stroke-width="2.2" stroke-linecap="round"/>'
              f'<rect x="22" y="4" width="64" height="20" rx="4" fill="#FFFBE6" stroke="{K}" stroke-width="{SW}"/>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="140" height="56" viewBox="0 0 140 56">
  <!-- Wochenraupe, Tag {heute} (1 = Montag) hervorgehoben, Schild fuer die KW (SMIL) -->
  <g>{bewege("rotate", "-1.5 54 40;1.5 54 40;-1.5 54 40", "3s")}
   {schild}
  </g>
  {segmente}
  <g>{bewege("rotate", "-3 117 46;3 117 46;-3 117 46", "2.4s")}
   {kopf}
  </g>
</svg>
"""


def mini_figur(x, y, r, farbe):
    return (f'<circle cx="{n(x)}" cy="{n(y)}" r="{r}" fill="{farbe}" stroke="{K}" stroke-width="1.8"/>'
            f'<circle cx="{n(x - r * .33)}" cy="{n(y - r * .2)}" r=".9" fill="{K}"/>'
            f'<circle cx="{n(x + r * .33)}" cy="{n(y - r * .2)}" r=".9" fill="{K}"/>'
            f'<path d="M{n(x - r * .35)},{n(y + r * .25)} q{n(r * .35)},{n(r * .35)} {n(r * .7)},0" fill="none" '
            f'stroke="{K}" stroke-width="1.1" stroke-linecap="round"/>')


def kalenderwoche(gerade: bool) -> str:
    if gerade:
        inhalt = (f'<g>{bewege("rotate", "-5 24 38;5 24 38;-5 24 38", "2s")}'
                  f'<path d="M21,32.5 q3,2.5 6,0" fill="none" stroke="{K}" stroke-width="1.8" stroke-linecap="round"/>'
                  + mini_figur(17.5, 29.5, 5.2, "#7FD9C8") + mini_figur(30.5, 29.5, 5.2, "#7FD9C8") + "</g>")
        return svg("Kalenderwoche gerade: zwei Figuren Hand in Hand, schaukeln",
                   f"  {kalenderblatt('#3DBFA8')}\n  {inhalt}\n")
    arm = (f'<g>{bewege("rotate", "-25 29 30;15 29 30;-25 29 30", "0.8s")}'
           f'<path d="M29,30 L34,24" stroke="{K}" stroke-width="1.8" stroke-linecap="round"/>'
           f'<circle cx="34" cy="24" r="1.4" fill="#C7AEEB" stroke="{K}" stroke-width="1.2"/></g>')
    inhalt = (f'<g>{bewege("translate", "0 0.8;0 -1.2;0 0.8", "0.8s")}{arm}'
              + mini_figur(24, 30, 6, "#C7AEEB") + "</g>")
    return svg("Kalenderwoche ungerade: eine Figur winkt und huepft",
               f"  {kalenderblatt('#9B6BD6')}\n  {inhalt}\n")


# --- Jahreslauf --------------------------------------------------------------------------------

def erdbahn(monat: int) -> str:
    """72 × 48, Erde nach Monat auf der Bahn (Januar unten, gegen den Uhrzeigersinn von Norden gesehen)."""
    cx, cy, rx, ry = 36, 24, 28, 16
    pos = []
    for m in range(1, 13):
        t = math.radians(90 - (m - 1) * 30)
        pos.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    ex, ey = pos[monat - 1]
    punkte = "".join(f'<circle cx="{n(x)}" cy="{n(y)}" r="1.2" fill="{K}" opacity=".45"/>'
                     for i, (x, y) in enumerate(pos) if i + 1 != monat)
    land = (f'<path d="M{n(ex - 3.6)},{n(ey - 1.2)} q1.2,-3 3.4,-2.6 q.6,1.6 -1,2.4 q-.6,1.6 -2.4,.2 z" fill="#6CC04A"/>'
            f'<path d="M{n(ex + 1.6)},{n(ey + 1.6)} q1.6,-.8 2.4,.6 q-1,1.6 -2.4,-.6 z" fill="#6CC04A"/>')
    erde = (f'<g>{bewege("translate", "0 -0.8;0 0.8;0 -0.8", "1.6s")}'
            f'<circle cx="{n(ex)}" cy="{n(ey)}" r="5.5" fill="{BLAU}" stroke="{K}" stroke-width="2"/>{land}'
            f'<circle cx="{n(ex - 1.7)}" cy="{n(ey - .2)}" r=".8" fill="{K}"/>'
            f'<circle cx="{n(ex + 1.7)}" cy="{n(ey - .2)}" r=".8" fill="{K}"/>'
            f'<path d="M{n(ex - 1.4)},{n(ey + 1.6)} q1.4,1.2 2.8,0" fill="none" stroke="{K}" stroke-width="1" '
            f'stroke-linecap="round"/></g>')
    strahlen = "".join(strahl(cx, cy, w, 9.5, 11.5) for w in range(0, 360, 45))
    sonne = (f'<g>{bewege("rotate", f"0 {cx} {cy};360 {cx} {cy}", "20s")}{strahlen}</g>'
             f'<circle cx="{cx}" cy="{cy}" r="7" fill="{GELB}" stroke="{K}" stroke-width="2.2"/>'
             f'<circle cx="33.5" cy="23" r="1.1" fill="{K}"/><circle cx="38.5" cy="23" r="1.1" fill="{K}"/>'
             f'<path d="M33.6,26 q2.4,2 4.8,0" fill="none" stroke="{K}" stroke-width="1.2" stroke-linecap="round"/>')
    hinten = ey < cy
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="72" height="48" viewBox="0 0 72 48">
  <!-- Erdbahn Monat {monat}: Erde mit Gesicht auf der Bahn um die Sonne (SMIL) -->
  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{K}" stroke-width="1.2" stroke-dasharray="2 3" opacity=".45"/>
  {punkte}
  {erde if hinten else ""}
  {sonne}
  {"" if hinten else erde}
</svg>
"""


def rakete(zustand: str) -> str:
    """Silvester-Countdown: ruhe (schläft), bald (zappelt, Lunte funkt), start (fliegt, Feuerwerk)."""
    koerper = (f'<path d="M24,37 V46" stroke="#9A6332" stroke-width="2" stroke-linecap="round"/>'
               f'<path d="M18,26 L12,34 V37 L18,34 Z M30,26 L36,34 V37 L30,34 Z" fill="{ROT}" stroke="{K}" '
               f'stroke-width="2" stroke-linejoin="round"/>'
               f'<rect x="20" y="33.5" width="8" height="3.5" rx="1" fill="#808080" stroke="{K}" stroke-width="1.8"/>'
               f'<path d="M24,6 C30,11 31,20 30,34 H18 C17,20 18,11 24,6 Z" fill="#F4F4F4" stroke="{K}" '
               f'stroke-width="{SW}" stroke-linejoin="round"/>'
               f'<path d="M24,6 C27.5,9 29,12 29.6,15 H18.4 C19,12 20.5,9 24,6 Z" fill="{ROT}" stroke="{K}" '
               f'stroke-width="2" stroke-linejoin="round"/>'
               f'<circle cx="24" cy="23" r="4.6" fill="#9FD0F5" stroke="{K}" stroke-width="2"/>')
    if zustand == "ruhe":
        gesicht = augen_zu(22.2, 25.8, 22.4, b=1.1) + f'<circle cx="24" cy="25.4" r=".7" fill="{K}"/>'
        lunte = f'<path d="M27,37 q2,2 1,4 q-1,2 1.5,3" fill="none" stroke="{K}" stroke-width="1.2" stroke-linecap="round"/>'
        return svg("Rakete Ruhe: schlaeft bis kurz vor Silvester",
                   f"  {lunte}\n  <g>{bewege('rotate', '-2 24 46;2 24 46;-2 24 46', '4s')}\n   {koerper}\n   {gesicht}\n  </g>\n")
    if zustand == "bald":
        gesicht = (f'<circle cx="22.4" cy="22.4" r="1.1" fill="{K}"/><circle cx="25.6" cy="22.4" r="1.1" fill="{K}"/>'
                   f'<circle cx="22.8" cy="22" r=".4" fill="#FFFFFF"/><circle cx="26" cy="22" r=".4" fill="#FFFFFF"/>'
                   f'<path d="M22.6,25 q1.4,1.4 2.8,0" fill="none" stroke="{K}" stroke-width="1" stroke-linecap="round"/>')
        lunte = f'<path d="M27,37 q2,2 1,4 q-1,2 1.5,3" fill="none" stroke="{K}" stroke-width="1.2" stroke-linecap="round"/>'
        funken = (stern(29.5, 44, 2.4, farbe="#FFC41F", anim=wiederhole("opacity", "1;0.1;1", "0.3s"))
                  + stern(32, 41.5, 1.6, farbe=ORANGE, anim=wiederhole("opacity", "0.1;1;0.1", "0.3s")))
        return svg("Rakete bald: zappelt vor Aufregung, Lunte funkt",
                   f"  {lunte}\n  {funken}\n  <g>{bewege('translate', '0 0;-0.6 0;0.6 0;-0.3 0;0 0', '0.3s')}\n"
                   f"   {koerper}\n   {gesicht}\n  </g>\n")
    gesicht = (f'<circle cx="22.4" cy="22" r="1.1" fill="{K}"/><circle cx="25.6" cy="22" r="1.1" fill="{K}"/>'
               f'<path d="M22.2,24.2 q1.8,2.6 3.6,0 z" fill="#B23A2A" stroke="{K}" stroke-width=".8" stroke-linejoin="round"/>')
    flamme = (f'<path d="M19.5,37 Q24,52 28.5,37 Z" fill="{ORANGE}" stroke="{K}" stroke-width="1.6" stroke-linejoin="round">'
              f'{wiederhole("d", "M19.5,37 Q24,52 28.5,37 Z;M19.5,37 Q24,47 28.5,37 Z;M19.5,37 Q24,52 28.5,37 Z", "0.25s")}</path>'
              f'<path d="M21.8,37 Q24,45 26.2,37 Z" fill="#FFD23F"/>')
    feuerwerk = ""
    for i, (fx, fy, farbe) in enumerate(((8, 9, "#FFC41F"), (40.5, 12, "#F7A1C4"))):
        b = f"{i * .8}s"
        strahlen = "".join(f'<circle cx="{n(4.5 * math.cos(math.radians(a)))}" cy="{n(4.5 * math.sin(math.radians(a)))}" '
                           f'r="1.1" fill="{farbe}" stroke="{K}" stroke-width=".6"/>' for a in range(0, 360, 45))
        feuerwerk += (f'<g transform="translate({fx} {fy})"><g opacity="0">'
                      f'{bewege("scale", "0.2;1.3;1.3", "1.6s", begin=b, key="0;0.6;1")}'
                      f'{wiederhole("opacity", "0;1;0", "1.6s", begin=b, key="0;0.3;1")}{strahlen}</g></g>')
    return svg("Rakete Start: Silvester, fliegt mit Flamme, Feuerwerk",
               f"  {feuerwerk}\n  <g>{bewege('translate', '0 1.5;0 -2;0 1.5', '0.8s')}\n"
               f"   {koerper}\n   {flamme}\n   {gesicht}\n  </g>\n")


SYMBOLE = {
    "Fun_Sonne_tag": sonne_tag,
    "Fun_Sonne_daemmerung": sonne_daemmerung,
    "Fun_Mond_nacht": mond_nacht,
    "Fun_Sonnenaufgang": lambda: sonne_ereignis(True),
    "Fun_Sonnenuntergang": lambda: sonne_ereignis(False),
    "Fun_Kalender_werktag": kalender_werktag,
    "Fun_Kalender_wochenende": kalender_wochenende,
    "Fun_Wecker_sommerzeit": lambda: wecker(True),
    "Fun_Wecker_winterzeit": lambda: wecker(False),
    **{f"Fun_Jahreszeit_{z}": (lambda z=z: jahreszeit(z)) for z in ("fruehling", "sommer", "herbst", "winter")},
    **{f"Fun_Wochenraupe_{t}": (lambda t=t: raupe(t)) for t in range(1, 8)},
    "Fun_Kalenderwoche_gerade": lambda: kalenderwoche(True),
    "Fun_Kalenderwoche_ungerade": lambda: kalenderwoche(False),
    **{f"Fun_Erdbahn_{m}": (lambda m=m: erdbahn(m)) for m in range(1, 13)},
    **{f"Fun_Rakete_{z}": (lambda z=z: rakete(z)) for z in ("ruhe", "bald", "start")},
}


def main() -> None:
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "symbole" / "fun" / "anzeigen"
    ziel.mkdir(parents=True, exist_ok=True)
    for name, fn in SYMBOLE.items():
        (ziel / f"{name}.svg").write_text(fn(), encoding="utf-8")
        print(f"{name}.svg")


if __name__ == "__main__":
    main()
