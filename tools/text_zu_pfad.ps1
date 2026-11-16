# Wandelt alle <text>-Elemente einer SVG-Datei in <path>-Elemente um (Schrift als Pfad).
# Windows, PowerShell 5.1 (WPF). Ausgewertet werden x, y (Grundlinie), text-anchor, font-family,
# font-size, font-weight, font-style, fill und opacity. Verschachtelte <tspan> werden nicht unterstützt.
# Die erste installierte Schrift aus font-family wird verwendet (generische Namen wie sans-serif -> Arial).
# Aufruf: powershell -ExecutionPolicy Bypass -File tools/text_zu_pfad.ps1 symbole/ordner/Datei.svg [weitere.svg ...]
param([Parameter(Mandatory = $true, ValueFromRemainingArguments = $true)][string[]]$Dateien)
Add-Type -AssemblyName PresentationCore
$inv = [Globalization.CultureInfo]::InvariantCulture
$generisch = @{ 'sans-serif' = 'Arial'; 'serif' = 'Times New Roman'; 'monospace' = 'Consolas' }

function Attr([string]$tag, [string]$name, [string]$standard) {
  $m = [regex]::Match($tag, "\s$([regex]::Escape($name))=`"([^`"]*)`"")
  if ($m.Success) { $m.Groups[1].Value } else { $standard }
}
function Zahl([string]$s) { [double]::Parse(($s -replace 'px$', ''), $inv) }
function Rund([string]$s) { [regex]::Replace($s, '-?\d+(\.\d+)?(E-?\d+)?', { param($m) ([Math]::Round([double]::Parse($m.Value, $inv), 2)).ToString($inv) }) }

function Schrift([string]$familien, [string]$gewicht, [string]$stil) {
  $w = if ($gewicht -in 'bold', 'bolder', '600', '700', '800', '900') { [Windows.FontWeights]::Bold } else { [Windows.FontWeights]::Normal }
  $s = if ($stil -eq 'italic') { [Windows.FontStyles]::Italic } else { [Windows.FontStyles]::Normal }
  foreach ($f in ($familien -split ',')) {
    $name = $f.Trim().Trim("'", '"')
    if ($generisch.ContainsKey($name)) { $name = $generisch[$name] }
    $tf = New-Object Windows.Media.Typeface((New-Object Windows.Media.FontFamily($name)), $s, $w, [Windows.FontStretches]::Normal)
    $gtf = $null
    if ($tf.TryGetGlyphTypeface([ref]$gtf)) { return $tf }
  }
  throw "Keine der Schriften '$familien' ist installiert."
}

foreach ($datei in $Dateien) {
  $pfad = (Resolve-Path $datei).Path
  $svg = [IO.File]::ReadAllText($pfad)
  $anzahl = 0
  $neu = [regex]::Replace($svg, '<text\b([^>]*)>([^<]*)</text>', {
    param($m)
    $tag = $m.Groups[1].Value
    $inhalt = [Net.WebUtility]::HtmlDecode($m.Groups[2].Value)
    $tf = Schrift (Attr $tag 'font-family' 'Arial') (Attr $tag 'font-weight' 'normal') (Attr $tag 'font-style' 'normal')
    $groesse = Zahl (Attr $tag 'font-size' '16')
    $ft = New-Object Windows.Media.FormattedText($inhalt, $inv, [Windows.FlowDirection]::LeftToRight, $tf, $groesse, [Windows.Media.Brushes]::Black)
    $x = Zahl (Attr $tag 'x' '0'); $y = Zahl (Attr $tag 'y' '0')
    switch (Attr $tag 'text-anchor' 'start') { 'middle' { $x -= $ft.WidthIncludingTrailingWhitespace / 2 } 'end' { $x -= $ft.WidthIncludingTrailingWhitespace } }
    $geo = $ft.BuildGeometry((New-Object Windows.Point($x, ($y - $ft.Baseline))))
    $d = Rund ([Windows.Media.PathGeometry]::CreateFromGeometry($geo).ToString($inv) -replace '^F[01]', '')
    $extra = ''
    foreach ($a in 'fill', 'opacity', 'fill-opacity', 'transform') { $v = Attr $tag $a $null; if ($v) { $extra += " $a=`"$v`"" } }
    $script:anzahl++
    "<!-- Text: $($inhalt -replace '--', '- -') --><path d=`"$d`"$extra/>"
  })
  [IO.File]::WriteAllText($pfad, $neu, (New-Object Text.UTF8Encoding($false)))
  "$datei : $anzahl Text(e) in Pfade umgewandelt"
}
