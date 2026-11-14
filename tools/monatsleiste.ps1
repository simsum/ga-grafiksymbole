# Erzeugt symbole/fun/Fun_Monatsleiste.svg (Windows, PowerShell 5.1, Schrift Segoe Print fett).
# Aufruf: powershell -ExecutionPolicy Bypass -File tools/monatsleiste.ps1 -OutFile symbole/fun/Fun_Monatsleiste.svg
param([string]$OutFile)
Add-Type -AssemblyName PresentationCore
$inv = [Globalization.CultureInfo]::InvariantCulture
$monate = @('Januar','Februar',("M" + [char]0xE4 + "rz"),'April','Mai','Juni','Juli','August','September','Oktober','November','Dezember')
$farbe  = @('#5C5CA8','#5D66CC','#6E74C8','#4FAE62','#68B67C','#7ABE8A','#B5875C','#B08E94','#A3A3AB','#8150A0','#A458C0','#A879C0')
$tf = New-Object Windows.Media.Typeface((New-Object Windows.Media.FontFamily('Segoe Print')), [Windows.FontStyles]::Normal, [Windows.FontWeights]::Bold, [Windows.FontStretches]::Normal)
$gtf = $null
if (-not $tf.TryGetGlyphTypeface([ref]$gtf)) { throw 'Segoe Print fett nicht gefunden' }

function Shade([string]$hex, [double]$f) {
  $n = [Convert]::ToInt32($hex.Substring(1), 16)
  $rgb = @((($n -shr 16) -band 255), (($n -shr 8) -band 255), ($n -band 255))
  $o = foreach ($x in $rgb) { if ($f -gt 0) { [int][Math]::Round($x + (255 - $x) * $f) } else { [int][Math]::Round($x * (1 + $f)) } }
  '#{0:X2}{1:X2}{2:X2}' -f $o[0], $o[1], $o[2]
}
function Rund([string]$s) { [regex]::Replace($s, '-?\d+\.\d+', { param($m) ([Math]::Round([double]::Parse($m.Value, $inv), 2)).ToString($inv) }) }

$segW = 1188 / 12
# einheitliche Schriftgroesse: so gross, dass der laengste Name in sein Feld passt
$groesse = 19.0
for ($k = 0; $k -lt 12; $k++) {
  $probe = New-Object Windows.Media.FormattedText($monate[$k], $inv, [Windows.FlowDirection]::LeftToRight, $tf, 19.0, [Windows.Media.Brushes]::Black)
  $platz = if ($k -eq 0 -or $k -eq 11) { 76.0 } else { 86.0 }
  $groesse = [Math]::Min($groesse, 19.0 * $platz / $probe.Width)
}
$defs = ''; $segs = ''; $seps = ''; $txt = ''
for ($i = 0; $i -lt 12; $i++) {
  $col = $farbe[$i]
  $defs += "<linearGradient id=`"m$i`" x1=`"0`" y1=`"0`" x2=`"0`" y2=`"1`"><stop offset=`"0`" stop-color=`"$(Shade $col 0.45)`"/><stop offset=`".5`" stop-color=`"$col`"/><stop offset=`"1`" stop-color=`"$(Shade $col -0.3)`"/></linearGradient>`n    "
  $x = 4 + $i * $segW
  $xs = $x.ToString('0.##', $inv); $ws = ($segW + 0.5).ToString('0.##', $inv)
  $segs += "<rect x=`"$xs`" y=`"4`" width=`"$ws`" height=`"52`" fill=`"url(#m$i)`"/>`n    "
  if ($i -gt 0) {
    if ($i % 3 -eq 0) { $seps += "<line x1=`"$xs`" y1=`"4`" x2=`"$xs`" y2=`"56`" stroke=`"#2b1600`" stroke-width=`"4`"/>`n    " }
    else { $seps += "<line x1=`"$xs`" y1=`"4`" x2=`"$xs`" y2=`"56`" stroke=`"#2b1600`" stroke-width=`"1.5`" opacity=`".55`"/>`n    " }
  }
  $ft = New-Object Windows.Media.FormattedText($monate[$i], $inv, [Windows.FlowDirection]::LeftToRight, $tf, $groesse, [Windows.Media.Brushes]::Black)
  $mitte = $x + $segW / 2
  if ($i -eq 0) { $mitte += 4 } elseif ($i -eq 11) { $mitte -= 4 }
  $ox = $mitte - $ft.Width / 2
  $oy = 37 - $ft.Baseline
  $geo = $ft.BuildGeometry((New-Object Windows.Point($ox, $oy)))
  $pg = [Windows.Media.PathGeometry]::CreateFromGeometry($geo)
  $d = Rund ($pg.ToString($inv) -replace '^F[01]', '')
  $txt += "<path d=`"$d`"/>`n    "
}

$svg = @"
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 64" width="1200" height="64">
  <!-- Monatsleiste im Fun-Button-Stil, Schrift Segoe Print fett als Pfade -->
  <defs>
    $defs<clipPath id="kapsel"><rect x="4" y="4" width="1188" height="52" rx="20"/></clipPath>
  </defs>
  <rect x="6" y="9" width="1188" height="52" rx="20" fill="#1a0d00" opacity=".45"/>
  <g clip-path="url(#kapsel)">
    $segs$seps</g>
  <path d="M28,11 H1172" stroke="#ffffff" stroke-width="4" stroke-linecap="round" opacity=".45"/>
  <g fill="#2b1600">
    $txt</g>
  <rect x="4" y="4" width="1188" height="52" rx="20" fill="none" stroke="#2b1600" stroke-width="5"/>
</svg>
"@
[IO.File]::WriteAllText($OutFile, $svg, (New-Object Text.UTF8Encoding($false)))
"ok $((Get-Item $OutFile).Length) Bytes"

