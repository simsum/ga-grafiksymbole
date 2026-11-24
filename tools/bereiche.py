#!/usr/bin/env python3
"""Erzeugt dezente Trennlinien, Bereichsflächen und einen hellen Seitenhintergrund unter symbole/allgemein/bereiche/.

Zum optischen Gliedern einer Px-Seite (z. B. Bereich Wärmepumpe | Bereich Puffer). Alle Dateien mit
transparentem Hintergrund (außer dem Seitenhintergrund), halbtransparente Farben, damit sie auf hellen und
grauen Hintergründen funktionieren.

  Trennlinie_<Design>_<Länge>_{waagerecht,senkrecht}
      8 px stark, Linie mittig (y bzw. x = 4); Längen 120, 240, 360, 480, 600.
      Designs:
        Rille          dunkle + helle 1-px-Linie übereinander (eingeprägt)
        RilleVerlauf   wie Rille, an den Enden weich auslaufend
        VerlaufHell    weiße Linie, Enden weich
        VerlaufDunkel  graue Linie, Enden weich
        gestrichelt    grau, Striche 8 / Lücke 5
        punktiert      runde Punkte im Abstand 7
        Doppel         zwei feine graue Linien
        Band           heller weicher Streifen mit feiner Mittellinie
  Bereich_{hell,dunkel,Kopfzeile}_<B>x<H>
      Fläche hinter einem Anlagenteil, Ecken r = 10. Kopfzeile: oben 30 px abgesetzter Streifen für ein Titel-Label.
  Hintergrund_hell_1920x1080
      ruhiger Seitenhintergrund #EEF0F2 → #DDE1E5 (senkrecht), frei skalierbar.

Bausteine für Übersichts- und Legendenseiten (ohne Text, Beschriftung als Niagara-Label):
  Variante „Karten“: Hintergrund_hell + Titelband + je Kategorie eine Karte
  Titelband_dunkel_1920x54
      dunkles Band (#2B3138, wie Kopfzeile_dunkel) mit blauer Unterkante, frei skalierbar.
  Karte_Kopfzeile_<B>x<H>
      helle Karte mit leichtem Schatten und 30 px Kopfstreifen für die Kategorie-Überschrift, Ecken r = 10.
  Variante „Rahmen“: dunkler Rahmen mit heller Arbeitsfläche, Kategorien als Reiter
  Hintergrund_Rahmen_dunkel_<B>x<H>
      dunkler Verlauf, oben 50 px Platz für den Seitentitel, darunter helle Arbeitsfläche (Rand 14 px, r = 12).
  Reiter_<farbe>_<B>
      Kategorie-Reiter 26 px hoch, abgerundet, Farbe 15 % Fläche / 60 % Kontur. Spaltentrenner: Trennlinie_gestrichelt_*_senkrecht.

Aufruf: python tools/bereiche.py
"""
from pathlib import Path

ZIEL = Path(__file__).resolve().parent.parent / "symbole" / "allgemein" / "bereiche"
D = 8
LAENGEN = (120, 240, 360, 480, 600)
GROESSEN = ((240, 240), (300, 400), (400, 300), (400, 600), (600, 400), (800, 500))
DUNKEL, HELL = "#5A5A5A", "#FFFFFF"


def verlauf(gid: str, farbe: str, op: float) -> str:
    """Längsverlauf mit weichen Enden (12 % je Seite). objectBoundingBox auf <rect>, daher auch gedreht korrekt."""
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="{farbe}" stop-opacity="0"/><stop offset="0.12" stop-color="{farbe}" stop-opacity="{op}"/>'
            f'<stop offset="0.88" stop-color="{farbe}" stop-opacity="{op}"/><stop offset="1" stop-color="{farbe}" stop-opacity="0"/></linearGradient>')


