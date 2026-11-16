"""Erzeugt symbole/hydraulik/Brenner_Flamme_{links,rechts}_{1..5}.svg: animierte Brennerflamme ohne Kessel.

Die Flamme wird in Px über Kessel_Brenner_links/rechts gelegt (transparenter Hintergrund). Fünf Längen für
Leistungsstufen. Alle zehn Symbole haben dieselbe Größe (die der längsten Flamme) und dieselbe Wurzelposition,
damit Niagara beim Umschalten nichts verschiebt. Aufbau aus fünf Schichten (rot, orange, gelb, hell, blauer Ansatz), deren Umriss
und Schwerpunkt per SMIL (animate d) unregelmäßig flackern. Keine Filter, nur Verläufe und Deckkraft.

  Brenner_Flamme_links_N    Flamme zeigt nach rechts (Brenner links vom Kessel)
  Brenner_Flamme_rechts_N   Flamme zeigt nach links (Brenner rechts vom Kessel)

Position über dem Kessel (Koordinaten der Kessel-SVGs, Brenner links): Flammenwurzel an der Kesseltür bei
x = 82, Brennermitte y = 113 − 27 = 86 im Bild. Das Symbol hat links einen Rand von RAND px.
Zusätzlich je Flamme eine statische Variante `…_statisch` (SVG + PNG, ohne Animation, gleiche Größe) als
Ausweichlösung, z. B. für Darstellungen ohne SMIL.
Aufruf: python tools/flamme.py [Zielordner]
"""
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAENGEN = {1: 26, 2: 46, 3: 66, 4: 86, 5: 106}   # px ab Kesseltür
HOEHEN = {1: 9, 2: 11, 3: 13, 4: 15, 5: 17}      # halbe Flammenhöhe an der Wurzel
RAND = 4
PUNKTE = 36
PHASEN = (0.0, 0.27, 0.55, 0.8, 0.0)             # Flackerphasen eines Zyklus (letzte = erste)


def umriss(L: float, h: float, amp: float, phase: float, zungen: float) -> str:
    """Flammenumriss als Polygon: Breite nimmt zur Spitze ab, die Mittellinie schwingt zur Spitze hin stärker."""
    oben, unten = [], []
    for i in range(PUNKTE + 1):
        t = i / PUNKTE
        breite = h * (1 - t) ** 0.8 * (1 + 0.28 * math.sin(math.pi * t) + 0.08 * math.sin(2 * math.pi * (zungen * t + phase)))
        mitte = amp * t ** 1.3 * math.sin(2 * math.pi * (1.1 * t - phase))
        oben.append((t * L, mitte - breite))
        unten.append((t * L, mitte + breite))
    pts = oben + unten[::-1]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def schicht(L, h, amp, farbe, deckkraft, dauer, zungen, versatz=0.0) -> str:
    werte = ";".join(umriss(L, h, amp, p + versatz, zungen) for p in PHASEN)
    return (f'<path d="{umriss(L, h, amp, versatz, zungen)}" fill="{farbe}" opacity="{deckkraft}">'
            f'<animate attributeName="d" values="{werte}" dur="{dauer}s" repeatCount="indefinite"/></path>')


def statisch(text: str) -> str:
    """Entfernt alle SMIL-Animationen; die Flamme bleibt im Ausgangszustand stehen."""
    return re.sub(r"<animate(?:Transform)?\b[^>]*/>", "", text)


def svg(richtung: str, stufe: int) -> str:
    L, h = LAENGEN[stufe], HOEHEN[stufe]
    amp = h * 0.45
    hmax = HOEHEN[max(HOEHEN)]
    breite = LAENGEN[max(LAENGEN)] + 2 * RAND            # für alle Stufen gleich
    hoehe = 2 * math.ceil((hmax * 1.4 + hmax * 0.45) + 2)   # gerade, damit die Mitte auf ganzen px liegt
    cy = hoehe / 2
    g = f"fl{richtung[0]}{stufe}"
    flamme = [
        f'<defs>',
        f'  <linearGradient id="{g}a" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{L}" y2="0"><stop offset="0" stop-color="#FF9A1A"/><stop offset="0.6" stop-color="#F0501A"/><stop offset="1" stop-color="#C8261E"/></linearGradient>',
        f'  <linearGradient id="{g}b" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{L * .85:.1f}" y2="0"><stop offset="0" stop-color="#FFC21A"/><stop offset="1" stop-color="#FF7A00"/></linearGradient>',
        f'  <linearGradient id="{g}c" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{L * .62:.1f}" y2="0"><stop offset="0" stop-color="#FFF08A"/><stop offset="1" stop-color="#FFC21A"/></linearGradient>',
        f'</defs>',
        schicht(L, h, amp, f"url(#{g}a)", 0.9, 0.85, 2.0),
        schicht(L * .85, h * .74, amp * .8, f"url(#{g}b)", 0.95, 0.65, 2.6, 0.13),
        schicht(L * .62, h * .5, amp * .55, f"url(#{g}c)", 1, 0.5, 3.2, 0.31),
        schicht(L * .36, h * .26, amp * .3, "#FFFDF0", 0.95, 0.4, 3.6, 0.5),
        f'<ellipse cx="2" cy="0" rx="{3 + stufe * 0.8:.1f}" ry="{h * .48:.1f}" fill="#3F8CFF" opacity="0.7"><animate attributeName="opacity" values="0.7;0.45;0.7" dur="0.35s" repeatCount="indefinite"/></ellipse>',
    ]
    innen = "\n    ".join(flamme)
    if richtung == "links":
        trafo = f"translate({RAND},{cy})"
    else:
        trafo = f"translate({breite - RAND},{cy}) scale(-1,1)"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}" height="{hoehe}" viewBox="0 0 {breite} {hoehe}">\n'
            f'  <!-- Brennerflamme {richtung}, Stufe {stufe}: Wurzel bei x={RAND if richtung == "links" else breite - RAND}, y={cy:g} -->\n'
            f'  <g transform="{trafo}">\n    {innen}\n  </g>\n</svg>\n')


if __name__ == "__main__":
    import resvg_py
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "symbole" / "hydraulik"
    for richtung in ("links", "rechts"):
        for stufe in LAENGEN:
            p = ziel / f"Brenner_Flamme_{richtung}_{stufe}.svg"
            p.write_text(svg(richtung, stufe), encoding="utf-8")
            print(p)
            s = ziel / f"Brenner_Flamme_{richtung}_{stufe}_statisch.svg"
            s.write_text(statisch(svg(richtung, stufe)), encoding="utf-8")
            s.with_suffix(".png").write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=s.read_text(encoding="utf-8"))))
            print(s)
