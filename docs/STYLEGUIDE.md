# Stilvorgaben

## Allgemein

- Eher flach als plastisch, dezente Verläufe.
- Keine Nummern oder Beschriftungen im Symbol; die kommen als Niagara-Labels darüber. Beschriftete Varianten nur zusätzlich.
- Keine Herstellerlogos, neutrale Darstellung.
- Anschlüsse nur als angedeuteter Flansch, keine farbigen Leitungsstummel (Ausnahme: WRG, deren Kanäle nahtlos an bestehende Kanäle anschließen; zusätzlich gibt es die WRG-Variante `_Flansch` mit Flansch an den Anschlüssen).
- Symbole mit Richtung in allen vier Richtungen.
- Übergänge zu Rohren und Kanälen passen in Farbe, Breite und Profil.
- Symbole einer Familie sind gleich groß.

## Ventilstil (Hydraulik)

| Element | Wert |
|---|---|
| Körperverlauf (vertikal) | `#E6E6E6` → `#E0E0E0` (7 %) → `#999999` |
| Körperkontur | `#999999`, 2–2,4 px |
| Antriebs-/Rechenwerkkreis | r = 15,8, Füllung `#F2F2F2`, Kontur `#808080` 2,4 px |
| „M“ und dunkle Elemente | `#666666` |
| Rohrachse | y = 15 (waagerecht) bzw. x = 15 (senkrecht) |

## Rohr- und Kanalfarben

| Medium | Randfarbe |
|---|---|
| Außenluft (grün) | `#94C652` |
| Ab-/Fortluft (orange) | `#FF9A30` |
| Zuluft / Heizung Vorlauf (rot) | `#F04F46` |
| Wasser / Kälte (blau) | ca. `#4A86D4` |

**Profil:** kräftige Randfarbe, zur Mitte fast weiß (`#F4F4F4`). Nachbau in SVG mit vier übereinanderliegenden Strichen: Breite 100 % / 75 % / 50 % / 22 %, Aufhellung 0 / 0,35 / 0,65 / 0,92.

**Breiten:** Wasserrohre ca. 12 px, Luftkanäle ca. 20 px (24 px bei der WRG in 400 × 480-Auslegung).

## Pfeile

| Pfeil | Farbe | Rand |
|---|---|---|
| Flusspfeile auf Rohren | `#2A2A2A` | weiß, 70 % Deckkraft, 1 px |
| Umschaltpfeile heizen | `#E0463C` | weißer Halo 7 px |
| Umschaltpfeile kühlen | `#2F7FD8` | weißer Halo 7 px |
| Umschaltpfeile neutral | `#4D4D4D` | weißer Halo 7 px |

## Blauer Stil (Umluft-/Luftsymbole)

Hauptfarbe `#4B50E6`, Hellfläche `#EEF0FF`, Hintergrund weiß.

## Zustandsfarben

Einheitlich für **alle** Symbole mit Betriebszustand (Pumpen, Fun-Pumpen, Freigabe-Anzeigen und alle neuen Symbole). Verlauf senkrecht von oben nach unten, dazu die Kontur. Die Werte stehen auch in `tools/zustandsfarben.py`; Erzeuger-Skripte importieren sie von dort, statt eigene Farben festzulegen.

| Zustand | Datei-Zusatz | Verlauf oben | Verlauf unten | Kontur |
|---|---|---|---|---|
| Aus / keine Freigabe (grau) | `_aus` | `#EDEDED` | `#A6A6A6` | `#808080` |
| Freigabe / bereit (gelb) | `_freigabe` | `#FFEB8F` | `#E3B200` | `#A88400` |
| Betrieb / an (grün) | `_an` | `#A8DC96` | `#3E9A3A` | `#2F7A2C` |
| Störung (rot) | `_stoerung` | `#F5A3A0` | `#D7302B` | `#9E1F1B` |

