# Package dist\ into PlatinumTranscriber_V8.zip (matches README release layout).
# Prerequisite: run 2_Build_Platinum.bat so dist\PlatinumTranscriber.exe exists.
param(
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$OutZip = ""
)
$ErrorActionPreference = "Stop"
$dist = Join-Path $ProjectRoot "dist"
$exe = Join-Path $dist "PlatinumTranscriber.exe"
if (-not (Test-Path $exe)) {
    Write-Error "Not found: $exe`nBuild first: place ffmpeg.exe + logo.ico, run 2_Build_Platinum.bat"
}
if (-not $OutZip) {
    $OutZip = Join-Path $ProjectRoot "PlatinumTranscriber_V8.zip"
}
if (Test-Path $OutZip) { Remove-Item -LiteralPath $OutZip -Force }
# Zip includes folder "dist" so users extract and open dist\PlatinumTranscriber.exe (see README).
Compress-Archive -Path $dist -DestinationPath $OutZip -CompressionLevel Optimal
$hash = Get-FileHash -Algorithm SHA256 -LiteralPath $OutZip
Write-Host "Created: $OutZip"
Write-Host "SHA256:  $($hash.Hash)"
$hash.Hash | Set-Content -Path ($OutZip + ".sha256") -Encoding ascii
Write-Host "Wrote:   $($OutZip).sha256"