def design(name: str, L: int) -> tuple[str, str]:
    """(defs, Zeichnung) für eine waagerechte Linie der Länge L, Mitte y = 4."""
    if name == "Rille":
        return "", (f'<rect x="0" y="3" width="{L}" height="1" fill="{DUNKEL}" fill-opacity="0.45"/>'
                    f'<rect x="0" y="4" width="{L}" height="1" fill="{HELL}" fill-opacity="0.6"/>')
    if name == "RilleVerlauf":
        return verlauf("vd", DUNKEL, 0.5) + verlauf("vh", HELL, 0.65), (
            f'<rect x="0" y="3" width="{L}" height="1" fill="url(#vd)"/>'
            f'<rect x="0" y="4" width="{L}" height="1" fill="url(#vh)"/>')
    if name == "VerlaufHell":
        return verlauf("vh", HELL, 0.75), f'<rect x="0" y="3.25" width="{L}" height="1.5" fill="url(#vh)"/>'
    if name == "VerlaufDunkel":
        return verlauf("vd", "#4D4D4D", 0.5), f'<rect x="0" y="3.25" width="{L}" height="1.5" fill="url(#vd)"/>'
    if name == "gestrichelt":
        return "", (f'<line x1="1" y1="4" x2="{L}" y2="4" stroke="{DUNKEL}" stroke-opacity="0.5" stroke-width="1.5" '
                    f'stroke-dasharray="8 5"/>')
    if name == "punktiert":
        return "", (f'<line x1="2" y1="4" x2="{L - 1}" y2="4" stroke="{DUNKEL}" stroke-opacity="0.5" stroke-width="2.4" '
                    f'stroke-linecap="round" stroke-dasharray="0 7"/>')
    if name == "Doppel":
        return "", (f'<rect x="0" y="2" width="{L}" height="1" fill="{DUNKEL}" fill-opacity="0.4"/>'
                    f'<rect x="0" y="5" width="{L}" height="1" fill="{DUNKEL}" fill-opacity="0.4"/>')
    if name == "Band":
        return verlauf("vb", HELL, 0.28) + verlauf("vd", DUNKEL, 0.4), (
            f'<rect x="0" y="0" width="{L}" height="8" rx="4" fill="url(#vb)"/>'
            f'<rect x="0" y="3.5" width="{L}" height="1" fill="url(#vd)"/>')
    raise ValueError(name)


DESIGNS = ("Rille", "RilleVerlauf", "VerlaufHell", "VerlaufDunkel", "gestrichelt", "punktiert", "Doppel", "Band")


def trennlinie(name: str, L: int, achse: str) -> str:
    defs, body = design(name, L)
    if achse == "waagerecht":
        w, h = L, D
    else:  # an der Diagonalen gespiegelt, wie Trennung_*_senkrecht
        w, h, body = D, L, f'<g transform="matrix(0 1 1 0 0 0)">{body}</g>'
    defs = f"<defs>{defs}</defs>" if defs else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
            f'  <!-- Trennlinie {name}, Länge {L}, {achse}, Linie mittig -->\n  {defs}{body}\n</svg>\n')


def bereich(art: str, w: int, h: int) -> str:
    kopf = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n  <!-- Bereichsfläche {art}, {w} × {h} -->\n  '
    if art == "hell":
        s = (f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="10" fill="#FFFFFF" fill-opacity="0.22" '
             f'stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="1.2"/>')
    elif art == "dunkel":
        s = (f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="10" fill="#000000" fill-opacity="0.07" '
             f'stroke="#000000" stroke-opacity="0.15" stroke-width="1.2"/>'
             f'<rect x="2.2" y="2.2" width="{w - 4.4:g}" height="{h - 4.4:g}" rx="9" fill="none" stroke="#FFFFFF" '
             f'stroke-opacity="0.35" stroke-width="1"/>')
    else:  # Kopfzeile
        s = (f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="10" fill="#FFFFFF" fill-opacity="0.55" '
             f'stroke="#B9BFC6" stroke-width="1.2"/>'
             f'<path d="M1,30 V11 a10,10 0 0 1 10,-10 H{w - 11} a10,10 0 0 1 10,10 V30 Z" fill="#5E6873" fill-opacity="0.12"/>'
             f'<line x1="1" y1="30" x2="{w - 1}" y2="30" stroke="#B9BFC6" stroke-width="1"/>')
    return kopf + s + "\n</svg>\n"


def hintergrund() -> str:
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080" preserveAspectRatio="none">\n'
            '  <!-- Heller Seitenhintergrund, frei skalierbar -->\n'
            '  <defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EEF0F2"/>'
            '<stop offset="1" stop-color="#DDE1E5"/></linearGradient></defs>\n'
            '  <rect width="1920" height="1080" fill="url(#g)"/>\n</svg>\n')


