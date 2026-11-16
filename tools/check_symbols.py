#!/usr/bin/env python3
"""Prüft die SVG-Symbole unter symbole/ auf die Projektregeln.

Regeln:
  - unter symbole/ liegen nur SVG-Dateien (keine PNG, GIF o. Ä.)
  - gültiges XML mit <svg>-Wurzel
  - kein <text>-Element, Schrift nur als Pfad (auch in beschrifteten und animierten Varianten)
  - Dateiname nach Schema Name_Variante.svg (ASCII, keine Leerzeichen)

Aufruf: python tools/check_symbols.py [Ordner]
Exit-Code 1 bei Fehlern.
"""
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import xml.etree.ElementTree as ET
from pathlib import Path

NAME_RE = re.compile(r"^[A-Za-z0-9]+(_[A-Za-z0-9]+)*\.svg$")
SVG_NS = "{http://www.w3.org/2000/svg}"


def check(svg: Path) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    if not NAME_RE.match(svg.name):
        errors.append("Dateiname entspricht nicht dem Schema Name_Variante.svg (ASCII, nur Unterstriche, kein Bindestrich)")
    try:
        root = ET.parse(svg).getroot()
    except ET.ParseError as e:
        return [f"kein gültiges XML: {e}"], warnings
    if root.tag not in (SVG_NS + "svg", "svg"):
        errors.append("Wurzelelement ist kein <svg>")
    if any(el.tag in (SVG_NS + "text", "text") for el in root.iter()):
        errors.append("enthält <text> (Schrift nur als Pfad; Werte und Beschriftung als Niagara-Label)")
    if "viewBox" not in root.attrib and not ("width" in root.attrib and "height" in root.attrib):
        warnings.append("weder viewBox noch width/height gesetzt")
    return errors, warnings


def main() -> int:
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "symbole"
    files = sorted(base.rglob("*.svg"))
    failed = 0
    for fremd in sorted(p for p in base.rglob("*") if p.is_file() and p.suffix.lower() != ".svg"):
        rel = fremd.relative_to(base.parent) if base.parent in fremd.parents else fremd
        print(f"FEHLER  {rel}: keine SVG-Datei (unter symbole/ sind nur SVGs erlaubt)")
        failed += 1
    for svg in files:
        errors, warnings = check(svg)
        rel = svg.relative_to(base.parent) if base.parent in svg.parents else svg
        for m in errors:
            print(f"FEHLER  {rel}: {m}")
        for m in warnings:
            print(f"WARNUNG {rel}: {m}")
        failed += bool(errors)
    print(f"{len(files)} SVG geprüft, {failed} Datei(en) mit Fehlern.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
