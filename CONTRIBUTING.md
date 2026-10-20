# Mitwirken

Beiträge sind willkommen: neue Symbole, Varianten oder Korrekturen.

## Regeln für Symbole

- SVG ohne `<text>`-Elemente; Buchstaben wie „M“ als Polygon zeichnen.
- Keine Herstellerlogos, keine Nummern oder Beschriftungen im Symbol.
- Farben, Verläufe und Strichstärken nach [docs/STYLEGUIDE.md](docs/STYLEGUIDE.md).
- Richtungssymbole in allen vier Richtungen (`_rechts`, `_links`, `_oben`, `_unten`).
- Symbole einer Familie mit identischer Größe.
- Dateiname `<Symbol>_<Richtung/Variante>.svg`, Umlaute ausgeschrieben, keine Leerzeichen, keine Bindestriche (Niagara mag sie nicht).
- Eine gleichnamige PNG beilegen (Ausweichlösung), im selben Ordner.
- Größe und Anschlusspunkte in [docs/SYMBOLKATALOG.md](docs/SYMBOLKATALOG.md) eintragen.
- Nur eigene Zeichnungen einreichen, keine Kopien aus Herstellerbibliotheken.

## Prüfung

```bash
python tools/check_symbols.py
```

Das Skript läuft auch automatisch bei jedem Push und Pull Request (GitHub Actions).

## Lizenz

Mit einem Beitrag stimmen Sie zu, dass er unter der Lizenz [CC BY 4.0](LICENSE) des Projekts veröffentlicht wird.