- Bei Freigabe-Anzeigen steht `_an` für „Freigabe“ (gelb) und `_aus` für „keine Freigabe“ (grau).
- Weiße Elemente (Haken, Schalterknopf, Ein-Symbol) bleiben weiß, dunkle Details nehmen die Kontur des Zustands.
- LEDs und Punkte (`anzeigen/led`, `anzeigen/punkte`), Betriebsart „normal“ (`anzeigen/betriebsart`) und das Warndreieck der Wärmepumpe nutzen die Zustandsfarben ebenfalls: Verläufe mit oben, unten und Kontur, volle Flächen mit „Verlauf unten“.
- Bewusst eigene Töne: Blau (LED und Punkt blau, Betriebsart „leise“, Abtaubetrieb der Wärmepumpe), Sonne/Mond und die Flamme der Wärmemengenzähler (`#E0302A`). Kein Zustand im Schema.
- Noch eigene Zustandstöne, bisher nicht angeglichen: Absperrklappe und Endlage auf/zu (`#2EAA3A` / `#E0302A`, hier bedeutet Rot „zu“ und nicht Störung), Warndreieck der Pumpen und Fun-Pumpen (`#E2231A`, `tools/pumpe.py`).
- Ausnahme Pumpen, Fun-Pumpen und Ventilatoren: Außenring und Förderzeichen (Dreieck bzw. Linien) bleiben in allen Zuständen grau (`#808080`), nur die Füllung trägt die Zustandsfarbe und pulsiert bei Freigabe und Störung; der Ring pulsiert nicht mit (siehe „Pumpen und Ventilatoren“).

## Pumpen und Ventilatoren

Gleich aufgebaut, gleiche Zustände und Animationen. Pumpen 40 × 40, Ventilatoren 60 × 60 (beide im 40er-Raster gezeichnet, viewBox `0 0 40 40`).

| Element | Wert |
|---|---|
| Förderdreieck (Pumpe) | immer grau `#808080` |
| Ventilatorzeichen | zwei Linien von Kreisrand zu Kreisrand, laufen in Förderrichtung zusammen (DIN EN 12792) |
| Linien (Ventilator) | immer grau `#808080`, 1,4 px |
| Außenring | immer grau `#808080`, 1,6 px; pulsiert nicht mit |
| Füllung | Zustandsverlauf; bei Freigabe und Störung pulsiert nur die Füllung |
| Betrieb (`_an`) | weißer Ring mit drei Segmenten dreht wie bei der Pumpe |
| Fließ-/Luftpfeile (`_an`) | hell `#E6E6E6`; Pumpe: im Dreieck zur Spitze, Ventilator: zur engen Seite |
| Variante `Fluegel` (Ventilator) | statt des drehenden Rings drei angedeutete Lüfterflügel (Weiß 50 %, Rand Weiß 75 %) mit Nabe hinter den Linien; drehen nur bei `_an`. Luftpfeile und Punkte hier dunkel `#4D4D4D` |

## Flanschfarben

Angedeutete Geräteflansche (`tools/flansche.py`, Wärmepumpe, Gastherme, Mehrleitermaschine):

| Anschluss | Farbe |
|---|---|
| Heizung Vorlauf | `#D7302B` (rot) |
| Heizung Rücklauf | `#F29A38` (orange); bei der Gastherme `#2E6BC2` (blau) |
| Kälte Vorlauf / Rücklauf | `#2E6BC2` / `#7CA6DE` |
| Gas | `#F2C230` (gelb) |
| Kaltwasser | `#6BB33A` (grün) |
| neutral | `#9A9A9A` |

Reihenfolge an der Gastherme von links: Vorlauf, Gas, Rücklauf.

## Detailstufen

Falls feste Größen nötig sind (lange Seite): 20, 30, 40, 50, 60, 80, 100, 120 px. Mindest-Strichstärken 1,2 px (Konturen) und 0,8 px (Details). Unter 60 px Detailraster entfernen, unter 40 px weiter vereinfachen. Mit `Picture` + `fitRatio` meist nicht nötig.

## Verzeichnisse

