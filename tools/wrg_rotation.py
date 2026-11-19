#!/usr/bin/env python3
"""Erzeugt symbole/lueftung/wrg/WRG_Rotation_{senkrecht,waagerecht,vorne}_{aus,an,stoerung}.svg.

Rotationswärmetauscher (Wärmerad), neutral gezeichnet, ohne Logos. Aufruf: python tools/wrg_rotation.py

  senkrecht   80 × 400, Rad von außen gesehen (Lauffläche), Kanäle setzen links und rechts an,
              Kanalachsen y = 60 (oben, Abluft/Fortluft) und y = 340 (unten, Außenluft/Zuluft), Kanäle 20 px.
              Links leicht schräg die Stirnseite des Rads (Ellipse mit Speichen), Lamellen perspektivisch
              (zu den Enden dichter), Mittelsteg mit Nabe trennt die Luftströme.
  waagerecht  400 × 80, dasselbe um 90° gedreht für senkrechte Kanäle: Kanalachsen x = 60 und x = 340,
              Kanäle setzen oben und unten an.
  vorne       180 × 180, Vorderansicht: Rahmen, Rad mit Speichen, Kreuzsteg, Nabe (Gerätebild, ohne Kanalanschluss).

Zustände:
  _aus        Rad steht
  _an         Rad dreht (SMIL): Lamellen laufen über die Rundung, Speichen drehen mit; Drehrichtungspfeile
  _stoerung   Rad steht, rotes Warndreieck blinkt (1 Hz)
"""
import math
from pathlib import Path

from zustandsfarben import STOERUNG

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "lueftung" / "wrg"
ROT = STOERUNG[1]

DEFS = """<defs>
<linearGradient id="gG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F0F1F2"/><stop offset="1" stop-color="#D2D5D8"/></linearGradient>
<linearGradient id="gK" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#A8A8A8"/><stop offset="0.5" stop-color="#E6E6E6"/><stop offset="1" stop-color="#A8A8A8"/></linearGradient>
<linearGradient id="gR" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E8CFB4"/><stop offset="0.5" stop-color="#DADDE0"/><stop offset="1" stop-color="#C9DDB8"/></linearGradient>
<linearGradient id="gT" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2B3440" stop-opacity="0.35"/><stop offset="0.25" stop-color="#2B3440" stop-opacity="0"/><stop offset="0.75" stop-color="#2B3440" stop-opacity="0"/><stop offset="1" stop-color="#2B3440" stop-opacity="0.35"/></linearGradient>
<linearGradient id="gZ" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2B3440" stop-opacity="0.45"/><stop offset="0.2" stop-color="#2B3440" stop-opacity="0.08"/><stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.15"/><stop offset="0.8" stop-color="#2B3440" stop-opacity="0.08"/><stop offset="1" stop-color="#2B3440" stop-opacity="0.45"/></linearGradient>
<radialGradient id="gW" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#6B7480"/><stop offset="1" stop-color="#3E4752"/></radialGradient>
</defs>"""


def warnung(cx: float, cy: float, s: float = 1.0) -> str:
    return ('<g><animate attributeName="opacity" values="1;0.15" dur="1s" calcMode="discrete" repeatCount="indefinite"/>'
            f'<g transform="translate({cx} {cy}) scale({s})">'
            f'<path d="M0,-24 L26,20 L-26,20 Z" fill="{ROT}" stroke="#FFFFFF" stroke-width="3" stroke-linejoin="round"/>'
            '<rect x="-3" y="-12" width="6" height="20" rx="3" fill="#FFFFFF"/><circle cx="0" cy="14" r="3.5" fill="#FFFFFF"/></g></g>')


