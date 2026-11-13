"""Erzeugt symbole/hydraulik/Waermepumpe_Luft_Wasser_{rechts,links} (SVG + PNG, resvg-py).

Außengerät Luft/Wasser-Wärmepumpe, Monoblock, Vorderansicht. Aufruf: python tools/waermepumpe.py

Zustände (gleiche Größe und Anschlusspunkte):
  (ohne)        aus, Lüfter steht
  _an           Betrieb, Lüfter dreht, Windlinien wandern nach außen (nur im SVG)
                  _an.svg  animiertes SVG (SMIL) – läuft in 4.15 in Workbench und HTML5, bevorzugt
                  _an.gif  animiertes GIF (12 Bilder, 40 ms) als Ausweichlösung
                  _an.png  Standbild als Ausweichlösung
  _stoerung     Störung: Lüfter steht, rotes Warndreieck und rote Status-LED blinken (1 Hz)
  _abtau        Abtaubetrieb (Enteisung): Lüfter steht, Reif auf dem Lüfter, Schneeflocke,
                Schmelzwassertropfen, blaue Status-LED pulsiert
Bei _stoerung und _abtau zeigt das Standbild (PNG, oder SVG ohne SMIL) den Zustand vollständig,
nur die Tropfen fehlen dort.
"""
import io
import math
from pathlib import Path

W, H = 180, 168
VL_X, RL_X = 160, 140          # Anschluss rechts; links gespiegelt: 20 / 40
GIF_BILDER = 12                # Bilder je Flügelteilung (72°) – Schleife ist nahtlos
GIF_MS = 40                    # Anzeigedauer je Bild
GIF_MATTE = (166, 166, 166)    # Hintergrund, gegen den die Außenkanten geglättet werden
SVG_DREHDAUER = "2.4s"         # eine Umdrehung im animierten SVG

def body(winkel: float = 0.0, animation: str = "") -> str:
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
    # Flügelrad (drehbar); Schutzgitter bleibt stehend darüber
    s.append(f'<g transform="rotate({winkel:.2f} {cx} {cy})"><g>{animation}')
    for a in range(0, 360, 72):
        s.append(f'<ellipse cx="{cx}" cy="{cy-23}" rx="11.5" ry="21" fill="#55606D" transform="rotate({a} {cx} {cy})"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="8" fill="#8A94A0"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="#55606D"/>')
    s.append('</g></g>')
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

TITEL = {"aus": "", "an": ", Lüfter dreht", "stoerung": ", Störung", "abtau": ", Abtaubetrieb (Enteisung)"}

def overlay(seite: str, zustand: str) -> str:
    """Zustandsanzeige über dem Gerät, ungespiegelt (Dreieck und Schneeflocke sehen links wie rechts gleich aus)."""
    fx = 68 if seite == "rechts" else W - 68          # Lüftermitte
    lx = 145 if seite == "rechts" else W - 145 - 12   # Status-LED im Schaltkasten
    if zustand == "an":
        # Windlinien: wandern von der Mitte nach außen und verblassen; nur animiert sichtbar
        s = ['  <g>\n']
        for i, a in enumerate((0, 60, 120, 180, 240, 300)):
            beginn = f"{i * 0.25:.2f}s"
            s.append(f'    <g transform="rotate({a + 30} {fx} 79)"><path d="M{fx},64 q4,-4 0,-8 q-4,-4 0,-8" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" opacity="0">'
                     f'<animate attributeName="opacity" values="0;0.85;0" keyTimes="0;0.3;1" dur="1.5s" begin="{beginn}" repeatCount="indefinite"/>'
                     f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -26" dur="1.5s" begin="{beginn}" repeatCount="indefinite"/>'
                     f'</path></g>\n')
        s.append('  </g>\n')
        return "".join(s)
    if zustand == "stoerung":
        return (f'  <g>\n'
                f'    <animate attributeName="opacity" values="1;0.15" dur="1s" calcMode="discrete" repeatCount="indefinite"/>\n'
                f'    <rect x="{lx}" y="74" width="12" height="5" rx="1.5" fill="#E2231A"/>\n'
                f'    <path d="M{fx},48 L{fx + 32},104 L{fx - 32},104 Z" fill="#E2231A" stroke="#FFFFFF" stroke-width="3" stroke-linejoin="round"/>\n'
                f'    <rect x="{fx - 3.5}" y="62" width="7" height="25" rx="3.5" fill="#FFFFFF"/>\n'
                f'    <circle cx="{fx}" cy="95" r="4" fill="#FFFFFF"/>\n'
                f'  </g>\n')
    if zustand == "abtau":
        s = [f'  <g>\n',
             f'    <circle cx="{fx}" cy="79" r="49" fill="#CFE8FF" opacity="0.45"><animate attributeName="opacity" values="0.45;0.15;0.45" dur="3s" repeatCount="indefinite"/></circle>\n',
             f'    <rect x="{lx}" y="74" width="12" height="5" rx="1.5" fill="#2F9BE8"><animate attributeName="opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite"/></rect>\n',
             f'    <g transform="translate({fx} 79)">\n',
             f'      <circle r="17" fill="#FFFFFF" fill-opacity="0.9" stroke="#2F7FD0" stroke-width="1.5"/>\n',
             f'      <g fill="none" stroke="#2F7FD0" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">\n']
        for a in (0, 60, 120):
            s.append(f'        <path d="M0,-12 L0,12 M-3.5,-11.5 L0,-8 L3.5,-11.5 M-3.5,11.5 L0,8 L3.5,11.5" transform="rotate({a})"/>\n')
        s.append('      </g>\n    </g>\n')
        # Schmelzwassertropfen: nur animiert sichtbar
        for dx, beginn in ((-22, "0s"), (4, "0.7s"), (24, "1.4s")):
            s.append(f'    <g transform="translate({fx + dx} 0)"><path d="M0,-3 Q2.6,1 0,3.2 Q-2.6,1 0,-3 Z" fill="#5AA9E6" opacity="0">'
                     f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.8;1" dur="2.1s" begin="{beginn}" repeatCount="indefinite"/>'
                     f'<animateTransform attributeName="transform" type="translate" values="0 118;0 140" dur="2.1s" begin="{beginn}" repeatCount="indefinite"/>'
                     f'</path></g>\n')
        s.append('  </g>\n')
        return "".join(s)
    return ""

