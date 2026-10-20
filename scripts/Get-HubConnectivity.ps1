# Read-only NAS connectivity diagnostic, run from Windows PowerShell on office LAN.
param([Parameter(Mandatory=$true)][string]$NasHost)
Write-Host 'PhilexcelHUB connectivity check (read only)'
foreach($port in @(445,5001,22)) {
 $ok=Test-NetConnection -ComputerName $NasHost -Port $port -InformationLevel Quiet -WarningAction SilentlyContinue
 [pscustomobject]@{Host=$NasHost;Port=$port;Reachable=$ok}
}
