# Symbolkatalog

Geplante und vorhandene Symbole mit Abmessungen und Anschlusspunkten. Alle Koordinaten in px, bezogen auf die linke obere Ecke des Bildes.

Status: Das Repository enthält die Symbole unter `symbole/` (jeweils SVG + PNG). Übersichtsgrafiken mit Hinweisen: [uebersicht/](uebersicht/). Die Tabellen beschreiben die Vorgaben. Das Volumenstromregler-Rund-Set heißt `Volumenstromregler_rund_*`, liegende Zortström-Speicher `Zortstroem_*_liegend`.

## Allgemein

Fachübergreifende Symbole (Wasser, Luft, Strom) unter `symbole/allgemein/`.

### Flusspfeile

24 × 14 (waagerecht), 14 × 24 (senkrecht), passend zu 12-px-Rohren; auch auf Luftkanälen und Stromleitungen einsetzbar. Position: Leitungsmitte − 7.

Variante `_an` (z. B. `Flusspfeil_rechts_an`), gleiche Größe: drei helle Punkte laufen in Flussrichtung durch den Pfeil (SMIL, 1,2 s). Ohne Animation normaler Pfeil. Für „fließt“ / „steht“ per `image`-Binding zwischen `Flusspfeil_rechts.svg` und `…_an.svg` umschalten, z. B. gekoppelt an den Pumpen- oder Ventilatorbetrieb.

### Flusspfeile mit Bogen (90°)

- 24 × 24, gleiche Schaft- und Spitzenbreite wie die geraden Flusspfeile, Bogen außen r = 7, innen r = 3.
- `Flusspfeil_Knick_<vorher>_<nachher>`: erst die Flussrichtung vor dem Bogen, dann danach, z. B. `Flusspfeil_Knick_rechts_unten` (fließt nach rechts, biegt nach unten ab). Acht Richtungen: `rechts_unten`, `rechts_oben`, `links_unten`, `links_oben`, `unten_rechts`, `unten_links`, `oben_rechts`, `oben_links`.
- Position: Schnittpunkt der Rohrachsen im Bild – (17, 7): `rechts_unten`, `oben_links`; (17, 17): `rechts_oben`, `unten_links`; (7, 7): `links_unten`, `oben_rechts`; (7, 17): `links_oben`, `unten_rechts`.
- Variante `_an` wie bei den geraden Pfeilen: helle Punkte laufen um den Bogen bis in die Spitze (SMIL, 1,4 s).

### Trennung / Durchführung (Decke, Wand)

- Schraffiertes Band (zwei Randlinien, Schraffur 45°), 16 px stark, Hintergrund transparent – Leitungen werden darübergelegt.
- `Trennung_{horizontal,vertikal}_<Länge>` mit Länge 60, 120, 180, 240, 300 px (horizontal L × 16, vertikal 16 × L).
- Ohne Zusatz hell (`#C8C8D0`, für dunkle Hintergründe), `_dunkel` (`#555555`, für helle Hintergründe).
- Nicht verzerrt skalieren: passende Länge wählen, damit die Schraffur gleichmäßig bleibt.

## Lüftung

| Symbol | Größe | Hinweise |
|---|---|---|
| Klimakonvektor (Kanalgerät, Draufsicht) | 160 × 90 (rechts/links), 90 × 160 (oben/unten) | Pfeil = Ausblasrichtung; zwei Radialventilatoren; Freifläche für Nummern-Label |
| Volumenstromregler rund | 140 × 80 / 80 × 140 | Rohr mit Flanschen, Klappe, Kompaktregler; links/oben gespiegelt, damit der Regler oben bzw. rechts sitzt |
| Volumenstromregler eckig | 140 × 80 / 80 × 140 | Rechteckkanal, drei gegenläufige Lamellen (zwei unter 40 px) |
| Deckenluftdurchlass rund (Hallen-Lochblech) | quadratisch | Kreis füllt die Bildfläche, ohne Stellhebel |
| WRG Kreuzstrom-Plattenwärmetauscher | 400 × 480 (im Schema ca. 331 × 399) | Kein Rahmen; Anschlüsse links/rechts bei y = 46,5 und y = 435,5, Kanalhöhe 24; Varianten mit/ohne Bypass |
| WRG mit Flanschen (`WRG_Platte_mit_Bypass_PlusMinus_Flansch`) | 400 × 480 | Wie oben, zusätzlich Flansch (6 × 34) an allen vier Anschlüssen ganz außen am Symbolrand; Kanäle enden am Flansch. Bestehender Kanal im Schema muss an der Flanschkante enden |
| Klappe, ein Blatt, senkrecht/waagerecht (`lueftung/klappen/klein/Klappe_senkrecht_klein_1_zu` bis `_5_auf`, `Klappe_waagerecht_klein_…`) | klein 30 × 60 / 60 × 30, groß 40 × 80 / 80 × 40 | Fünf Stellungen 1_zu, 2_25, 3_50, 4_75, 5_auf (Blattwinkel zur Kanalachse 90° / 67,5° / 45° / 22,5° / 0°); Kanal verläuft entlang der langen Seite; grau, Statusfarbe über Niagara. Abgeleitet von AC0531 und AC0532 (M, L); große Variante in `klappen/gross/` (`Klappe_senkrecht_gross_…`, `Klappe_waagerecht_gross_…`) |
| Klappe, drei Blätter, senkrecht/waagerecht (`Klappe_senkrecht_3blatt_klein_…`, `Klappe_waagerecht_3blatt_klein_…`, groß: `…_3blatt_gross_…`) | klein 30 × 60 / 60 × 30, groß 40 × 80 / 80 × 40 | Drei Blätter, Blattlänge nimmt Richtung „auf“ ab. Abgeleitet von AC0511/AC0521 (senkrecht) und AC0512/AC0522 (waagerecht), M und L. Waagerechte Klappen kippen wie das Original AC0532 nach „\“, senkrechte nach „/“ |

