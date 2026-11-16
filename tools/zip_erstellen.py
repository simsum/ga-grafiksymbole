"""Packt alle Symbole samt Verzeichnisstruktur in download/ga-grafiksymbole.zip.

Enthalten sind alle von Git verfolgten Dateien unter symbole/ sowie die LICENSE (CC BY 4.0).
Das Archiv ist reproduzierbar (sortierte Einträge, fester Zeitstempel, SVG mit LF-Zeilenenden):
ohne Änderungen an den Symbolen entsteht dieselbe Datei, es gibt also keine unnötigen Git-Änderungen.

Aufruf: python tools/zip_erstellen.py [Zieldatei]
Nach jeder Änderung an symbole/ erneut ausführen und das Archiv mitcommitten.
"""
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZEITSTEMPEL = (2025, 1, 1, 0, 0, 0)
TEXT = {".svg"}


def dateien() -> list[Path]:
    ausgabe = subprocess.run(["git", "ls-files", "-z", "symbole"], cwd=ROOT, capture_output=True, check=True).stdout
    liste = sorted(Path(p) for p in ausgabe.decode("utf-8").split("\0") if p)
    return [p for p in liste if (ROOT / p).exists()] + [Path("LICENSE")]


def main() -> int:
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "download" / "ga-grafiksymbole.zip"
    ziel.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ziel, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel in dateien():
            daten = (ROOT / rel).read_bytes()
            if rel.suffix in TEXT or rel.name == "LICENSE":
                daten = daten.replace(b"\r\n", b"\n")
            info = zipfile.ZipInfo(rel.as_posix(), ZEITSTEMPEL)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, daten)
    print(f"{ziel} ({ziel.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
