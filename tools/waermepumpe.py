"""Erzeugt symbole/hydraulik/Waermepumpe_Luft_Wasser_{rechts,links} (SVG + PNG, resvg-py).

Außengerät Luft/Wasser-Wärmepumpe, Monoblock, Vorderansicht. Aufruf: python tools/waermepumpe.py
"""
import math
from pathlib import Path

W, H = 180, 168
VL_X, RL_X = 160, 140          # Anschluss rechts; links gespiegelt: 20 / 40

def body() -> str:
    s = []
    # Grundrahmen / Füße
    s.append('<rect x="8" y="147" width="164" height="9" rx="1.5" fill="#4A4F55" stroke="#2E3237" stroke-width="1.2"/>')
    # Gehäuse
    s.append('<rect x="4" y="4" width="172" height="144" rx="3" fill="url(#gG)" stroke="#999999" stroke-width="2"/>')
    s.append('<rect x="5" y="5" width="170" height="6" fill="url(#gB)"/>')
    s.append('<line x1="5" y1="11" x2="175" y2="11" stroke="#B5B5B5" stroke-width="1.2"/>')
    # Lüfteröffnung mit Rahmen
    s.append('<rect x="11" y="18" width="114" height="122" rx="4" fill="#D9DCDF" stroke="#999999" stroke-width="1.6"/>')
    cx, cy, r = 68, 79, 50
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#2B3440" stroke="#6B7480" stroke-width="2"/>')
    for a in range(0, 360, 72):
        s.append(f'<ellipse cx="{cx}" cy="{cy-23}" rx="11.5" ry="21" fill="#55606D" transform="rotate({a} {cx} {cy})"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="8" fill="#8A94A0"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="#55606D"/>')
    # Schutzgitter: Ringe und Speichen, dezent
    for rr in (18, 30, 42):
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="#8A94A0" stroke-opacity="0.6" stroke-width="0.8"/>')
    for a in range(0, 360, 45):
        x1 = cx + 8 * math.cos(math.radians(a)); y1 = cy + 8 * math.sin(math.radians(a))
        x2 = cx + r * math.cos(math.radians(a)); y2 = cy + r * math.sin(math.radians(a))
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#8A94A0" stroke-opacity="0.6" stroke-width="0.8"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#8A94A0" stroke-width="0.8" stroke-dasharray="2 3"/>')
    # Serviceklappe / Schaltkasten auf Anschlussseite
    s.append('<rect x="132" y="18" width="38" height="122" fill="#F2F2F2" stroke="#999999" stroke-width="2"/>')
    s.append('<line x1="134" y1="58" x2="168" y2="58" stroke="#B5B5B5" stroke-width="1.2"/>')
    s.append('<line x1="134" y1="104" x2="168" y2="104" stroke="#B5B5B5" stroke-width="1.2"/>')
    s.append('<rect x="145" y="74" width="12" height="5" rx="1.5" fill="#4D4D4D"/>')
    # Anschlussabdeckung unten
    s.append('<rect x="136" y="112" width="30" height="24" rx="2" fill="#E6E6E6" stroke="#999999" stroke-width="1.2"/>')
    # Flansche VL/RL an der Unterkante (Anschlussseite)
    for x, col in ((VL_X, "#D7302B"), (RL_X, "#F29A38")):
        s.append(f'<rect x="{x-3}" y="156" width="6" height="4" fill="#8C8C8C" stroke="#6B6B6B" stroke-width="1"/>'
                 f'<rect x="{x-8}" y="160" width="16" height="5" rx="1" fill="{col}" stroke="#6B6B6B" stroke-width="1"/>')
    return "\n    ".join(s)

DEFS = '''  <defs>
    <linearGradient id="gB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E6E6E6"/><stop offset="0.07" stop-color="#E0E0E0"/><stop offset="1" stop-color="#999999"/></linearGradient>
    <linearGradient id="gG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F0F1F2"/><stop offset="1" stop-color="#D2D5D8"/></linearGradient>
  </defs>'''

def svg(seite: str) -> str:
    inner = body()
    if seite == "links":
        inner = f'<g transform="translate({W} 0) scale(-1 1)">\n    {inner}\n  </g>'
    else:
        inner = f'<g>\n    {inner}\n  </g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title">\n'
            f'  <title id="title">Luft/Wasser-Wärmepumpe Außengerät (Monoblock), Vorderansicht, Anschluss {seite}</title>\n'
            f'{DEFS}\n  {inner}\n</svg>\n')

if __name__ == "__main__":
    import resvg_py
    out = Path(__file__).resolve().parent.parent / "symbole" / "hydraulik"
    for seite in ("rechts", "links"):
        p = out / f"Waermepumpe_Luft_Wasser_{seite}.svg"
        p.write_text(svg(seite), encoding="utf-8")
        png = resvg_py.svg_to_bytes(svg_string=svg(seite))
        p.with_suffix(".png").write_bytes(bytes(png))
        print(p)