Klappen: Blattwinkel zur Kanalachse, zu = quer, auf = längs. Die Klappen stammen aus der SBC-Icon-Galerie (Honeywell) und werden von `tools/klappen.py` erzeugt.

WRG-Luftwege: Außenluft oben links (grün) → Zuluft unten rechts (rot); Abluft oben rechts → Fortluft unten links (orange).

## Hydraulik

### Umschaltventil-Pfeile

- 40 × 40, quadratisch einsetzen; Knick auf den Kreuzungspunkt der Rohrachsen.
- Richtungen: `links-oben`, `rechts-oben`, `oben-links`, `oben-rechts`.
- Farben: `rot`, `blau`, `grau`.
- Vorlaufventil: heizen `links-oben_rot`, kühlen `rechts-oben_blau`. Rücklaufventil: heizen `oben-links_rot`, kühlen `oben-rechts_blau`.

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

### Mehrleitermaschine (luftgekühlt, Monoblock)

Wärmepumpe/Kältemaschine mit mehreren Hydraulikkreisen, neutral gezeichnet, ohne Logos. Jedes Gerät hat immer beide Kreise: Heizen (Kondensatorseite) und Kühlen (Verdampferseite), jeweils mit Vorlauf (VL) und Rücklauf (RL). Die vier Anschlüsse sind nur als angedeutete Flansche an der Unterkante dargestellt, der Schaltschrank sitzt auf der Anschlussseite. „links/rechts“ bezeichnet die Anschlussseite.

| Symbol | Größe | Anschlusspunkte (x; y = Unterkante) |
|---|---|---|
| `Mehrleitermaschine_Seite_links` | 260 × 172 | Heizen VL 18, RL 38; Kühlen VL 66, RL 86; y = 172 |
| `Mehrleitermaschine_Seite_rechts` | 260 × 172 | Heizen VL 242, RL 222; Kühlen VL 194, RL 174; y = 172 |
| `Mehrleitermaschine_Draufsicht_links` | 260 × 124 | Heizen VL 14, RL 32; Kühlen VL 58, RL 76; y = 124 |
| `Mehrleitermaschine_Draufsicht_rechts` | 260 × 124 | Heizen VL 246, RL 228; Kühlen VL 202, RL 184; y = 124 |

Flanschfarben: Heizen VL `#D7302B`, RL `#F29A38`; Kühlen VL `#2E6BC2`, RL `#7CA6DE`. Die Bezeichnung der Kreise erfolgt über Labels, z. B. `WP01-H`, `WP01-K` (siehe Anlagenkennzeichnung im Styleguide).

### Luft/Wasser-Wärmepumpe (Außengerät, Monoblock)

Kompaktes Außengerät mit einem Ventilator, Vorderansicht, neutral gezeichnet, ohne Logos. Ein Hydraulikkreis mit Vorlauf und Rücklauf als angedeutete Flansche an der Unterkante; Serviceklappe auf der Anschlussseite. „links/rechts“ bezeichnet die Anschlussseite.

