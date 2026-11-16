# ga-grafiksymbole

Freie SVG-Symbole für Px-Grafiken der Gebäudeautomation (Niagara 4) – Lüftung, Heizung, Kälte, Hydraulik und Anzeigen.

Die Symbole sind für den Einsatz in Niagara Px als `Picture` mit `scale = fitRatio` gedacht. Alle Symbole liegen ausschließlich als SVG vor, auch die animierten (SMIL); Schrift ist immer als Pfad gezeichnet.

## Inhalt

```
symbole/                 nur SVG-Dateien, immer in symbole/<Fachbereich>/<Gruppe>/
  allgemein/             Fachübergreifend (Wasser, Luft, Strom)
    flusspfeile/         Flusspfeile gerade und mit Bogen
    trennung/            Trennung/Durchführung (Decke, Wand)
  lueftung/
    klimageraete/        Klimakonvektor
    luftdurchlaesse/     Deckenluftdurchlass
    volumenstromregler/  Volumenstromregler rund und eckig
    wrg/                 Wärmerückgewinnung (Plattenwärmetauscher)
    klappen/             Lüftungsklappen (ein und drei Blätter, klein und groß) in fünf Stellungen
  hydraulik/
    armaturen/           Absperrklappe, Energieventil, Endlagen
    pumpen/              Pumpen in vier Richtungen und vier Zuständen
    erzeuger/            Kessel, Brenner (Flamme, Rauch), Wärmepumpe, Mehrleitermaschine
    speicher/            Pufferspeicher, Schichtspeicher
    zaehler/             Wärme-, Kälte-, Wasser- und Elektrozähler
  anzeigen/
    led/                 LEDs rund und eckig, statisch und animiert
    punkte/              Dezent blinkende Punkte
    betriebsart/         Betriebsart Normal/Leise
  fun/                   Verspielte Cartoon-Symbole, animiert, Gruppen wie in der Hauptstruktur
    anzeigen/            Außentemperatur, -feuchte, CO₂
    hydraulik/pumpen/    Fun-Pumpen
    hydraulik/speicher/  Fun-Pufferspeicher
    navigation/          Navigationsbuttons 280 × 72 (normal/aktiv), Monatsleiste
  topologie/
    automation/          Controller, I/O-Module, GLT-Leitrechner
    netzwerk/            Ethernet-Switches
    schaltschraenke/     Schaltschränke
    feldgeraete/         Energieventile, Energie- und Wasserzähler
    geraete/             Allgemeine Geräte
docs/
  STYLEGUIDE.md          Farben, Strichstärken, Proportionen
  NIAGARA.md             Einbindung in Px, Positionierung, Fallstricke
  SYMBOLKATALOG.md       Abmessungen und Anschlusspunkte je Symbol
  uebersicht/            Übersichtsgrafik je Symbolgruppe (SVG, animierte Symbole laufen mit)
tools/
  check_symbols.py       Prüft symbole/ auf Regeln (nur SVG, kein <text>, Namensschema)
  text_zu_pfad.ps1       Wandelt <text> in einer SVG in Pfade um (Windows)
  pumpe.py               Erzeugt die Pumpensymbole unter symbole/hydraulik/pumpen/
  rauch.py               Erzeugt den Brennerrauch unter symbole/hydraulik/erzeuger/ (animiert + statisch)
  flamme.py              Erzeugt die Brennerflammen unter symbole/hydraulik/erzeuger/ (animiert + statisch)
  fun_pumpe.py           Erzeugt die Fun-Pumpen unter symbole/fun/hydraulik/pumpen/ (baut auf pumpe.py auf)
  waermepumpe.py         Erzeugt die Wärmepumpen-Symbole unter symbole/hydraulik/erzeuger/
  klappen.py             Erzeugt die Klappensymbole unter symbole/lueftung/klappen/
  monatsleiste.py        Erzeugt symbole/fun/navigation/Fun_Monatsleiste.svg (Schrift Chewy als Pfade, fonttools)
  zip_erstellen.py       Packt symbole/ und LICENSE in dist/ga-grafiksymbole.zip (von der Action genutzt)
  uebersichten.py        Erzeugt die Übersichtsgrafiken in docs/uebersicht/ aus den SVGs (ohne Zusatzpakete)
```

## Download

