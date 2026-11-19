# Symbolkatalog

Geplante und vorhandene Symbole mit Abmessungen und Anschlusspunkten. Alle Koordinaten in px, bezogen auf die linke obere Ecke des Bildes.

Status: Das Repository enthält die Symbole unter `symbole/` (nur SVG, Schrift als Pfad). Übersichtsgrafiken mit Hinweisen: [uebersicht/](uebersicht/). Die Tabellen beschreiben die Vorgaben. Das Volumenstromregler-Rund-Set heißt `Volumenstromregler_rund_*`, liegende Schichtspeicher `Schichtspeicher_*_liegend`.

## Allgemein

Fachübergreifende Symbole (Wasser, Luft, Strom) unter `symbole/allgemein/flusspfeile/` und `symbole/allgemein/trennung/`.

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
- `Trennung_<Länge>_{waagerecht,senkrecht}` mit Länge 60, 120, 180, 240, 300 px (waagerecht L × 16, senkrecht 16 × L).
- Ohne Zusatz hell (`#C8C8D0`, für dunkle Hintergründe), `_dunkel` (`#555555`, für helle Hintergründe).
- Nicht verzerrt skalieren: passende Länge wählen, damit die Schraffur gleichmäßig bleibt.

### Aufstellplatten (`symbole/allgemein/aufstellung/`)

3D-angedeutete Aufstellflächen, die in Px unter stehende Geräte gelegt werden (Pufferspeicher, Schichtspeicher, Kessel …). Alle 180 × 30, transparenter Hintergrund, Kontur `#5A5A5A` wie die Speicher, ohne `clipPath`.

| Symbol | Darstellung |
|---|---|
| `Aufstellplatte_Beton` | Rechteckiger Betonsockel: helle Oberseite in Perspektive, dunklere Vorderkante |
| `Aufstellplatte_rund` | Rundes Podest: ovale Oberseite, zylindrischer Mantel, passt zu runden Speichern |
| `Aufstellplatte_Stahl` | Flache Stahlplatte mit zwei Schraubenköpfen und weichem Kontaktschatten |

- Aufstellpunkt: Die Füße stehen bei y = 9 (Mitte der Oberseite).
- Platzierung unter einem 144 px breiten Speicher (z. B. `Pufferspeicher_WT_stehend`): Platte bei x = x<sub>Speicher</sub> − 18, y = y<sub>Speicher</sub> + 336 − 9 (Fußunterkante des Speichers bei y = 336). Die Platte liegt in Px **unter** dem Speicher (zuerst einfügen).
- Erzeugt mit `tools/aufstellplatten.py`.

### Bereiche (`symbole/allgemein/bereiche/`)

Zum optischen Gliedern einer Px-Seite, z. B. Bereich Wärmepumpe | Bereich Puffer. Halbtransparent, damit sie auf dem bisherigen grauen und auf hellen Hintergründen funktionieren. Nicht zu verwechseln mit `Trennung_*` (Wand-/Deckendurchführung).

**Trennlinien** `Trennlinie_<Design>_<Länge>_{waagerecht,senkrecht}`: Längen 120, 240, 360, 480, 600; 8 px stark (waagerecht L × 8, senkrecht 8 × L), Linie mittig. Hinter die Symbole legen. Wegen der Strich- und Punktmuster passende Länge wählen statt verzerrt zu skalieren.

| Design | Darstellung |
|---|---|
| `Rille` | dunkle und helle 1-px-Linie übereinander, wirkt eingeprägt |
| `RilleVerlauf` | wie `Rille`, an den Enden weich auslaufend |
| `VerlaufHell` | weiße Linie (75 %), Enden weich |
| `VerlaufDunkel` | graue Linie (50 %), Enden weich |
| `gestrichelt` | grau (50 %), Strich 8 / Lücke 5 |
| `punktiert` | runde Punkte im Abstand 7 |
| `Doppel` | zwei feine graue Linien |
| `Band` | heller, weicher Streifen mit feiner Mittellinie |

**Bereichsflächen** `Bereich_{hell,dunkel,Kopfzeile}_<B>x<H>`: 240x240, 300x400, 400x300, 400x600, 600x400, 800x500; Ecken r = 10. Als unterste Ebene hinter ein Anlagenteil legen.

