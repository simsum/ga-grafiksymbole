#!/usr/bin/env python3
"""Erzeugt die Übersichtsgrafiken unter docs/uebersicht/ aus den Symbolen unter symbole/.

Je Symbolverzeichnis eine Grafik mit allen Symbolen (Kachel mit Vorschau,
Dateiname und Größe). Alle Verzeichnisse unterhalb von symbole/ mit SVGs werden
berücksichtigt. Animierte SVGs erscheinen im Ausgangszustand.

Benötigt Pillow und resvg-py (pip install pillow resvg-py); die Vorschauen werden
direkt aus den SVGs gerendert.

Aufruf: python tools/uebersichten.py [Zielordner]
        python tools/uebersichten.py --nur lueftung [Zielordner]
"""
import io
import re
import sys
from pathlib import Path

import resvg_py as _resvg
from PIL import Image, ImageDraw, ImageFont

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

HINTERGRUND = (244, 245, 247)
KACHEL = (200, 200, 200)
KACHEL_RAND = (187, 189, 192)
KACHEL_SCHATTEN = (209, 211, 215)
TITEL = (48, 52, 58)
NAME = (32, 36, 42)
GRAU = (105, 114, 122)

SCHRIFTEN_FETT = ["arialbd.ttf", "LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf", "Helvetica-Bold.ttf"]
SCHRIFTEN_NORMAL = ["arial.ttf", "LiberationSans-Regular.ttf", "DejaVuSans.ttf", "Helvetica.ttf"]


def schrift(namen: list[str], groesse: int) -> ImageFont.FreeTypeFont:
    for n in namen:
        try:
            return ImageFont.truetype(n, groesse)
        except OSError:
            continue
    raise SystemExit("Keine passende Schrift gefunden (Arial, Liberation Sans oder DejaVu Sans installieren).")


def namenszeilen(name: str) -> list[str]:
    """Lange Namen werden am Unterstrich so auf zwei Zeilen verteilt, dass die längere Zeile möglichst kurz ist."""
    if len(name) <= MAX_ZEICHEN or "_" not in name:
        return [name]
    stellen = [i for i, c in enumerate(name) if c == "_"]
    i = min(stellen, key=lambda s: max(s, len(name) - s - 1))
    return [name[:i], name[i + 1:]]


def svg_groesse(svg: Path) -> tuple[int, int]:
    """Liest die Größe aus width/height, ersatzweise aus der viewBox des Wurzelelements."""
    kopf = re.search(r"<svg\b[^>]*>", svg.read_text(encoding="utf-8"), re.S).group(0)
    w = re.search(r'\swidth="([\d.]+)', kopf)
    h = re.search(r'\sheight="([\d.]+)', kopf)
    if w and h:
        return round(float(w.group(1))), round(float(h.group(1)))
    vb = re.search(r'viewBox="[\d.\-]+[ ,]+[\d.\-]+[ ,]+([\d.]+)[ ,]+([\d.]+)"', kopf)
    return round(float(vb.group(1))), round(float(vb.group(2)))


def rendern(svg: Path, groesse: tuple[int, int]) -> Image.Image:
    """Rendert das SVG scharf in Zielgröße."""
    daten = _resvg.svg_to_bytes(svg_string=svg.read_text(encoding="utf-8"), width=groesse[0], height=groesse[1])
    return Image.open(io.BytesIO(bytes(daten))).convert("RGBA")


def kachel(bild: Image.Image, draw: ImageDraw.ImageDraw, x: int, y: int, svg: Path, f_name, f_klein) -> None:
    draw.rounded_rectangle((x - 1, y - 1, x + KACHEL_B, y + KACHEL_H - 1), radius=11, fill=KACHEL_SCHATTEN)
    draw.rounded_rectangle((x, y, x + KACHEL_B - 1, y + KACHEL_H - 2), radius=10, fill=KACHEL, outline=KACHEL_RAND, width=1)

    breite, hoehe = svg_groesse(svg)
    massstab = min(VORSCHAU_B / breite, VORSCHAU_H / hoehe, MAX_MASSSTAB)
    gr = (max(1, round(breite * massstab)), max(1, round(hoehe * massstab)))
    vorschau = rendern(svg, gr)
    bild.paste(vorschau, (x + (KACHEL_B - gr[0]) // 2, y + VORSCHAU_MITTE_Y - gr[1] // 2), vorschau)

    mx = x + KACHEL_B / 2
    ty = y + 217
    zeilen = namenszeilen(svg.stem)
    for z in zeilen:
        draw.text((mx, ty), z, font=f_name, fill=NAME, anchor="mm")
        ty += 18
    draw.text((mx, ty + 3), f"{breite} × {hoehe} px", font=f_klein, fill=GRAU, anchor="mm")


def uebersicht(ordner: Path, ziel: Path) -> Path:
    svgs = sorted(ordner.glob("*.svg"), key=lambda p: p.stem)
    rel = ordner.relative_to(ROOT)
    name = "Uebersicht_" + "_".join(rel.parts[1:]) + ".png"
    zeilen = max(1, -(-len(svgs) // SPALTEN))
    hoehe = KOPF + zeilen * SCHRITT_Y + RAND - (SCHRITT_Y - KACHEL_H) + 13
    bild = Image.new("RGB", (BREITE, hoehe), HINTERGRUND)
    draw = ImageDraw.Draw(bild)
    draw.text((RAND, 33), rel.as_posix(), font=schrift(SCHRIFTEN_FETT, 26), fill=TITEL, anchor="lm")
    draw.text((BREITE - RAND, 36), f"{len(svgs)} Symbole", font=schrift(SCHRIFTEN_NORMAL, 16), fill=GRAU, anchor="rm")
    f_name, f_klein = schrift(SCHRIFTEN_FETT, 15), schrift(SCHRIFTEN_NORMAL, 12)
    for i, svg in enumerate(svgs):
        kachel(bild, draw, RAND + (i % SPALTEN) * SCHRITT_X, KOPF + (i // SPALTEN) * SCHRITT_Y, svg, f_name, f_klein)
    ziel.mkdir(parents=True, exist_ok=True)
    bild.save(ziel / name)
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