Alle Symbole inklusive Verzeichnisstruktur als ein Archiv:
[ga-grafiksymbole.zip](https://github.com/simsum/ga-grafiksymbole/releases/latest/download/ga-grafiksymbole.zip)
(aktueller Stand, siehe auch [Releases](https://github.com/simsum/ga-grafiksymbole/releases)). Das Archiv enthält den Ordner `symbole/` und die Lizenz.

Es wird bei jeder Änderung an `symbole/` automatisch von einer GitHub Action gebaut (`.github/workflows/zip.yml`) und liegt als Anhang am Release `latest`, nicht im Repository.

## Übersicht der Symbole

Jede Grafik zeigt alle Symbole einer Gruppe mit Dateinamen und Größe. Die Symbole sind direkt eingebettet, animierte Symbole bewegen sich daher auch hier (im Browser; die GitHub-App zeigt je nach Version nur ein Standbild).

### Allgemein – `symbole/allgemein`

**Flusspfeile** (`flusspfeile`)
![Flusspfeile](docs/uebersicht/Uebersicht_allgemein_flusspfeile.svg)

**Trennung** (`trennung`)
![Trennung](docs/uebersicht/Uebersicht_allgemein_trennung.svg)

### Lüftung – `symbole/lueftung`

**Klimageräte** (`klimageraete`)
![Klimageräte](docs/uebersicht/Uebersicht_lueftung_klimageraete.svg)

**Luftdurchlässe** (`luftdurchlaesse`)
![Luftdurchlässe](docs/uebersicht/Uebersicht_lueftung_luftdurchlaesse.svg)

**Volumenstromregler** (`volumenstromregler`)
![Volumenstromregler](docs/uebersicht/Uebersicht_lueftung_volumenstromregler.svg)

**Wärmerückgewinnung** (`wrg`)
![WRG](docs/uebersicht/Uebersicht_lueftung_wrg.svg)

**Klappen** (`klappen`)
![Klappen](docs/uebersicht/Uebersicht_lueftung_klappen.svg)

### Hydraulik – `symbole/hydraulik`

**Armaturen** (`armaturen`)
![Armaturen](docs/uebersicht/Uebersicht_hydraulik_armaturen.svg)

**Pumpen** (`pumpen`)
![Pumpen](docs/uebersicht/Uebersicht_hydraulik_pumpen.svg)

**Erzeuger** (`erzeuger`)
![Erzeuger](docs/uebersicht/Uebersicht_hydraulik_erzeuger.svg)

**Speicher** (`speicher`)
![Speicher](docs/uebersicht/Uebersicht_hydraulik_speicher.svg)

**Zähler** (`zaehler`)
![Zähler](docs/uebersicht/Uebersicht_hydraulik_zaehler.svg)

### Anzeigen – `symbole/anzeigen`

**LEDs** (`led`)
![LEDs](docs/uebersicht/Uebersicht_anzeigen_led.svg)

**Punkte** (`punkte`)
![Punkte](docs/uebersicht/Uebersicht_anzeigen_punkte.svg)

**Betriebsart** (`betriebsart`)
![Betriebsart](docs/uebersicht/Uebersicht_anzeigen_betriebsart.svg)

### Fun – `symbole/fun`

**Anzeigen** (`anzeigen`)
![Fun-Anzeigen](docs/uebersicht/Uebersicht_fun_anzeigen.svg)

**Pumpen** (`hydraulik/pumpen`)
![Fun-Pumpen](docs/uebersicht/Uebersicht_fun_hydraulik_pumpen.svg)

**Speicher** (`hydraulik/speicher`)
![Fun-Speicher](docs/uebersicht/Uebersicht_fun_hydraulik_speicher.svg)

**Navigation** (`navigation`)
![Fun-Navigation](docs/uebersicht/Uebersicht_fun_navigation.svg)

### Topologie – `symbole/topologie`

**Automation: Controller, I/O-Module, Leitrechner** (`automation`)
![Automation](docs/uebersicht/Uebersicht_topologie_automation.svg)

**Netzwerk** (`netzwerk`)
![Netzwerk](docs/uebersicht/Uebersicht_topologie_netzwerk.svg)

**Allgemeine Geräte** (`geraete`)
![Geräte](docs/uebersicht/Uebersicht_topologie_geraete.svg)

**Feldgeräte: Energieventile, Energie- und Wasserzähler** (`feldgeraete`)
![Feldgeräte](docs/uebersicht/Uebersicht_topologie_feldgeraete.svg)

**Schaltschränke** (`schaltschraenke`)
![Schaltschränke](docs/uebersicht/Uebersicht_topologie_schaltschraenke.svg)

## Verwendung in Niagara

1. SVG-Dateien nach `file:^px/GraphicTemplates/symbole/` in der Station kopieren.
2. In Px ein `Picture` anlegen, `image` auf die Datei setzen, `scale = fitRatio`.
3. Beschriftungen und Werte als Niagara-Label darüberlegen (die Symbole enthalten bewusst keinen Text).

Details: [docs/NIAGARA.md](docs/NIAGARA.md).

## Konventionen

- Keine Texte, Nummern oder Herstellerlogos in den Symbolen.
- Symbole mit Richtung gibt es in allen vier Richtungen.
- Symbole einer Familie haben identische Abmessungen.
- Dateinamen: `Symbol[_Variante][_Größe]_Ausrichtung[_Zustand][_Zusatz].svg`, nur Unterstriche (Niagara mag keine Bindestriche), Umlaute ausgeschrieben, z. B. `Klimakonvektor_rechts.svg`, `Absperrklappe_ohneAntrieb_senkrecht_auf.svg`. Details im [Styleguide](docs/STYLEGUIDE.md#dateinamen).
- Bestehende Symbole werden nur nach Rückfrage umbenannt, da Px-Seiten auf die Dateinamen verweisen. Frühere Umbenennungen stehen in [docs/MIGRATION.csv](docs/MIGRATION.csv) (alter Pfad;neuer Pfad).

Siehe [docs/STYLEGUIDE.md](docs/STYLEGUIDE.md) und [CONTRIBUTING.md](CONTRIBUTING.md).

## Haftung und Marken

Die Symbole sind eigenständig gezeichnet und neutral gehalten. „Niagara“, „Honeywell“ und weitere genannte Namen sind Marken ihrer jeweiligen Inhaber. Dieses Projekt steht in keiner Verbindung zu diesen Unternehmen und enthält keine Dateien aus deren Symbolbibliotheken. Bezeichnungen wie „Honeywell-Stil“ beschreiben nur die visuelle Anmutung.

Die Nutzung erfolgt auf eigene Verantwortung, ohne Gewähr.

## Lizenz

[Creative Commons Namensnennung 4.0 International (CC BY 4.0)](LICENSE)

Die Symbole dürfen frei genutzt, verändert und weitergegeben werden, auch kommerziell, wenn die Urheberschaft genannt wird, zum Beispiel: „Symbole: Sven Steinmeier, https://github.com/simsum/ga-grafiksymbole, CC BY 4.0“. Änderungen sind kenntlich zu machen.