| Art | Darstellung |
|---|---|
| `hell` | Weiß 22 %, heller Rand; hebt den Bereich auf dem grauen Hintergrund leicht an |
| `dunkel` | Schwarz 7 % mit heller Innenkante; wirkt eingelassen |
| `Kopfzeile` | Weiß 55 %, Rand `#B9BFC6`, oben 30 px abgesetzter Streifen für ein Titel-Label (z. B. „Wärmepumpe“); gedacht für den hellen Seitenhintergrund |

**Seitenhintergrund** `Hintergrund_hell_1920x1080`: ruhiger Verlauf `#EEF0F2` → `#DDE1E5` (senkrecht), frei skalierbar (`preserveAspectRatio="none"`). Alternativ dieselben Farben direkt als Hintergrund der Px-Seite setzen.

- Erzeugt mit `tools/bereiche.py`.

## Lüftung

| Symbol | Größe | Hinweise |
|---|---|---|
| Klimakonvektor (Kanalgerät, Draufsicht) | 160 × 90 (rechts/links), 90 × 160 (oben/unten) | Pfeil = Ausblasrichtung; zwei Radialventilatoren; Freifläche für Nummern-Label |
| Volumenstromregler rund | 140 × 80 / 80 × 140 | Rohr mit Flanschen, Klappe, Kompaktregler; links/oben gespiegelt, damit der Regler oben bzw. rechts sitzt |
| Volumenstromregler eckig | 140 × 80 / 80 × 140 | Rechteckkanal, drei gegenläufige Lamellen (zwei unter 40 px) |
| Deckenluftdurchlass rund (Hallen-Lochblech) | quadratisch | Kreis füllt die Bildfläche, ohne Stellhebel |
| WRG Kreuzstrom-Plattenwärmetauscher | 400 × 480 (im Schema ca. 331 × 399) | Kein Rahmen; Anschlüsse links/rechts bei y = 46,5 und y = 435,5, Kanalhöhe 24; Varianten mit/ohne Bypass |
| WRG mit Flanschen (`WRG_Platte_mit_Bypass_PlusMinus_Flansch`) | 400 × 480 | Wie oben, zusätzlich Flansch (6 × 34) an allen vier Anschlüssen ganz außen am Symbolrand; Kanäle enden am Flansch. Bestehender Kanal im Schema muss an der Flanschkante enden |
| Rotationswärmetauscher, Kanäle links/rechts (`WRG_Rotation_senkrecht_{aus,an,stoerung}`) | 80 × 400 | Rad von außen gesehen (Lauffläche), links leicht schräg die Stirnseite mit Speichen; Kanalachsen y = 60 (oben, Abluft/Fortluft) und y = 340 (unten, Außenluft/Zuluft), Kanäle 20 px setzen an der Gehäusekante x = 10 bzw. 70 an. Mittelsteg mit Nabe bei y = 200 |
| Rotationswärmetauscher, Kanäle oben/unten (`WRG_Rotation_waagerecht_{aus,an,stoerung}`) | 400 × 80 | Wie oben um 90° gedreht: Kanalachsen x = 60 und x = 340, Kanäle setzen an der Gehäusekante y = 10 bzw. 70 an |
| Rotationswärmetauscher, Vorderansicht (`WRG_Rotation_vorne_{aus,an,stoerung}`) | 180 × 180 | Rahmen, Rad mit acht Speichen, Kreuzsteg und Nabe; Gerätebild ohne Kanalanschluss |
| Klappe, ein Blatt, senkrecht/waagerecht (`lueftung/klappen/Klappe_klein_senkrecht_1_zu` bis `_5_auf`, `Klappe_klein_waagerecht_…`) | klein 30 × 60 / 60 × 30, groß 40 × 80 / 80 × 40 | Fünf Stellungen 1_zu, 2_25, 3_50, 4_75, 5_auf (Blattwinkel zur Kanalachse 90° / 67,5° / 45° / 22,5° / 0°); Kanal verläuft entlang der langen Seite; grau, Statusfarbe über Niagara. Abgeleitet von AC0531 und AC0532 (M, L); große Variante `Klappe_gross_senkrecht_…`, `Klappe_gross_waagerecht_…` |
| Klappe, drei Blätter, senkrecht/waagerecht (`Klappe_3blatt_klein_senkrecht_…`, `Klappe_3blatt_klein_waagerecht_…`, groß: `Klappe_3blatt_gross_…`) | klein 30 × 60 / 60 × 30, groß 40 × 80 / 80 × 40 | Drei Blätter, Blattlänge nimmt Richtung „auf“ ab. Abgeleitet von AC0511/AC0521 (senkrecht) und AC0512/AC0522 (waagerecht), M und L. Waagerechte Klappen kippen wie das Original AC0532 nach „\“, senkrechte nach „/“ |