| Symbol | Größe | Anschlusspunkte (x; y = Unterkante) |
|---|---|---|
| `Waermepumpe_Luft_Wasser_links` | 180 × 168 | VL 20, RL 40; y = 168 |
| `Waermepumpe_Luft_Wasser_rechts` | 180 × 168 | VL 160, RL 140; y = 168 |

Zustandsvarianten, jeweils für `links` und `rechts`, gleiche Größe und Anschlusspunkte:

| Zustand | Suffix | Darstellung |
|---|---|---|
| aus | – | Lüfter steht |
| Betrieb | `_an` | Lüfter dreht, Windlinien wandern von der Mitte nach außen; `.svg` animiert per SMIL (läuft in 4.15 in Workbench und Browser, bevorzugt), `.gif` als Ausweichlösung (12 Bilder à 40 ms), `.png` als Standbild |
| Störung | `_stoerung` | Lüfter steht, rotes Warndreieck mit Ausrufezeichen und rote Status-LED blinken (1 Hz) |
| Abtaubetrieb | `_abtau` | Lüfter steht, Reif auf dem Lüfter, Schneeflocke, Schmelzwassertropfen, blaue Status-LED pulsiert |

Bei `_stoerung` und `_abtau` zeigt auch das Standbild (ohne Animation) den Zustand eindeutig. Zustandswechsel: `image` per Binding auf die passende Datei umschalten, nicht über `animate` (siehe NIAGARA.md).

Flanschfarben: VL `#D7302B`, RL `#F29A38`. Reversibles Gerät mit einem Kreis neutral benennen, z. B. `WP01-SEK` (siehe Anlagenkennzeichnung im Styleguide).

### Absperrklappe Wasser

- Waagerecht: mit Antrieb 50 × 65, ohne Antrieb 50 × 30, Rohrachse y = 15 (`Absperrklappe_<Stellung>[_ohne_Antrieb]_waagerecht`).
- Senkrecht: mit Antrieb 65 × 50, ohne Antrieb 30 × 50, Rohrachse x = 15, Antrieb rechts (`..._senkrecht`).
- Stellungen: `neutral` (Scheibe schräg, grau), `auf` (waagerecht, grün `#2EAA3A`), `zu` (senkrecht, rot `#E0302A`).
- Endlagen-Marker 16 × 16: `Endlage_auf` (grün, waagerechter Strich), `Endlage_zu` (rot, senkrechter Strich).

### Energieventil

- 80 × 65 (rechts/links), 65 × 80 (oben/unten), Rohrachse 15.
- Ultraschall-Durchflusssensor stromaufwärts vor dem 2-Wege-Ventil, Antrieb unten bzw. rechts.
- Temperaturfühler als eigene Symbole.

### Zähler

Mit angedeutetem Rollenzählwerk (fünf Rollen, letzte rot).

- Wärmemengenzähler (rote Flamme), Kältemengenzähler (blaue Schneeflocke), Wasserzähler (blauer Tropfen): 60 × 65 waagerecht, 65 × 60 senkrecht, Rohrachse 15.
- Kombinierter Wärme-/Kältemengenzähler (`Waerme_Kaeltemengenzaehler_waagerecht` / `_senkrecht`): Flamme und Schneeflocke nebeneinander im Zählwerkkreis, gleiche Größe und Anschlüsse wie die Einzelzähler.
- Elektrozähler 50 × 60, Rollenzählwerk mit sechs Stellen oben, gelber Blitz unten.

### Pumpe

- 40 × 40, Kreis mit Förderpfeil (Dreieck `#4D4D4D`). Erzeugt mit `tools/pumpe.py`.
- `Pumpe_{richtung}_{zustand}`, Richtungen `oben`, `rechts`, `unten`, `links` (Dreieck fest gedreht, Niagara dreht nicht).

| Zustand | Suffix | Darstellung |
|---|---|---|
| aus | `_aus` | grau (`#EDEDED` → `#A6A6A6`) |
| Freigabe | `_freigabe` | gelb (`#FFEB8F` → `#E3B200`), pulsiert weich (1,4 s) |
| Betrieb | `_an` | grün (`#A8DC96` → `#3E9A3A`), drei lange Segmente drehen, Fließpfeile laufen im Dreieck Richtung Spitze |
| Störung | `_stoerung` | rot (`#F5A3A0` → `#D7302B`), pulsiert weich (1,4 s), kleines Warndreieck mit „!“ in der Mitte |

Animation per SMIL. Ohne Animation bleibt die Zustandsfarbe (und bei Störung das Warndreieck) sichtbar. Zustandswechsel über `image`-Binding (siehe NIAGARA.md).

