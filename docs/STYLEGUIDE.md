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

`<Symbol>_<Richtung/Variante>.svg`, Umlaute ausgeschrieben (ae, oe, ue), z. B. `Klimakonvektor_rechts.svg`, `Absperrklappe_auf_ohne_Antrieb.svg`, `Zortstroem_Heizung_stehend.svg`.

## SVG-Regeln

- Verläufe sind unkritisch.
- Kein `<text>`; Beschriftung und Werte als Niagara-Label.
- Einfache Formen bevorzugen, `pattern` vermeiden.
- `clipPath` wurde in Niagara noch nicht umfassend geprüft; bei Darstellungsfehlern hier zuerst ansetzen.
- Zu jedem SVG eine gleichnamige PNG als Ausweichlösung.

## Anlagenkennzeichnung (Heizen/Kälte)

- Kreise mit **H** (Heizen) und **K** (Kälte) kennzeichnen, nicht die Maschine.
- Wärmepumpe/Kältemaschine mit beiden Seiten: `WP01` (Gerät), `WP01-H` (Kondensatorseite), `WP01-K` (Verdampferseite), darunter `-VL`/`-RL`.
- Reversible Wärmepumpe mit einem Kreis: neutral benennen, z. B. `WP01-SEK`.
- Vermeiden: `HK` (= Heizkreis) und `H/K` (Schrägstrich ist in Niagara-Namen problematisch).