Klappen: Blattwinkel zur Kanalachse, zu = quer, auf = längs. Die Klappen stammen aus der SBC-Icon-Galerie (Honeywell) und werden von `tools/klappen.py` erzeugt.

WRG-Luftwege: Außenluft oben links (grün) → Zuluft unten rechts (rot); Abluft oben rechts → Fortluft unten links (orange).

Rotationswärmetauscher: `_aus` Rad steht; `_an` Rad dreht (SMIL), Lamellen laufen perspektivisch über die Rundung, die Speichen der Stirnseite drehen mit, Pfeile zeigen die Drehrichtung; `_stoerung` Rad steht, rotes Warndreieck blinkt (1 Hz). Motor nicht eingezeichnet, dafür das M-Symbol daneben setzen. Erzeugt mit `tools/wrg_rotation.py`.

### Ventilatoren (`symbole/lueftung/ventilatoren/`)

- 60 × 60, aufgebaut wie die Pumpe: Kreis in Zustandsfarbe, statt des Dreiecks das Ventilatorzeichen (zwei Linien, die in Förderrichtung zusammenlaufen). Außenring und Linien immer grau `#808080`. Erzeugt mit `tools/ventilator.py`.
- `Ventilator_{richtung}_{zustand}`: Zustände und Animation wie bei der Pumpe (`_aus`, `_freigabe`, `_an`, `_an_punkte`, `_stoerung`); bei `_an` dreht der weiße Ring, helle Luftpfeile wandern zur engen Seite.
- `Ventilator_Fluegel_{richtung}_{zustand}`: statt des drehenden Rings ein angedeutetes Lüfterrad (drei helle Flügel), dreht bei `_an`; Luftpfeile und Punkte dunkel.
- Richtungen `oben`, `rechts`, `unten`, `links` (Förderrichtung, fest gedreht). Mittig auf die Kanalachse setzen.

### Filter (`symbole/lueftung/filter/`)

- `rechts`, `links`: 40 × 80 für waagerechte Kanäle, Kanalachse y = 40. `oben`, `unten`: 80 × 40 für senkrechte Kanäle, Kanalachse x = 40. Richtung = Strömungsrichtung. Erzeugt mit `tools/filter.py`.
- `Filter_<richtung>`: Luftfilter wie im bestehenden Anlagenbild, graues Gehäuse mit hellem Keil (Spitze in Strömungsrichtung); statisch.
- `Filter_Taschen_<richtung>`: Taschenfilter von vorn, Rahmen mit zwei Zellen übereinander, Stege zwischen den Taschen. Graue Staubteilchen fliegen von der Anströmseite heran und werden aufgefangen (SMIL).
- `_verschmutzt` (beide): Filterfläche bräunlich mit Schmutzflecken, Staub bleibt hängen, Filterfläche blinkt leicht gelb (`#E3B200`, 1 Hz wie Störung). Ohne Animation bleibt der verschmutzte Filter erkennbar.

### Kanalrauchmelder (`symbole/lueftung/rauchmelder/`)

- `Kanalrauchmelder_<lage>_<zustand>`: hellgraues, quadratisches Gehäuse (30 × 30) mit runder Messkammer in Zustandsfarbe (grauer fester Ring wie bei Pumpe und Ventilator), Messrohr mit Ansauglöchern ragt in den Kanal. Erzeugt mit `tools/kanalrauchmelder.py`.
- Lage = Seite des Kanals, auf der das Gerät sitzt. `oben`/`unten`: 48 × 50 für waagerechte Kanäle, Rohrende auf der Kanalmitte bei x = 24, y = 50 bzw. y = 0. `links`/`rechts`: 52 × 48 für senkrechte Kanäle, Rohrende bei x = 52 bzw. x = 0, y = 24.

