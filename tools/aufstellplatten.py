#!/usr/bin/env python3
"""Erzeugt symbole/allgemein/aufstellung/Aufstellplatte_{Beton,rund,Stahl}.svg.

3D-angedeutete Aufstellflächen, die in Px unter stehende Geräte gelegt werden (z. B. Pufferspeicher,
Schichtspeicher, Kessel). Alle drei 180 × 30, transparenter Hintergrund, Kontur wie die Speicher.

  _Beton   rechteckiger Betonsockel: helle Oberseite in Perspektive, dunklere Vorderkante
  _rund    rundes Podest: ovale Oberseite, zylindrischer Mantel (passt zu runden Speichern)
  _Stahl   flache Stahlplatte mit zwei Schraubenköpfen und weichem Kontaktschatten

Aufstellpunkt: Die Füße des Geräts stehen bei y = 9 (Mitte der Oberseite). Ein 144 px breiter Speicher
sitzt mittig, also 18 px vom linken Plattenrand: Platte bei (x_Speicher − 18, y_Fußunterkante − 9).

Aufruf: python tools/aufstellplatten.py [Zielordner]
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
B, H = 180, 30
KONTUR = "#5A5A5A"


def kopf(titel: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{B}" height="{H}" viewBox="0 0 {B} {H}">\n'
            f'  <!-- {titel}; Aufstellpunkt y = 9 (Mitte Oberseite), Speicher 144 px breit bei x = 18 -->\n')


def beton() -> str:
    return kopf("Aufstellplatte_Beton: Betonsockel, 3D angedeutet") + f'''  <defs>
    <linearGradient id="oben" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C9CBCE"/><stop offset="1" stop-color="#E2E4E6"/></linearGradient>
    <linearGradient id="vorne" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A9ACB0"/><stop offset="1" stop-color="#8A8D91"/></linearGradient>
    <linearGradient id="licht" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000000" stop-opacity=".12"/><stop offset=".4" stop-color="#FFFFFF" stop-opacity=".18"/><stop offset="1" stop-color="#000000" stop-opacity=".14"/></linearGradient>
  </defs>
  <path d="M14,2 H166 L178,16 H2 Z" fill="url(#oben)" stroke="{KONTUR}" stroke-width="1.5" stroke-linejoin="round"/>
  <path d="M2,16 H178 V27 a1.5,1.5 0 0 1 -1.5,1.5 H3.5 a1.5,1.5 0 0 1 -1.5,-1.5 Z" fill="url(#vorne)" stroke="{KONTUR}" stroke-width="1.5" stroke-linejoin="round"/>
  <rect x="2" y="16" width="176" height="12.5" fill="url(#licht)"/>
  <path d="M3,16.8 H177" stroke="#FFFFFF" stroke-opacity=".5" stroke-width="1"/>
</svg>
'''


def rund() -> str:
    return kopf("Aufstellplatte_rund: rundes Podest, 3D angedeutet") + f'''  <defs>
    <linearGradient id="mantel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7E8186"/><stop offset=".38" stop-color="#C3C6CA"/><stop offset="1" stop-color="#76797E"/></linearGradient>
    <radialGradient id="deckel" cx=".42" cy=".4" r=".7"><stop offset="0" stop-color="#EEF0F2"/><stop offset="1" stop-color="#C2C5C9"/></radialGradient>
  </defs>
  <path d="M2,9 V20 A88,8 0 0 0 178,20 V9 Z" fill="url(#mantel)" stroke="{KONTUR}" stroke-width="1.5" stroke-linejoin="round"/>
  <ellipse cx="90" cy="9" rx="88" ry="7.5" fill="url(#deckel)" stroke="{KONTUR}" stroke-width="1.5"/>
</svg>
'''


def stahl() -> str:
    return kopf("Aufstellplatte_Stahl: Stahlplatte mit Kontaktschatten, 3D angedeutet") + '''  <defs>
    <radialGradient id="schatten" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#000000" stop-opacity=".35"/><stop offset="1" stop-color="#000000" stop-opacity="0"/></radialGradient>
    <linearGradient id="platte" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9AA0A6"/><stop offset="1" stop-color="#C9CED3"/></linearGradient>
    <linearGradient id="kante" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4E5358"/><stop offset=".4" stop-color="#7C8288"/><stop offset="1" stop-color="#4A4F54"/></linearGradient>
  </defs>
  <ellipse cx="90" cy="22" rx="88" ry="6" fill="url(#schatten)"/>
  <path d="M10,4 H170 L176,14 H4 Z" fill="url(#platte)" stroke="#4A4F54" stroke-width="1.2" stroke-linejoin="round"/>
  <path d="M4,14 H176 V18 H4 Z" fill="url(#kante)" stroke="#4A4F54" stroke-width="1.2" stroke-linejoin="round"/>
  <g fill="#6F757B"><circle cx="16" cy="9" r="1.6"/><circle cx="164" cy="9" r="1.6"/></g>
</svg>
'''


def main() -> int:
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "symbole" / "allgemein" / "aufstellung"
    ziel.mkdir(parents=True, exist_ok=True)
    for name, f in (("Beton", beton), ("rund", rund), ("Stahl", stahl)):
        p = ziel / f"Aufstellplatte_{name}.svg"
        p.write_text(f(), encoding="utf-8", newline="\n")
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
