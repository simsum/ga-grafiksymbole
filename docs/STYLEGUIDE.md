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

## Detailstufen

Falls feste Größen nötig sind (lange Seite): 20, 30, 40, 50, 60, 80, 100, 120 px. Mindest-Strichstärken 1,2 px (Konturen) und 0,8 px (Details). Unter 60 px Detailraster entfernen, unter 40 px weiter vereinfachen. Mit `Picture` + `fitRatio` meist nicht nötig.

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