KARTEN_B = (240, 300)
KARTEN_H = (300, 400, 500, 600, 800)
RAHMEN = ((1920, 1080), (1280, 800), (1024, 768))
REITER_B = (160, 200, 240)
REITER_FARBEN = {"gruen": "#6BB33A", "blau": "#2E6BC2", "orange": "#F29A38", "rot": "#D7302B", "gelb": "#E3B200", "grau": "#808080"}


def titelband() -> str:
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="54" viewBox="0 0 1920 54" preserveAspectRatio="none">\n'
            '  <!-- Titelband dunkel (wie Kopfzeile_dunkel), frei skalierbar -->\n'
            '  <rect width="1920" height="54" fill="#2B3138"/><rect y="51" width="1920" height="3" fill="#4A86D4"/>\n</svg>\n')


def karte(w: int, h: int) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
            f'  <!-- Karte mit Kopfstreifen (30 px), {w} × {h} -->\n'
            f'  <rect x="3" y="3" width="{w - 4}" height="{h - 4}" rx="10" fill="#000000" fill-opacity="0.07"/>'
            f'<rect x="1" y="1" width="{w - 4}" height="{h - 4}" rx="10" fill="#FFFFFF" fill-opacity="0.88" stroke="#C8CDD2" stroke-width="1.2"/>'
            f'<path d="M1,31 V11 a10,10 0 0 1 10,-10 H{w - 13} a10,10 0 0 1 10,10 V31 Z" fill="#E4E8EC"/>'
            f'<line x1="1" y1="31" x2="{w - 3}" y2="31" stroke="#C8CDD2" stroke-width="1"/>\n</svg>\n')


def rahmen(w: int, h: int) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
            f'  <!-- Seitenhintergrund mit dunklem Rahmen und heller Arbeitsfläche, {w} × {h}; Titel oben links (y 0–50) -->\n'
            '  <defs><linearGradient id="gR" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A3F46"/><stop offset="1" stop-color="#262A30"/></linearGradient>'
            '<linearGradient id="gF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FAFBFC"/><stop offset="1" stop-color="#E9EDF1"/></linearGradient></defs>\n'
            f'  <rect width="{w}" height="{h}" fill="url(#gR)"/><rect y="0" width="{w}" height="2" fill="#4A86D4"/>'
            f'<rect x="14" y="50" width="{w - 28}" height="{h - 64}" rx="12" fill="url(#gF)"/>\n</svg>\n')


def reiter(farbe: str, w: int) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="28" viewBox="0 0 {w} 28">\n'
            f'  <!-- Kategorie-Reiter {w} × 28 -->\n'
            f'  <rect x="1" y="1" width="{w - 2}" height="26" rx="13" fill="{farbe}" fill-opacity="0.15" stroke="{farbe}" stroke-opacity="0.6" stroke-width="1.2"/>\n</svg>\n')


def schreib(name: str, inhalt: str) -> None:
    with open(ZIEL / name, "w", encoding="utf-8", newline="\n") as f:
        f.write(inhalt)


def main() -> None:
    ZIEL.mkdir(parents=True, exist_ok=True)
    n = 0
    for d in DESIGNS:
        for L in LAENGEN:
            for achse in ("waagerecht", "senkrecht"):
                schreib(f"Trennlinie_{d}_{L}_{achse}.svg", trennlinie(d, L, achse))
                n += 1
    for art in ("hell", "dunkel", "Kopfzeile"):
        for w, h in GROESSEN:
            schreib(f"Bereich_{art}_{w}x{h}.svg", bereich(art, w, h))
            n += 1
    schreib("Hintergrund_hell_1920x1080.svg", hintergrund())
    n += 1
    # Bausteine für Übersichts-/Legendenseiten
    schreib("Titelband_dunkel_1920x54.svg", titelband())
    n += 1
    for w in KARTEN_B:
        for h in KARTEN_H:
            schreib(f"Karte_Kopfzeile_{w}x{h}.svg", karte(w, h))
            n += 1
    for w, h in RAHMEN:
        schreib(f"Hintergrund_Rahmen_dunkel_{w}x{h}.svg", rahmen(w, h))
        n += 1
    for name, farbe in REITER_FARBEN.items():
        for w in REITER_B:
            schreib(f"Reiter_{name}_{w}.svg", reiter(farbe, w))
            n += 1
    print(f"{n} Dateien in {ZIEL}")


if __name__ == "__main__":
    main()
