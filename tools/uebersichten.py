#!/usr/bin/env python3
"""Erzeugt die Übersichtsgrafiken unter docs/uebersicht/ aus den Symbolen unter symbole/.

Je Symbolgruppe eine SVG-Grafik mit allen Symbolen (Kachel mit Vorschau, Dateiname und
Größe). Die Symbole werden als verschachtelte <svg> direkt eingebettet, animierte Symbole
laufen daher auch in der Übersicht (z. B. in der README auf GitHub). Damit sich die
Symbole nicht gegenseitig stören, erhalten alle IDs und url(#…)-Verweise je Kachel
ein eigenes Präfix.

Keine zusätzlichen Pakete nötig.

Aufruf: python tools/uebersichten.py [Zielordner]
        python tools/uebersichten.py --nur lueftung [Zielordner]
"""
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
SYMBOLE = ROOT / "symbole"

BREITE = 1560
RAND = 20
KOPF = 70            # Höhe der Kopfzeile bis zur ersten Kachelreihe
SPALTEN = 4
KACHEL_B, KACHEL_H = 365, 275
SCHRITT_X, SCHRITT_Y = 380, 288
VORSCHAU_B, VORSCHAU_H = 280, 165   # Box für das Symbol, wird maßstäblich eingepasst
VORSCHAU_MITTE_Y = 108              # Mitte der Box in der Kachel
MAX_MASSSTAB = 3                    # kleine Symbole nicht stärker vergrößern
MAX_ZEICHEN = 27                    # längere Namen werden zweizeilig

HINTERGRUND = "#F4F5F7"
KACHEL = "#C8C8C8"
KACHEL_RAND = "#BBBDC0"
KACHEL_SCHATTEN = "#D1D3D7"
TITEL = "#30343A"
NAME = "#20242A"
GRAU = "#69727A"
SCHRIFT = "Segoe UI, Arial, Helvetica, sans-serif"

ID_RE = re.compile(r'\bid="([^"]+)"')
URL_RE = re.compile(r"url\(\s*#([^)\s]+)\s*\)")
HREF_RE = re.compile(r'\b((?:xlink:)?href)="#([^"]+)"')


def namenszeilen(name: str) -> list[str]:
    """Lange Namen werden am Unterstrich so auf zwei Zeilen verteilt, dass die längere Zeile möglichst kurz ist."""
    if len(name) <= MAX_ZEICHEN or "_" not in name:
        return [name]
    stellen = [i for i, c in enumerate(name) if c == "_"]
    i = min(stellen, key=lambda s: max(s, len(name) - s - 1))
    return [name[:i], name[i + 1:]]


def zerlegen(text: str) -> tuple[str, str]:
    """Liefert (Kopf des <svg>-Wurzelelements, Inhalt) ohne XML-Deklaration, DOCTYPE, Kommentare und <metadata>."""
    text = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>|<!--.*?-->|<metadata\b.*?</metadata>", "", text, flags=re.S)
    kopf = re.search(r"<svg\b[^>]*>", text, re.S)
    ende = text.rfind("</svg>")
    return kopf.group(0), text[kopf.end():ende].strip()


def svg_groesse(kopf: str) -> tuple[float, float, str]:
    """Breite, Höhe und viewBox aus dem Wurzelelement; fehlende Werte aus dem jeweils anderen."""
    w = re.search(r'\swidth="([\d.]+)', kopf)
    h = re.search(r'\sheight="([\d.]+)', kopf)
    vb = re.search(r'viewBox="([^"]+)"', kopf)
    if vb:
        werte = [float(x) for x in re.split(r"[\s,]+", vb.group(1).strip())]
        viewbox = vb.group(1).strip()
    else:
        werte = [0, 0, float(w.group(1)), float(h.group(1))]
        viewbox = f"0 0 {w.group(1)} {h.group(1)}"
    breite = float(w.group(1)) if w else werte[2]
    hoehe = float(h.group(1)) if h else werte[3]
    return breite, hoehe, viewbox


def ids_praefixen(inhalt: str, praefix: str) -> str:
    """Macht IDs eindeutig, damit gleichnamige Verläufe verschiedener Symbole nicht kollidieren."""
    ids = set(ID_RE.findall(inhalt))
    if not ids:
        return inhalt
    inhalt = ID_RE.sub(lambda m: f'id="{praefix}{m.group(1)}"', inhalt)
    inhalt = URL_RE.sub(lambda m: f"url(#{praefix}{m.group(1)})" if m.group(1) in ids else m.group(0), inhalt)
    return HREF_RE.sub(lambda m: f'{m.group(1)}="#{praefix}{m.group(2)}"' if m.group(2) in ids else m.group(0), inhalt)