| Zustand | Suffix | Darstellung |
|---|---|---|
| Normal | `_normal` | grün, statisch |
| Luftstrom in Ordnung | `_luftstrom` | grün, weißer Ring dreht, helle Punkte steigen im Messrohr zum Gehäuse |
| Wartung | `_wartung` | gelb, Kammer pulsiert weich (1,4 s) mit dunklem Warndreieck |
| Alarm | `_alarm` | rot, Kammer pulsiert schnell (0,6 s), Rauch quillt auf, Alarmwellen blinken (2 Hz) |
| Störung | `_stoerung` | rot wie alle Störungen, Kammer pulsiert weich (1,4 s) mit rotem Warndreieck |

## Hydraulik

### Umschaltventil-Pfeile

- 40 × 40, quadratisch einsetzen; Knick auf den Kreuzungspunkt der Rohrachsen.
- Richtungen: `links-oben`, `rechts-oben`, `oben-links`, `oben-rechts`.
- Farben: `rot`, `blau`, `grau`.
- Vorlaufventil: heizen `links-oben_rot`, kühlen `rechts-oben_blau`. Rücklaufventil: heizen `oben-links_rot`, kühlen `oben-rechts_blau`.

### Schichtspeicher liegend (`Schichtspeicher_{Heizung,Kaelte}_liegend[_beschriftet]`)

- Heizung 800 × 160 (6 Zonen A–F), Kälte 800 × 136 (5 Zonen A–E), Zonenhöhe 24.
- Zonenmitte y = Oberkante + 20 + 24 × (Zone − 1).
- Varianten ohne und mit Beschriftung.

### Schichtspeicher stehend (`Schichtspeicher_{Heizung,Kaelte}_stehend`)

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

### Gastherme (Wandgerät)

Wandhängende Gastherme, Vorderansicht, neutral gezeichnet, ohne Logos. Abgasstutzen oben mittig, drei Anschlüsse als angedeutete Flansche an der Unterkante. Zwei Darstellungen mit gleicher Größe und gleichen Anschlusspunkten:

- `Gastherme_vorne_*`: geschlossenes Gehäuse mit Schauglas (Brenner) und Bedienfeld.
- `Gastherme_Schnitt_vorne_*`: offenes Gehäuse mit Ausdehnungsgefäß, Wärmetauscher (Rohrwendel, Brennkammer), Gebläse, Gasventil und Leitungen innen.

| Symbol | Größe | Anschlusspunkte (x; y = Unterkante) |
|---|---|---|
| `Gastherme_vorne_aus` | 120 × 166 | VL 30, Gas 60, RL 90; y = 166 |
| `Gastherme_Schnitt_vorne_aus` | 120 × 166 | VL 30, Gas 60, RL 90; y = 166 |

| Zustand | Suffix | Darstellung |
|---|---|---|
| aus | `_aus` | Brenner aus, Status-LED grau |
| Betrieb | `_an` | Flammen flackern, Brennkammer glüht, im Schnitt dreht das Gebläse; Status-LED grün (SMIL) |
| Störung | `_stoerung` | rotes Warndreieck und rote Status-LED blinken (1 Hz) |

Flanschfarben: VL `#D7302B`, Gas `#F2C230`, RL `#2E6BC2`. Erzeugt mit `tools/gastherme.py`.

### Brennerflamme (animiert, zum Überlegen)

- `Brenner_Flamme_{links,rechts}_{1..5}_animiert`: 114 × 68, transparent, ohne Kessel. Alle zehn Dateien haben dieselbe Größe und dieselbe Wurzelposition, damit Niagara beim Umschalten nichts verschiebt.
- Fünf Flammenlängen (26, 46, 66, 86, 106 px ab Kesseltür) für Leistungsstufen; mit wachsender Länge wird die Flamme auch breiter. Bei Stufe 0 / Brenner aus Bild ausblenden.
- Aufbau aus fünf Schichten (rot, orange, gelb, hell, blauer Ansatz), Umriss flackert per SMIL (`animate d`); nur Verläufe und Deckkraft, keine Filter.
- `links`: Flamme zeigt nach rechts, über `Kessel_Brenner_links` legen; `rechts`: Flamme zeigt nach links, über `Kessel_Brenner_rechts`.
- Position relativ zur linken oberen Ecke des Kessel-Symbols (240 × 143): `links` bei x = 78, y = 52; `rechts` bei x = 48, y = 52. Die Flammenwurzel liegt dann an der Kesseltür (x = 82 bzw. 158) auf Brennerhöhe (y = 86).
- Statische Variante ohne Zusatz, `Brenner_Flamme_{links,rechts}_{1..5}` (gleiche Größe, ohne Animation), wenn SMIL nicht dargestellt wird oder Ruhe gewünscht ist.
- Erzeugt mit `tools/flamme.py`.