- Symbole liegen immer in einer Gruppe: `symbole/<Fachbereich>/<Gruppe>/`, bei Bedarf mit Untergruppe (z. B. `fun/hydraulik/pumpen/`). Direkt im Fachbereich liegen keine Dateien.
- Fachbereiche: `allgemein`, `lueftung`, `hydraulik`, `anzeigen`, `topologie`, `fun`. `fun` spiegelt die Gruppen der Hauptstruktur (`fun/anzeigen`, `fun/hydraulik/…`), dazu `fun/navigation`.
- Ordnernamen klein geschrieben, Mehrzahl oder Sammelbegriff, Umlaute ausgeschrieben (`klimageraete`, `luftdurchlaesse`, `zaehler`).
- Neue Gruppe anlegen, sobald eine Symbolfamilie nicht in eine bestehende passt. Eine Gruppe mit nur einem Symbol ist in Ordnung.

## Dateinamen

Schema: `Symbol[_Variante][_Größe]_Ausrichtung[_Zustand][_Zusatz].svg`

| Teil | Werte | Beispiel |
|---|---|---|
| Symbol | Gattungsbegriff, keine Produkt- oder Herstellernamen | `Absperrklappe`, `Schichtspeicher` |
| Variante | Bauart, Medium, Ansicht (mehrere Wörter in CamelCase) | `ohneAntrieb`, `3blatt`, `Heizung`, `Draufsicht` |
| Größe | `klein`/`gross`, `S`/`M`/`L`, Länge in px, Portzahl | `gross`, `120`, `16_Port` |
| Ausrichtung | `rechts`, `links`, `oben`, `unten` (Fluss-/Förderrichtung oder Anschlussseite); `waagerecht`, `senkrecht` (Rohr-/Kanalachse); `stehend`, `liegend` (Bauform) | `senkrecht` |
| Zustand | `aus`, `an`, `freigabe`, `stoerung`, `abtau`, `auf`, `zu`, `neutral`, `normal`, `aktiv`; Stufen als Zahl, Klappenstellungen `1_zu` … `5_auf` | `auf`, `3_50` |
| Zusatz | `animiert` (wenn es dieselbe Datei auch statisch gibt), `beschriftet`, `dunkel` | `animiert` |

- Umlaute ausgeschrieben (ae, oe, ue, ss), nur ASCII, Teile mit Unterstrich getrennt, keine Bindestriche oder Leerzeichen.
- Ausrichtung immer `waagerecht`/`senkrecht`, nie `horizontal`/`vertikal`.
- Gibt es Zustände, wird auch der Grundzustand benannt (`_aus`), nicht weggelassen.
- Fun-Symbole beginnen mit `Fun_`, Fun-Buttons mit `Fun_Button_`.
- Beispiele: `Klimakonvektor_rechts.svg`, `Absperrklappe_ohneAntrieb_senkrecht_auf.svg`, `Klappe_3blatt_gross_waagerecht_2_25.svg`, `Trennung_120_waagerecht_dunkel.svg`, `Waermepumpe_Luft_Wasser_links_aus.svg`, `Schichtspeicher_Heizung_liegend_beschriftet.svg`.

## SVG-Regeln

- Nur SVG, keine PNG- oder GIF-Dateien. Animationen als SVG (SMIL).
- Verläufe sind unkritisch.
- Kein `<text>`; Schrift immer nur als Pfad (auch in `_beschriftet`-Varianten und animierten SVGs). Werte und veränderliche Beschriftung als Niagara-Label.
- Einfache Formen bevorzugen, `pattern` vermeiden.
- `clipPath` wurde in Niagara noch nicht umfassend geprüft; bei Darstellungsfehlern hier zuerst ansetzen.
## Anlagenkennzeichnung (Heizen/Kälte)

- Kreise mit **H** (Heizen) und **K** (Kälte) kennzeichnen, nicht die Maschine.
- Wärmepumpe/Kältemaschine mit beiden Seiten: `WP01` (Gerät), `WP01-H` (Kondensatorseite), `WP01-K` (Verdampferseite), darunter `-VL`/`-RL`.
- Reversible Wärmepumpe mit einem Kreis: neutral benennen, z. B. `WP01-SEK`.
- Vermeiden: `HK` (= Heizkreis) und `H/K` (Schrägstrich ist in Niagara-Namen problematisch).
