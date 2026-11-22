param(
    [Parameter(Mandatory)] [string] $Version,
    [string] $Python = 'python'
)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true
$root = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$launcherDir = Join-Path $root 'launcher'
$source = Join-Path $launcherDir 'bbport_launcher_win.py'
$versionLine = Select-String -LiteralPath $source -Pattern "^VERSION = '([^']+)'$"
if ($versionLine.Matches[0].Groups[1].Value -ne $Version) {
    throw "The release version $Version does not match the Windows launcher."
}
& $Python -c 'import sys; assert sys.version_info[:2] == (3, 14) and sys.platform == "win32"'

$output = Join-Path $root "out/private-server-release/$Version"
New-Item -ItemType Directory -Force -Path $output | Out-Null
$work = Join-Path $output 'work'
$dist = Join-Path $output 'dist'
$check = Join-Path $root 'packaging/windows/check_launcher_runtime.py'
$hidden = foreach ($module in @('argparse', 'base64', 'bisect', 'collections', 'contextlib', 'hashlib', 'json',
                                're', 'shutil', 'struct', 'tempfile', 'xml.etree.ElementTree', 'urllib.request',
                                'ctypes.wintypes')) {
    '--hidden-import'
    $module
}

& $Python -m PyInstaller --noconfirm --log-level WARN --console --name launcher-runtime-check `
    --workpath $work --specpath $work --distpath $dist --paths $launcherDir $check
& $Python -m PyInstaller --noconfirm --log-level WARN --windowed --name Bloodborne `
    --workpath $work --specpath $work --distpath $dist --paths (Join-Path $root 'scripts') @hidden `
    --icon (Join-Path $launcherDir 'bloodborne.ico') --add-data "$(Join-Path $launcherDir 'assets');assets" $source

$launcher = Join-Path $dist 'Bloodborne'
& (Join-Path $dist 'launcher-runtime-check/launcher-runtime-check.exe') --launcher `
    (Join-Path $launcher 'Bloodborne.exe') $check
Copy-Item -LiteralPath (Join-Path $root 'LICENSE') -Destination $launcher
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'INSTALL.txt') -Destination $launcher
$archiveName = "Bloodborne-$Version-private-server-launcher.zip"
$archive = Join-Path $output $archiveName
& $Python -m zipfile -c $archive (Join-Path $launcher 'Bloodborne.exe') (Join-Path $launcher '_internal') `
    (Join-Path $launcher 'LICENSE') (Join-Path $launcher 'INSTALL.txt')
& $Python -m zipfile -t $archive
$hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $archive).Hash.ToLowerInvariant()
Set-Content -LiteralPath "$archive.sha256" -Value "$hash  $archiveName" -Encoding ascii
Write-Output $archive