### Brennerrauch (animiert, zum Überlegen)

- `Brenner_Rauch_animiert`: 64 × 96, transparent, ein Symbol für beide Kessel. Sechs weiche graue Rauchwolken steigen versetzt vom Abgasstutzen auf, wachsen, schwanken leicht und blenden aus (SMIL, keine Filter). Zusammen mit der Flamme bei „Brenner an“ einblenden.
- Statische Variante ohne Zusatz, `Brenner_Rauch` (gleiche Größe, Wolken über die Aufstiegshöhe verteilt).
- Position relativ zur linken oberen Ecke des Kessel-Symbols (240 × 143): `Kessel_Brenner_links` bei x = 180, y = −92; `Kessel_Brenner_rechts` bei x = −4, y = −92. Die Mündung liegt im Symbol bei (32, 92), der Rauch ragt über die Oberkante des Kessels hinaus.
- Erzeugt mit `tools/rauch.py`.

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
| `Waermepumpe_Luft_Wasser_links_aus` | 180 × 168 | VL 20, RL 40; y = 168 |
| `Waermepumpe_Luft_Wasser_rechts_aus` | 180 × 168 | VL 160, RL 140; y = 168 |

Zustandsvarianten, jeweils für `links` und `rechts`, gleiche Größe und Anschlusspunkte:

| Zustand | Suffix | Darstellung |
|---|---|---|
| aus | `_aus` | Lüfter steht |
| Betrieb | `_an` | Lüfter dreht, Windlinien wandern von der Mitte nach außen; animiert per SMIL (läuft in 4.15 in Workbench und Browser) |
| Störung | `_stoerung` | Lüfter steht, rotes Warndreieck mit Ausrufezeichen und rote Status-LED blinken (1 Hz) |
| Abtaubetrieb | `_abtau` | Lüfter steht, Reif auf dem Lüfter, Schneeflocke, Schmelzwassertropfen, blaue Status-LED pulsiert |

Bei `_stoerung` und `_abtau` zeigt auch das Standbild (ohne Animation) den Zustand eindeutig. Zustandswechsel: `image` per Binding auf die passende Datei umschalten, nicht über `animate` (siehe NIAGARA.md).

Flanschfarben: VL `#D7302B`, RL `#F29A38`. Reversibles Gerät mit einem Kreis neutral benennen, z. B. `WP01-SEK` (siehe Anlagenkennzeichnung im Styleguide).

### Absperrklappe Wasser

- Waagerecht: mit Antrieb 50 × 65, ohne Antrieb 50 × 30, Rohrachse y = 15 (`Absperrklappe[_ohneAntrieb]_waagerecht_<Stellung>`).
- Senkrecht: mit Antrieb 65 × 50, ohne Antrieb 30 × 50, Rohrachse x = 15, Antrieb rechts (`Absperrklappe[_ohneAntrieb]_senkrecht_<Stellung>`).
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

- 40 × 40, Kreis mit Förderpfeil (Dreieck). Außenring und Dreieck immer grau `#808080`, nur die Füllung zeigt den Zustand. Erzeugt mit `tools/pumpe.py`.
- `Pumpe_{richtung}_{zustand}`, Richtungen `oben`, `rechts`, `unten`, `links` (Dreieck fest gedreht, Niagara dreht nicht).

| Zustand | Suffix | Darstellung |
|---|---|---|
| aus | `_aus` | grau (`#EDEDED` → `#A6A6A6`) |
| Freigabe | `_freigabe` | gelb (`#FFEB8F` → `#E3B200`), Füllung pulsiert weich (1,4 s), Ring bleibt fest |
| Betrieb | `_an` | grün (`#A8DC96` → `#3E9A3A`), drei lange Segmente drehen, Fließpfeile laufen im Dreieck Richtung Spitze |
| Betrieb, Fließpunkte | `_an_punkte` | wie `_an`, statt der Fließpfeile laufen drei helle Punkte in einer Spur zur Spitze (wie bei `Flusspfeil_*_an`) |
| Störung | `_stoerung` | rot (`#F5A3A0` → `#D7302B`), Füllung pulsiert weich (1,4 s), kleines Warndreieck mit „!“ in der Mitte |

