# Symbolkatalog

Geplante und vorhandene Symbole mit Abmessungen und Anschlusspunkten. Alle Koordinaten in px, bezogen auf die linke obere Ecke des Bildes.

Status: Das Repository enthält die Symbole unter `symbole/` (jeweils SVG + PNG). Übersichtsgrafiken mit Hinweisen: [uebersicht/](uebersicht/). Die Tabellen beschreiben die Vorgaben. Das Volumenstromregler-Rund-Set heißt `Volumenstromregler_rund_*`, liegende Zortström-Speicher `Zortstroem_*_liegend`.

## Lüftung

| Symbol | Größe | Hinweise |
|---|---|---|
| Klimakonvektor (Kanalgerät, Draufsicht) | 160 × 90 (rechts/links), 90 × 160 (oben/unten) | Pfeil = Ausblasrichtung; zwei Radialventilatoren; Freifläche für Nummern-Label |
| Volumenstromregler rund | 140 × 80 / 80 × 140 | Rohr mit Flanschen, Klappe, Kompaktregler; links/oben gespiegelt, damit der Regler oben bzw. rechts sitzt |
| Volumenstromregler eckig | 140 × 80 / 80 × 140 | Rechteckkanal, drei gegenläufige Lamellen (zwei unter 40 px) |
| Deckenluftdurchlass rund (Hallen-Lochblech) | quadratisch | Kreis füllt die Bildfläche, ohne Stellhebel |
| WRG Kreuzstrom-Plattenwärmetauscher | 400 × 480 (im Schema ca. 331 × 399) | Kein Rahmen; Anschlüsse links/rechts bei y = 46,5 und y = 435,5, Kanalhöhe 24; Varianten mit/ohne Bypass |

WRG-Luftwege: Außenluft oben links (grün) → Zuluft unten rechts (rot); Abluft oben rechts → Fortluft unten links (orange).

## Hydraulik

### Umschaltventil-Pfeile

- 40 × 40, quadratisch einsetzen; Knick auf den Kreuzungspunkt der Rohrachsen.
- Richtungen: `links-oben`, `rechts-oben`, `oben-links`, `oben-rechts`.
- Farben: `rot`, `blau`, `grau`.
- Vorlaufventil: heizen `links-oben_rot`, kühlen `rechts-oben_blau`. Rücklaufventil: heizen `oben-links_rot`, kühlen `oben-rechts_blau`.

### Flusspfeile

24 × 14 (waagerecht), 14 × 24 (senkrecht) für 12-px-Rohre. Position: Rohrmitte − 7.

### Zortström-Schichtenspeicher liegend

- Heizung 800 × 160 (6 Zonen A–F), Kälte 800 × 136 (5 Zonen A–E), Zonenhöhe 24.
- Zonenmitte y = Oberkante + 20 + 24 × (Zone − 1).
- Varianten ohne und mit Beschriftung.

### Zortström-Schichtenspeicher stehend

Beide 144 × 338, ohne Beschriftung, Tankkörper x = 2 … 142. Heizung 6 Zonen à 44 px, Kälte 5 Zonen à 52,8 px.

| Zone | Heizung (y) | Kälte (y) |
|---|---|---|
| A | 52 | 56 |
| B | 96 | 109 |
| C | 140 | 162 |
| D | 184 | 215 |
| E | 228 | 268 |
| F | 272 | – |

Farben Heizung (oben → unten): `#D7302B`, `#E8642C`, `#F29A38`, `#F5C542`, `#8DB8E3`, `#3D79C6`.
Farben Kälte (oben → unten): `#3A8C4E`, `#6DB07B`, `#A8D2B4`, `#7CA6DE`, `#2E6BC2`.

### Heizkessel mit Brenner (neutral)

- Seitenansicht 240 × 143, Brenner links oder rechts. Flansch-Oberkante y = 5.
  - Brenner links: Vorlauf x = 130, Rücklauf x = 170.
  - Brenner rechts: Vorlauf x = 110, Rücklauf x = 70.
- Vorderansicht 140 × 143: Vorlauf x = 42, Rücklauf x = 98, Abgas mittig dahinter.

### Absperrklappe Wasser

- Mit Antrieb 50 × 65, ohne Antrieb 50 × 30, Rohrachse y = 15.
- Stellungen: `neutral` (Scheibe schräg, grau), `auf` (waagerecht, grün `#2EAA3A`), `zu` (senkrecht, rot `#E0302A`).
- Endlagen-Marker 16 × 16: `Endlage_auf` (grün, waagerechter Strich), `Endlage_zu` (rot, senkrechter Strich).

### Energieventil

- 80 × 65 (rechts/links), 65 × 80 (oben/unten), Rohrachse 15.
- Ultraschall-Durchflusssensor stromaufwärts vor dem 2-Wege-Ventil, Antrieb unten bzw. rechts.
- Temperaturfühler als eigene Symbole.

### Zähler

Mit angedeutetem Rollenzählwerk (fünf Rollen, letzte rot).

- Wärmemengenzähler (rote Flamme), Kältemengenzähler (blaue Schneeflocke), Wasserzähler (blauer Tropfen): 60 × 65 waagerecht, 65 × 60 senkrecht, Rohrachse 15.
- Elektrozähler 50 × 60, Rollenzählwerk mit sechs Stellen oben, gelber Blitz unten.

### Pumpe

- 40 × 40. Ein: grün (`#A8DC96` → `#3E9A3A`), aus: grau (`#EDEDED` → `#A6A6A6`), Dreieck `#4D4D4D`.
- Animationsvarianten (laufender gestrichelter Ring, drehendes Laufrad) als CSS-SVG, SMIL-SVG und GIF in Planung.

## Anzeigen

### LEDs (flache Version)

- 32 × 32 inkl. Lichtschein, LED selbst ca. 21 px.
- Zustände: `aus`, `gruen`, `rot`, `blau`, `gelb`.
- Ring dezent hellgrau, gleichmäßige Linsenfarbe, kleiner Glanzpunkt.
- Umschalten über Binding auf `image` eines einzigen Pictures.