def zahl(x: float) -> str:
    return f"{x:.2f}".rstrip("0").rstrip(".")


def kachel(nr: int, x: int, y: int, svg: Path) -> str:
    kopf, inhalt = zerlegen(svg.read_text(encoding="utf-8"))
    breite, hoehe, viewbox = svg_groesse(kopf)
    massstab = min(VORSCHAU_B / breite, VORSCHAU_H / hoehe, MAX_MASSSTAB)
    gb, gh = breite * massstab, hoehe * massstab
    sx, sy = x + (KACHEL_B - gb) / 2, y + VORSCHAU_MITTE_Y - gh / 2

    teile = [
        f'<g id="{escape(svg.stem)}">',
        f'<rect x="{x - 1}" y="{y - 1}" width="{KACHEL_B + 1}" height="{KACHEL_H}" rx="11" fill="{KACHEL_SCHATTEN}"/>',
        f'<rect x="{x}" y="{y}" width="{KACHEL_B - 1}" height="{KACHEL_H - 2}" rx="10" fill="{KACHEL}" stroke="{KACHEL_RAND}"/>',
        f'<svg x="{zahl(sx)}" y="{zahl(sy)}" width="{zahl(gb)}" height="{zahl(gh)}" viewBox="{viewbox}" overflow="hidden"'
        + "".join(" " + ns for ns in re.findall(r'xmlns:[\w-]+="[^"]*"', kopf)) + ">",
        ids_praefixen(inhalt, f"k{nr}_"),
        "</svg>",
    ]
    mx, ty = x + KACHEL_B / 2, y + 217
    for zeile in namenszeilen(svg.stem):
        teile.append(f'<text x="{zahl(mx)}" y="{ty}" class="name">{escape(zeile)}</text>')
        ty += 18
    teile.append(f'<text x="{zahl(mx)}" y="{ty + 3}" class="mass">{zahl(breite)} × {zahl(hoehe)} px</text>')
    teile.append("</g>")
    return "\n".join(teile)


def uebersicht(ordner: Path, ziel: Path) -> Path:
    svgs = sorted(ordner.glob("*.svg"), key=lambda p: p.stem)
    rel = ordner.relative_to(ROOT)
    name = "Uebersicht_" + "_".join(rel.parts[1:]) + ".svg"
    zeilen = max(1, -(-len(svgs) // SPALTEN))
    hoehe = KOPF + zeilen * SCHRITT_Y + RAND - (SCHRITT_Y - KACHEL_H) + 13
    teile = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{BREITE}" height="{hoehe}" viewBox="0 0 {BREITE} {hoehe}">',
        f"<title>{escape(rel.as_posix())}: {len(svgs)} Symbole</title>",
        f"<style>text{{font-family:{SCHRIFT}}}"
        f".name{{font-size:15px;font-weight:700;fill:{NAME};text-anchor:middle}}"
        f".mass{{font-size:12px;fill:{GRAU};text-anchor:middle}}</style>",
        f'<rect width="{BREITE}" height="{hoehe}" fill="{HINTERGRUND}"/>',
        f'<text x="{RAND}" y="42" font-size="26" font-weight="700" fill="{TITEL}">{escape(rel.as_posix())}</text>',
        f'<text x="{BREITE - RAND}" y="42" font-size="16" fill="{GRAU}" text-anchor="end">{len(svgs)} Symbole</text>',
    ]
    for i, svg in enumerate(svgs):
        teile.append(kachel(i, RAND + (i % SPALTEN) * SCHRITT_X, KOPF + (i // SPALTEN) * SCHRITT_Y, svg))
    teile.append("</svg>\n")
    ziel.mkdir(parents=True, exist_ok=True)
    (ziel / name).write_text("\n".join(teile), encoding="utf-8", newline="\n")
    return ziel / name


def symbolordner() -> list[Path]:
    return sorted(p for p in SYMBOLE.rglob("*") if p.is_dir() and any(p.glob("*.svg")))


def main() -> int:
    args = sys.argv[1:]
    nur = None
    if args[:1] == ["--nur"]:
        nur, args = args[1], args[2:]
    ziel = Path(args[0]) if args else ROOT / "docs" / "uebersicht"
    for ordner in symbolordner():
        if nur and nur not in ordner.relative_to(SYMBOLE).parts:
            continue
        print(uebersicht(ordner, ziel))
    return 0


if __name__ == "__main__":
    sys.exit(main())