Animation per SMIL. Ohne Animation bleibt die Zustandsfarbe (und bei Störung das Warndreieck) sichtbar. Zustandswechsel über `image`-Binding (siehe NIAGARA.md).

### Anschlüsse (`symbole/hydraulik/anschluesse/`)

Einzelne Flanschanschlüsse zum Anlegen an Geräte oder Leitungen, alle 24 × 24, Rohrbreite 12 px.

| Symbol | Darstellung |
|---|---|
| `Flansch_Geraet_<farbe>_<richtung>` | Geräteflansch wie an der Wärmepumpe: grauer Hals (6 × 5) an der Gerätekante, farbige Flanschplatte (16 × 6) |
| `Flansch_Platte_<achse>` | einzelne graue Flanschplatte (18 × 5) quer zur Rohrachse |
| `Flansch_Paar_<achse>` | zwei graue Flanschplatten mit Schrauben, Rohrverbindung in der Leitung |

- `<richtung>` = Seite, zu der das Rohr abgeht: `unten`, `oben`, `links`, `rechts`. Bei `unten` liegt die Gerätekante bei y = 5, das Rohr setzt mittig bei y = 16 an (x = 12); die anderen Richtungen sind um die Mitte (12, 12) gedreht.
- `<achse>` = Richtung der Rohrachse: `senkrecht` oder `waagerecht`. Die Rohrachse läuft durch die Mitte (12, 12); die Platten werden über das Rohr gelegt.
- Farben (`<farbe>`) wie die Flansche an Wärmepumpe und Mehrleitermaschine:

| Farbe | Wert | Verwendung |
|---|---|---|
| `rot` | `#D7302B` | Heizung Vorlauf |
| `orange` | `#F29A38` | Heizung Rücklauf |
| `blau` | `#2E6BC2` | Kälte Vorlauf |
| `hellblau` | `#7CA6DE` | Kälte Rücklauf |
| `gruen` | `#6BB33A` | Kaltwasser |
| `grau` | `#9A9A9A` | neutral |

- Grauteile `#8C8C8C`, Kontur `#6B6B6B` (1 px), bei den Fun-Flanschen gleich. Erzeugt mit `tools/flansche.py`.

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

### Freigabe (`symbole/anzeigen/freigabe/`)

- 24 × 24, klein und unaufdringlich, statisch, zum Danebenlegen an Pumpen, Ventile, Erzeuger.
- Farben nach Styleguide „Zustandsfarben“: `_an` = Freigabe (gelb), `_aus` = keine Freigabe (grau).
- Fünf Varianten, je `_an` und `_aus`:

| Variante | Freigabe (`_an`) | keine Freigabe (`_aus`) |
| --- | --- | --- |
| `Freigabe_Haken` | runder Knopf mit weißem Haken | weißer Strich |
| `Freigabe_Schalter` | Kippschalter, Knopf rechts | Knopf links |
| `Freigabe_Schloss` | Schloss offen | Schloss zu |
| `Freigabe_Ein` | Ein-Symbol | Ein-Symbol grau |
| `Freigabe_Punkt` | Punkt mit Ring | Punkt mit Ring grau, am dezentesten |

- Umschalten über Boolean-Binding auf `image`. Erzeugt mit `tools/freigabe.py`.

## Fun

Verspielte Cartoon-Symbole unter `symbole/fun/` (Gruppen wie in der Hauptstruktur: `anzeigen/`, `hydraulik/pumpen/`, `hydraulik/speicher/`, `navigation/`), 48 × 48, dunkelbraune Kontur `#3B2412`, animiert per SMIL. Zum Danebenstellen von Messwerten.