## Anzeigen

### LEDs (flache Version)

- 32 × 32 inkl. Lichtschein, LED selbst ca. 21 px.
- Zustände: `aus`, `gruen`, `rot`, `blau`, `gelb`.
- Ring dezent hellgrau, gleichmäßige Linsenfarbe, kleiner Glanzpunkt.
- Umschalten über Binding auf `image` eines einzigen Pictures.
- Variante `_animiert` (z. B. `LED_gruen_animiert`, nicht für `aus`): Glanzpunkt blitzt alle 4 s kurz auf (SMIL). Ohne Animation identisch mit der statischen LED.

### LEDs eckig

- 32 × 32 inkl. Lichtschein, Kachel 24 × 24 mit Eckenradius 6, Verlauf hell → Farbe → dunkel, Glanzstreifen oben, schwacher eckiger Farbschein.
- `LED_eckig_{gruen,rot,blau,gelb,aus}`, dazu `_animiert` für die farbigen (Glanzstreifen blitzt alle 4 s kurz auf).
- `aus` ohne Farbschein.

### Punkte (dezent blinkend)

- 12 × 12, kleiner Punkt mit Glanzlicht, z. B. vor Temperaturanzeigen.
- `Punkt_{gruen,blau,gelb,rot}_blinkend`: Füllung wechselt weich Grau `#9A9A9A` → Farbe → Grau (SMIL, 3,5 s). Ohne Animation grau.
- `Punkt_grau`: statisch, für „aus“.
- Farbe per Binding auf `image` umschalten.

### Betriebsart Normal / Leise (z. B. Wärmepumpe)

- 40 × 40, eigenständiges Symbol zum Danebenlegen (Zustand der Wärmepumpe bleibt davon getrennt).
- Vier Motive, je `_normal` und `_leise`, statisch und als `_animiert`:

| Motiv | Normal | Leise |
| --- | --- | --- |
| `Betriebsart_Lautsprecher` | drei grüne Schallbögen | ein kleiner blauer Bogen |
| `Betriebsart_Pegel` | vier grüne Pegelbalken | ein blauer Balken, Rest als Umriss |
| `Betriebsart_SonneMond` | Sonne (dreht langsam) | Mond mit schwebendem „Z“ (Nachtbetrieb) |
| `Betriebsart_Luefter` | Lüfter schnell, zwei Schallbögen | Lüfter langsam, ein blasser Bogen |

- Farben: Normal `#2ECC40`, Leise `#4A86D4`.
- Umschalten über Binding (Boolean oder Enum) auf `image` eines Pictures.

## Fun

Verspielte Cartoon-Symbole unter `symbole/fun/`, 48 × 48, dunkelbraune Kontur `#3B2412`, animiert per SMIL. Zum Danebenstellen von Messwerten.

| Symbol | Dateien | Vorschlag Umschaltung |
|---|---|---|
| Außentemperatur | `Fun_Thermometer_kalt` (zittert, Schal), `_mild` (lächelt), `_warm` (Sonnenbrille, schwitzt) | kalt < 5 °C, mild 5–25 °C, warm > 25 °C |
| Außenfeuchte | `Fun_Tropfen_trocken` (durstig), `_normal` (hüpft), `_nass` (Schnorchel) | trocken < 35 %RH, normal 35–70 %RH, nass > 70 %RH |
| Außen-CO₂ | `Fun_CO2_Blase` (Schrift als Pfad) | – |

Umschalten über `image`-Binding mit Konverter (siehe NIAGARA.md).

### Buttons

Unter `symbole/fun/button/`, 280 × 72, Cartoon-Stil passend zu den Fun-Symbolen. Beschriftung als Pfad (kein `<text>`).

- `btn_{uebersicht,heizung,waermepumpe,puffer,pv,raeume}_{normal,aktiv}`: mit Icon und Beschriftung. „Räume“ ist aus Buchstaben der anderen Buttons zusammengesetzt (R = P mit ergänztem Bein).
- `btn_leer_{normal,aktiv}`: ohne Icon und Text, für eigene Beschriftung per Niagara-Label.
- `normal` gelb, `aktiv` orange mit hellem Rand und 3 px nach unten versetzt (gedrückt).
- `btn_welle_{fliesst,atmet,punkte,funken}`: 280 × 20, animierte Wellenlinie unter einem `normal`-Button als Alternative zu `aktiv`. `fliesst` und `atmet` verformen die Linie (SMIL `animate d`, im Browser geprüft, Workbench ungeprüft), `punkte` und `funken` bewegen nur Punkte.
