# Mitwirken

Beiträge sind willkommen: neue Symbole, Varianten oder Korrekturen.

## Regeln für Symbole

- Nur SVG: keine PNG-, GIF- oder sonstigen Bilddateien unter `symbole/`. Animationen ebenfalls als SVG (SMIL).
- Kein `<text>`-Element, Schrift immer nur als Pfad – auch in beschrifteten und animierten Varianten. Umwandeln mit `tools/text_zu_pfad.ps1`.
- Keine Herstellerlogos, keine Nummern oder Beschriftungen im Symbol.
- Farben, Verläufe und Strichstärken nach [docs/STYLEGUIDE.md](docs/STYLEGUIDE.md).
- Richtungssymbole in allen vier Richtungen (`_rechts`, `_links`, `_oben`, `_unten`).
- Symbole einer Familie mit identischer Größe.
- Ablage in `symbole/<Fachbereich>/<Gruppe>/`, nie direkt im Fachbereich (siehe [Styleguide](docs/STYLEGUIDE.md#verzeichnisse)).
- Dateiname nach Schema `Symbol[_Variante][_Größe]_Ausrichtung[_Zustand][_Zusatz].svg` (siehe [Styleguide](docs/STYLEGUIDE.md#dateinamen)), Umlaute ausgeschrieben, keine Leerzeichen, keine Bindestriche (Niagara mag sie nicht).
- Bestehende Symbole dürfen nur nach Rückfrage beim Maintainer umbenannt werden, weil Dateinamen in Px-Seiten und Stationen referenziert sind. Jede Umbenennung wird in [docs/MIGRATION.csv](docs/MIGRATION.csv) nachgetragen.
- Größe und Anschlusspunkte in [docs/SYMBOLKATALOG.md](docs/SYMBOLKATALOG.md) eintragen.
- Nur eigene Zeichnungen einreichen, keine Kopien aus Herstellerbibliotheken.

## Prüfung

```bash
python tools/check_symbols.py
```

Das Skript läuft auch automatisch bei jedem Push und Pull Request (GitHub Actions).

## Lizenz

Mit einem Beitrag stimmen Sie zu, dass er unter der Lizenz [CC BY 4.0](LICENSE) des Projekts veröffentlicht wird.