**Zeichensatz Fun:** Beschriftungen im Fun-Stil (Buttons, Monatsleiste) verwenden **Chewy** (Google Fonts, Apache License 2.0, [github.com/google/fonts/tree/main/apache/chewy](https://github.com/google/fonts/tree/main/apache/chewy)).

- Darstellung wie auf den Buttons: helle Füllung `#fffbe6`, darunter dieselbe Form als braune Kontur `#2b1600` (Buttons 5 px, Monatsleiste 4 px), `stroke-linejoin="round"`.
- Immer als Pfad, nie als `<text>`. Umwandeln mit fonttools wie in `tools/monatsleiste.py`; die Schriftdatei wird nicht eingecheckt (Download nach `tools/.schriften/`).
- Bei den Buttons wurde die Schrift nachträglich durch Vergleich der Buchstabenformen bestimmt; „Räume“ ist dort aus Buchstaben der anderen Buttons zusammengesetzt.

| Symbol | Dateien | Vorschlag Umschaltung |
|---|---|---|
| Außentemperatur | `Fun_Thermometer_kalt` (zittert, Schal), `_mild` (lächelt), `_warm` (Sonnenbrille, schwitzt) | kalt < 5 °C, mild 5–25 °C, warm > 25 °C |
| Außenfeuchte | `Fun_Tropfen_trocken` (durstig), `_normal` (hüpft), `_nass` (Schnorchel) | trocken < 35 %RH, normal 35–70 %RH, nass > 70 %RH |
| Außen-CO₂ | `Fun_CO2_Blase` (Schrift als Pfad) | – |
| Pufferspeicher | `Fun_Pufferspeicher_WT_stehend` (Cartoon-Variante von `hydraulik/speicher/Pufferspeicher_WT_stehend`, liegt in `fun/hydraulik/speicher/`, gleiche Größe) | – |

Umschalten über `image`-Binding mit Konverter (siehe NIAGARA.md).

### Fun-Gastherme (`symbole/fun/hydraulik/erzeuger/`)

- `Fun_Gastherme_vorne_{aus,an,stoerung}_animiert`: 120 × 166, gleiche Größe und Anschlusspunkte wie `Gastherme_vorne_*` (VL 30, Gas 60, RL 90; y = 166), daher per `image`-Binding austauschbar.
- Gehäuse, Bedienfeld und Flansche wie die normale Gastherme; die Frontplatte bekommt ein Gesicht, das Schauglas sitzt darunter.
- `_aus`: Augen zu, „Zzz“ steigt auf, Schauglas dunkel. `_an`: große Augen (blinzeln), Lächeln, Bäckchen, Flammen flackern, LED grün. `_stoerung`: X-Augen, Zickzack-Mund, Therme wackelt, Rauch steigt auf, Warndreieck im Schauglas, rote LED blinkt.
- Ohne Animation bleiben Gesicht und Zustandsanzeigen sichtbar. Erzeugt mit `tools/fun_gastherme.py` (baut auf `tools/gastherme.py` und `tools/fun_waermepumpe.py` auf).

### Fun-Pumpen

- `Fun_Pumpe_{oben,rechts,unten,links}_{aus,freigabe,an,stoerung}`: 40 × 40, gleiche Größe, Richtungen und Zustandsfarben wie die Pumpen unter `symbole/hydraulik/pumpen/`, daher per `image`-Binding austauschbar. Pumpensymbol mit demselben grauen Außenring und grauen Förderdreieck wie die normale Pumpe (Effekte kräftig dunkel umrandet `#3B2412`), dazu eine kleine Animation (SMIL).
- Das Förderdreieck zeigt in allen Zuständen die Förderrichtung, wie bei den Standard-Pumpen.
- `_aus`: zwei „z“ steigen auf. `_freigabe`: Funken blinken. `_an`: blaue Wasserblasen wandern über das Dreieck in Förderrichtung (Blasen nur im Betrieb). `_stoerung`: Pumpe wackelt, Dampfwolken steigen auf, Schweißperlen spritzen ab, Warndreieck in der Mitte.
- Erzeugt mit `tools/fun_pumpe.py` (baut auf `tools/pumpe.py` auf). Ohne Animation bleibt das Symbol mit allen Effekten sichtbar.

### Fun-Flansche, undicht (`symbole/fun/hydraulik/anschluesse/`)

- `Fun_Flansch_Geraet_<richtung>_undicht_animiert`, `Fun_Flansch_Platte_<achse>_undicht_animiert`, `Fun_Flansch_Paar_<achse>_undicht_animiert`: dieselben Formen wie die normalen Flansche (grau, Kontur `#6B6B6B` wie die normalen).
- An der tiefsten Kante bildet sich ein Wassertropfen, fällt nach unten und zerplatzt (SMIL, 2,4 s, Tropfen immer senkrecht nach unten, unabhängig von der Richtung).
- 24 × 36: oben deckungsgleich mit den normalen 24 × 24-Symbolen, darunter 12 px Platz für den Tropfen. Damit lassen sie sich an derselben Position gegen die normalen Flansche tauschen (z. B. bei Leckage-Meldung).
- Ohne Animation hängt ein kleiner Tropfen an der Kante. Erzeugt mit `tools/flansche.py`.

### Fun-Wärmepumpe (`symbole/fun/hydraulik/erzeuger/`)

- `Fun_Waermepumpe_Luft_Wasser_{rechts,links}_{aus,an,stoerung,abtau}_animiert`: 180 × 168, gleiche Größe und Anschlusspunkte wie `Waermepumpe_Luft_Wasser_*`, daher per `image`-Binding austauschbar.
- Gehäuse wie die normale Wärmepumpe (graue Konturen); der Lüfter wird zum Gesicht (Nabe = Nase), Gesichtszüge weiß mit brauner Außenkontur.

| Zustand | Gesicht | Animation |
| --- | --- | --- |
| `_aus` | Augen zu, schläft | „Zzz“ steigt auf |
| `_an` | große Augen (blinzeln), Lächeln, Bäckchen | Lüfter dreht, Windlinien |
| `_stoerung` | X-Augen, Zickzack-Mund | Gerät wackelt, Rauch steigt aus dem Lüfter, Warndreieck im Schaltkasten, rote LED blinkt |
| `_abtau` | besorgte Augen, Zähneklappern | Gerät zittert, Eiszapfen, Reif auf dem Lüfter, Schneeflocke im Schaltkasten, blaue LED |

- Ohne Animation bleiben Gesicht und Zustandsanzeigen sichtbar. Erzeugt mit `tools/fun_waermepumpe.py` (baut auf `tools/waermepumpe.py` auf).

### Monatsleiste

- `Fun_Monatsleiste`: 1200 × 64, statisch, Stil der Fun-Buttons (Kontur `#2b1600`, Glanzstreifen, Schatten, abgerundete Enden).
- Zwölf gleich breite Monatsfelder (je 99 px, Leiste x = 4 … 1192), Jahreszeitenfarben: Winter blau-violett, Frühling grün, Sommer braun bis grau, Herbst lila. Dicke Trennstriche zwischen den Quartalen.
- Monatsnamen in der Schrift der Fun-Buttons (Chewy, Google Fonts, Apache License 2.0), helle Füllung `#fffbe6` mit brauner Kontur wie auf den Buttons, als Pfade (kein `<text>`, unabhängig von installierten Schriften).
- Für den Jahresfortschritt einen Balken (z. B. kitPx-Bargraph, 0–365) mit gleicher Breite darunterlegen.
- Erzeugt mit `tools/monatsleiste.py` (benötigt fonttools; lädt `Chewy-Regular.ttf` beim ersten Aufruf nach `tools/.schriften/`, alternativ `--schrift <Pfad>`).

### Buttons

Unter `symbole/fun/navigation/`, 280 × 72, Cartoon-Stil passend zu den Fun-Symbolen. Beschriftung als Pfad (kein `<text>`).

- `Fun_Button_{Uebersicht,Heizung,Waermepumpe,Puffer,PV,Raeume}_{normal,aktiv}`: mit Icon und Beschriftung. „Räume“ ist aus Buchstaben der anderen Buttons zusammengesetzt (R = P mit ergänztem Bein).
- `Fun_Button_Leer_{normal,aktiv}`: ohne Icon und Text, für eigene Beschriftung per Niagara-Label.
- `normal` gelb, `aktiv` orange mit hellem Rand und 3 px nach unten versetzt (gedrückt).
- `Fun_Button_Welle_{fliesst,atmet,punkte,funken}`: 280 × 20, animierte Wellenlinie unter einem `normal`-Button als Alternative zu `aktiv`. `fliesst` und `atmet` verformen die Linie (SMIL `animate d`, im Browser geprüft, Workbench ungeprüft), `punkte` und `funken` bewegen nur Punkte.
