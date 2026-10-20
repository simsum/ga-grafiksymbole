# Einbindung in Niagara Px

Getestet mit Niagara 4.15.

## Picture statt Label

Symbole gehören in ein `Picture` (`ui:Picture`), nicht in ein `Label`: Ein Bild in der `image`-Eigenschaft eines Labels wird immer in Originalgröße angezeigt.

Wichtige Eigenschaften: `image`, `scale`, `animate`, `halign`, `valign`, `layout`, `visible`.

Mit `scale = fitRatio` wird das Bild auf die Layoutgröße skaliert und behält sein Seitenverhältnis. Pro Symbol genügt daher ein SVG.

Im Px-Quelltext (Rechtsklick auf die .px-Datei → *Views* → *Text Editor*):

```xml
<Picture layout="x,y,b,h" image="file:^px/GraphicTemplates/symbole/Datei.svg" scale="fitRatio"/>
```

Ablageort der Dateien in der Station: `file:^px/GraphicTemplates/symbole/`.

## Positionierung

Layout = Zielpunkt − halbe Symbolgröße.

Beispiel: Pfeil 56 × 56 auf einer Rohrkreuzung bei (885, 400) → `857, 372, 56, 56`.

## Zustandswechsel

Die Eigenschaft `image` per Binding an einen Zustand koppeln. So genügt ein `Picture` statt mehrerer übereinanderliegender (z. B. LEDs, Klappenstellungen).

## Beschriftung

- Die Symbole enthalten keinen Text. Bezeichnungen und Werte als Label darüberlegen.
- Zeilenumbruch im Label: im Px-Quelltext `&#10;` einsetzen, z. B. `text="-4-&#10;Nikolaus"`. Über das Property Sheet geht es nicht.
- `wordWrapEnabled = true` bricht nur an Leerzeichen um.
- Labels lassen sich nicht drehen. Workaround: Text als Bild oder gestapelte Buchstaben über `&#10;`.

## Animation

| Technik | Bewertung |
|---|---|
| Zustandsbilder umschalten (Binding auf `image`) | sicher, überall lauffähig |
| Animiertes GIF (`animate = true`) | echte Bewegung; Pixelgrafik, harte Transparenz, in Anzeigegröße erzeugen |
| Animiertes SVG (CSS/SMIL) | ob Workbench/HTML5-Ansicht es abspielt, ist ungeprüft |

## Hinweise zu SVG

- Kein `<text>`.
- Verläufe funktionieren.
- `clipPath` ist nicht umfassend geprüft.
- Für maximale Kompatibilität einfache Formen verwenden.