def svg(seite: str, zustand: str = "aus", winkel: float = 0.0) -> str:
    # gespiegelte Variante dreht intern andersherum, damit beide sichtbar im Uhrzeigersinn laufen
    richtung = -1 if seite == "links" else 1
    anim = ""
    if zustand == "an":
        anim = (f'<animateTransform attributeName="transform" type="rotate" from="0 68 79" '
                f'to="{360 * richtung} 68 79" dur="{SVG_DREHDAUER}" repeatCount="indefinite"/>')
    inner = body(winkel * richtung, anim)
    if seite == "links":
        inner = f'<g transform="translate({W} 0) scale(-1 1)">\n    {inner}\n  </g>'
    else:
        inner = f'<g>\n    {inner}\n  </g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title">\n'
            f'  <title id="title">Luft/Wasser-Wärmepumpe Außengerät (Monoblock), Vorderansicht, Anschluss {seite}{TITEL[zustand]}</title>\n'
            f'{DEFS}\n  {inner}\n{overlay(seite, zustand)}</svg>\n')

def gif(seite: str) -> bytes:
    """Animiertes GIF in Originalgröße; Außenkanten gegen GIF_MATTE geglättet, harte Transparenz."""
    import resvg_py
    from PIL import Image
    bilder = []
    for i in range(GIF_BILDER):
        png = bytes(resvg_py.svg_to_bytes(svg_string=svg(seite, winkel=72 * i / GIF_BILDER)))
        rgba = Image.open(io.BytesIO(png)).convert("RGBA")
        matte = Image.new("RGBA", rgba.size, GIF_MATTE + (255,))
        flach = Image.alpha_composite(matte, rgba).convert("RGB")
        maske = rgba.getchannel("A").point(lambda a: 255 if a >= 40 else 0)
        p = flach.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        p.paste(255, mask=maske.point(lambda a: 255 - a))      # Index 255 = transparent
        bilder.append(p)
    buf = io.BytesIO()
    bilder[0].save(buf, format="GIF", save_all=True, append_images=bilder[1:], duration=GIF_MS,
                   loop=0, transparency=255, disposal=2, optimize=False)
    return buf.getvalue()

if __name__ == "__main__":
    import resvg_py
    out = Path(__file__).resolve().parent.parent / "symbole" / "hydraulik"
    for seite in ("rechts", "links"):
        p = out / f"Waermepumpe_Luft_Wasser_{seite}.svg"
        p.write_text(svg(seite), encoding="utf-8")
        png = resvg_py.svg_to_bytes(svg_string=svg(seite))
        p.with_suffix(".png").write_bytes(bytes(png))
        print(p)
        a = out / f"Waermepumpe_Luft_Wasser_{seite}_an.svg"
        a.write_text(svg(seite, "an"), encoding="utf-8")
        a.with_suffix(".png").write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=svg(seite, winkel=36))))
        a.with_suffix(".gif").write_bytes(gif(seite))
        print(a, a.with_suffix(".gif"))
        for zustand in ("stoerung", "abtau"):
            z = out / f"Waermepumpe_Luft_Wasser_{seite}_{zustand}.svg"
            z.write_text(svg(seite, zustand), encoding="utf-8")
            z.with_suffix(".png").write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=svg(seite, zustand))))
            print(z)
