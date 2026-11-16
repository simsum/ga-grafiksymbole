"""Erzeugt symbole/hydraulik/Brenner_Rauch.svg: animierter Rauch für den Kamin (Abgasstutzen) des Kessels.

Ein Symbol für beide Kessel (Brenner links und rechts), transparenter Hintergrund, 64 × 96. Sechs weiche Rauchwolken
steigen versetzt auf, wachsen, schwanken leicht und blenden aus (SMIL, nur Verläufe und Deckkraft). Ohne Animation
sind die Wolken über die Aufstiegshöhe verteilt sichtbar.

Zusätzlich `Brenner_Rauch_statisch` (SVG + PNG, ohne Animation, gleiche Größe) als Ausweichlösung.

Position (linke obere Ecke des Rauch-Symbols relativ zur linken oberen Ecke des Kessel-Symbols 240 × 143):
  Kessel_Brenner_links:  x = 180, y = -92   (Abgasstutzen bei x = 204 … 220, Oberkante y = 0)
  Kessel_Brenner_rechts: x = -4,  y = -92   (Abgasstutzen bei x = 20 … 36)
Die Mündung liegt im Symbol bei (32, 92). Aufruf: python tools/rauch.py [Zielordner]
"""
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
B, H = 64, 96
MX, MY = 32, 92          # Mündung
HUB = 84                 # Aufstieg in px
ANZAHL = 6
DAUER = 5.0
PROBEN = 10


def zustand(p: float, ph: float) -> tuple[float, float, float, float]:
    """x, y, Maßstab, Deckkraft bei Zyklusanteil p (0…1)."""
    x = 5 * math.sin(2 * math.pi * (1.2 * p + ph)) * min(1, p * 3)
    y = -HUB * p
    s = 0.45 + 1.55 * p
    if p < 0.12:
        o = 0.7 * p / 0.12
    elif p < 0.55:
        o = 0.7 - 0.12 * (p - 0.12) / 0.43
    else:
        o = 0.58 * (1 - (p - 0.55) / 0.45)
    return x, y, s, max(0.0, o)


def wolke(i: int) -> str:
    p0 = i / ANZAHL
    ph = (i * 0.37) % 1
    x0, y0, s0, o0 = zustand(p0, ph)
    # Zyklus beginnt bei p0: Verlauf ab p0 (modulo 1) über die volle Dauer, begin negativ → t=0 entspricht p0
    ts = [k / PROBEN for k in range(PROBEN + 1)]
    pos = ";".join(f"{zustand(t, ph)[0]:.1f} {zustand(t, ph)[1]:.1f}" for t in ts)
    mas = ";".join(f"{zustand(t, ph)[2]:.2f}" for t in ts)
    deck = ";".join(f"{zustand(t, ph)[3]:.2f}" for t in ts)
    kt = ";".join(f"{t:.1f}" for t in ts)
    beginn = f"{-p0 * DAUER:.2f}s"
    kreise = [(0, 0, 7), (-5.5, 2, 5), (5.5, 1.5, 5.5), (0.5, -4.5, 5), (-2, 5, 4.5), (4, -3.5, 4)]
    def gruppe(farbe, dx, dy, f):
        return f'<g fill="{farbe}">' + "".join(f'<circle cx="{x * f + dx:.1f}" cy="{y * f + dy:.1f}" r="{r * f:.1f}"/>' for x, y, r in kreise) + "</g>"
    # flach gefüllt, damit sich überlappende Kreise nicht abzeichnen: dunkle Basis, hellere Kuppe oben links
    form = gruppe("#A9ADB3", 0.8, 1, 1) + gruppe("#C6CAD0", -0.4, -0.5, 0.88) + gruppe("#E2E4E8", -1.6, -2, 0.55)
    return (f'    <g transform="translate({x0:.1f},{y0:.1f})"><animateTransform attributeName="transform" type="translate" values="{pos}" keyTimes="{kt}" dur="{DAUER}s" begin="{beginn}" repeatCount="indefinite"/>\n'
            f'      <g transform="scale({s0:.2f})"><animateTransform attributeName="transform" type="scale" values="{mas}" keyTimes="{kt}" dur="{DAUER}s" begin="{beginn}" repeatCount="indefinite"/>\n'
            f'        <g opacity="{o0:.2f}"><animate attributeName="opacity" values="{deck}" keyTimes="{kt}" dur="{DAUER}s" begin="{beginn}" repeatCount="indefinite"/>{form}</g></g></g>')


def svg() -> str:
    wolken = "\n".join(wolke(i) for i in range(ANZAHL))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{B}" height="{H}" viewBox="0 0 {B} {H}">\n'
            f'  <!-- Rauch für den Kamin: Mündung bei ({MX},{MY}) -->\n'
            f'  <defs><radialGradient id="rg" cx="0.45" cy="0.4" r="0.7"><stop offset="0" stop-color="#E3E5E8"/><stop offset="0.6" stop-color="#B4B8BE"/><stop offset="1" stop-color="#8C9096"/></radialGradient></defs>\n'
            f'  <g transform="translate({MX},{MY})">\n{wolken}\n  </g>\n</svg>\n')


if __name__ == "__main__":
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "symbole" / "hydraulik"
    import resvg_py
    p = ziel / "Brenner_Rauch.svg"
    p.write_text(svg(), encoding="utf-8")
    print(p)
    s = ziel / "Brenner_Rauch_statisch.svg"
    s.write_text(re.sub(r"<animate(?:Transform)?\b[^>]*/>", "", svg()), encoding="utf-8")
    s.with_suffix(".png").write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=s.read_text(encoding="utf-8"))))
    print(s)
