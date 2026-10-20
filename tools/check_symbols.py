#!/usr/bin/env python3
"""Prüft die SVG-Symbole unter symbole/ auf die Projektregeln.

Regeln:
  - gültiges XML mit <svg>-Wurzel
  - kein <text>-Element (Ausnahme: Dateien mit Endung _beschriftet)
  - Dateiname nach Schema Name_Variante.svg (ASCII, keine Leerzeichen)
  - gleichnamige PNG vorhanden (nur Warnung)

Aufruf: python tools/check_symbols.py [Ordner]
Exit-Code 1 bei Fehlern.
"""
import re
import sys
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
    if not svg.stem.endswith("_beschriftet") and any(el.tag in (SVG_NS + "text", "text") for el in root.iter()):
        errors.append("enthält <text> (Beschriftung gehört in Niagara-Labels; Ausnahme: Variante *_beschriftet)")
    if "viewBox" not in root.attrib and not ("width" in root.attrib and "height" in root.attrib):
        warnings.append("weder viewBox noch width/height gesetzt")
    if not svg.with_suffix(".png").exists():
        warnings.append("gleichnamige PNG fehlt")
    return errors, warnings


def main() -> int:
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "symbole"
    files = sorted(base.rglob("*.svg"))
    failed = 0
    for svg in files:
        errors, warnings = check(svg)
        rel = svg.relative_to(base.parent) if base.parent in svg.parents else svg
        for m in errors:
            print(f"FEHLER  {rel}: {m}")
        for m in warnings:
            print(f"WARNUNG {rel}: {m}")
        failed += bool(errors)
    print(f"{len(files)} SVG geprüft, {failed} mit Fehlern.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