def senkrecht(z: str, warn: bool = True):
    """80 × 400, Kanalachsen y = 60 (oben) und y = 340 (unten), Kanäle 20 px, links/rechts."""
    W, H = 80, 400
    s = []
    # Rad von außen: Lauffläche (Zylinder, Achse waagerecht) + leicht schräg gesehene Stirnseite links (Ellipse)
    CY, R, FX, FR = 200, 186, 24, 9          # Radmitte, Radius, Stirnseite x, Ellipsen-Halbachse
    D, T, N = 7.5, 0.25, 7                    # Lamellenabstand in Grad, Zeit dafür, Stützstellen
    s.append('<rect x="14" y="20" width="52" height="360" fill="url(#gR)"/>')
    s.append(f'<ellipse cx="{FX}" cy="{CY}" rx="{FR}" ry="{R}" fill="#B9C0C7" stroke="#6B7480" stroke-width="1"/>')

    def punkt(grad, r=R):
        a = math.radians(grad)
        return FX + FR * math.cos(a) * r / R, CY + r * math.sin(a)

    def werte(fn, start, schritt):
        return ";".join(f"{fn(start + schritt * i / (N - 1)):.2f}" for i in range(N))

    lam = []
    for k in range(int(180 / D) + 1):
        th = -90 - D + k * D
        x1, y = punkt(th)
        a = ""
        if z == "an":
            a = "".join(f'<animate attributeName="{att}" values="{werte(fn, th, D)}" dur="{T}s" repeatCount="indefinite"/>'
                        for att, fn in (("y1", lambda g: punkt(g)[1]), ("y2", lambda g: punkt(g)[1]),
                                        ("x1", lambda g: punkt(g)[0])))
        lam.append(f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="66" y2="{y:.2f}">{a}</line>')
    s.append(f'<g stroke="#7D8792" stroke-width="1" stroke-opacity="0.85">{"".join(lam)}</g>')
    # Speichen auf der Stirnseite, drehen mit derselben Winkelgeschwindigkeit
    sp = []
    for k in range(8):
        ph = k * 45 + 20
        x2, y2 = punkt(ph, R - 2)
        a = ""
        if z == "an":
            t = T * 45 / D
            a = "".join(f'<animate attributeName="{att}" values="{werte(fn, ph, 45)}" dur="{t}s" repeatCount="indefinite"/>'
                        for att, fn in (("x2", lambda g: punkt(g, R - 2)[0]), ("y2", lambda g: punkt(g, R - 2)[1])))
        sp.append(f'<line x1="{FX}" y1="{CY}" x2="{x2:.2f}" y2="{y2:.2f}">{a}</line>')
    s.append(f'<g stroke="#EEF0F2" stroke-width="1.6" stroke-linecap="round">{"".join(sp)}</g>')
    # Rundung: Lauffläche zu den Enden hin dunkler, quer leichter Tiefenschatten
    s.append('<rect x="14" y="20" width="52" height="360" fill="url(#gZ)"/>')
    s.append('<rect x="14" y="20" width="52" height="360" fill="url(#gT)" opacity="0.6"/>')
    # Gehäuse als Rahmen: Seitenwangen, Abdeckungen oben/unten (decken Lamellen-Überstand ab), Mittelsteg
    s.append('<path d="M10,14 H70 V386 H10 Z M14,24 V376 H66 V24 Z" fill="url(#gG)" fill-rule="evenodd" stroke="#999999" stroke-width="2"/>')
    s.append('<rect x="14" y="20" width="52" height="360" fill="none" stroke="#6B7480" stroke-width="1.4"/>')
    s.append('<rect x="4" y="2" width="72" height="16" rx="3" fill="url(#gK)" stroke="#808080" stroke-width="1.4"/>')
    s.append('<rect x="4" y="382" width="72" height="16" rx="3" fill="url(#gK)" stroke="#808080" stroke-width="1.4"/>')
    s.append('<rect x="10" y="193" width="60" height="14" fill="url(#gG)" stroke="#999999" stroke-width="1.6"/>')
    s.append('<rect x="33" y="188" width="14" height="24" rx="3" fill="#55606D" stroke="#2B3440" stroke-width="1.2"/>')
    s.append('<circle cx="40" cy="200" r="3.5" fill="#B5BCC4"/>')
    # Drehrichtungspfeil am Steg
    if z == "an":
        s.append('<g fill="none" stroke="#4D4D4D" stroke-width="1.6" stroke-linecap="round">'
                 '<path d="M58,170 v14 M55,181 l3,3 3,-3"/>'
                 '<path d="M58,216 v14 M55,227 l3,3 3,-3"/></g>')
    if z == "stoerung" and warn:
        s.append(warnung(40, 200, 0.9))
    return W, H, "".join(s)


def vorne(z: str):
    """180 × 180, Vorderansicht wie im Foto: Rahmen, Rad mit Speichen, Kreuzsteg."""
    W, H, c, r = 180, 180, 90, 76
    s = ['<rect x="2" y="2" width="176" height="176" rx="4" fill="url(#gG)" stroke="#999999" stroke-width="2"/>',
         f'<circle cx="{c}" cy="{c}" r="{r + 3}" fill="#B5BCC4" stroke="#999999" stroke-width="1.2"/>',
         f'<circle cx="{c}" cy="{c}" r="{r}" fill="url(#gW)" stroke="#2B3440" stroke-width="1.4"/>']
    rad = [f'<circle cx="{c}" cy="{c}" r="46" fill="none" stroke="#9AA2AB" stroke-width="1" stroke-opacity="0.7"/>']
    for i in range(8):
        a = math.radians(i * 45 + 10)
        x1, y1 = c + 13 * math.cos(a), c + 13 * math.sin(a)
        x2, y2 = c + (r - 1) * math.cos(a), c + (r - 1) * math.sin(a)
        rad.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#E6E8EA" stroke-width="2.6"/>')
    anim = (f'<animateTransform attributeName="transform" type="rotate" from="0 {c} {c}" to="360 {c} {c}" dur="6s" repeatCount="indefinite"/>'
            if z == "an" else "")
    s.append(f'<g>{anim}{"".join(rad)}</g>')
    # Kreuzsteg (trennt die Luftströme) und Nabe
    s.append(f'<rect x="2" y="{c - 4}" width="176" height="8" fill="#E6E6E6" stroke="#999999" stroke-width="1.2"/>')
    s.append(f'<rect x="{c - 4}" y="2" width="8" height="176" fill="#E6E6E6" stroke="#999999" stroke-width="1.2"/>')
    s.append(f'<circle cx="{c}" cy="{c}" r="12" fill="#F2F2F2" stroke="#808080" stroke-width="1.6"/>')
    s.append(f'<circle cx="{c}" cy="{c}" r="3" fill="#55606D"/>')
    if z == "an":
        s.append(f'<path d="M{c + 20},{c - 58} a62,62 0 0 1 38,38" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" opacity="0.85"/>'
                 f'<path d="M{c + 56},{c - 27} l2,8 l-8,-1" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" opacity="0.85"/>')
    if z == "stoerung":
        s.append(warnung(c, c, 1.0))
    return W, H, "".join(s)


def waagerecht(z: str):
    """400 × 80: senkrechte Variante um 90° gedreht (x' = y, y' = 80 − x); Warndreieck bleibt aufrecht."""
    _, _, inhalt = senkrecht(z, warn=False)
    s = f'<g transform="matrix(0 -1 1 0 0 80)">{inhalt}</g>'
    if z == "stoerung":
        s += warnung(200, 40, 0.9)
    return 400, 80, s


def svg(fn, z: str, titel: str) -> str:
    W, H, inhalt = fn(z)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">\n'
            f'  <title>{titel}</title>\n  {DEFS}\n  {inhalt}\n</svg>\n')


TITEL = {"aus": "aus", "an": "Betrieb", "stoerung": "Störung"}
ANSICHT = {"senkrecht": "Seitenansicht, Kanäle links/rechts", "waagerecht": "Seitenansicht, Kanäle oben/unten",
           "vorne": "Vorderansicht"}


def main() -> None:
    for name, fn in (("senkrecht", senkrecht), ("waagerecht", waagerecht), ("vorne", vorne)):
        for z in ("aus", "an", "stoerung"):
            p = ZIEL / f"WRG_Rotation_{name}_{z}.svg"
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(svg(fn, z, f"Rotationswärmetauscher, {ANSICHT[name]}, {TITEL[z]}"))
            print(p.name)


if __name__ == "__main__":
    main()
