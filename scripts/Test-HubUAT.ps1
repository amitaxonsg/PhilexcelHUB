# Read-only PC-side site UAT evidence. Never probes WAN or changes NAS ACLs.
[CmdletBinding()]
param(
 [Parameter(Mandatory=$true)][string]$NasHost,
 [Parameter(Mandatory=$true)][string]$Share,
 [string]$OutputCsv='.\hub-uat-private.csv'
)
$ErrorActionPreference='Continue'
$tests=New-Object System.Collections.Generic.List[object]
function Add-Test([string]$name,[string]$result,[string]$detail){
 $tests.Add([pscustomobject]@{Timestamp=(Get-Date).ToString('o');Test=$name;Result=$result;Detail=$detail})
}
try { $ips=[System.Net.Dns]::GetHostAddresses($NasHost) | ForEach-Object IPAddressToString;Add-Test 'DNS/hostname' 'PASS' ($ips -join ',') }
catch { Add-Test 'DNS/hostname' 'FAIL' $_.Exception.Message }
foreach ($port in @(445,5001)) {
 try {$t=Test-NetConnection -ComputerName $NasHost -Port $port -InformationLevel Quiet -WarningAction SilentlyContinue;Add-Test "TCP port $port" $(if($t){'PASS'}else{'FAIL'}) 'LAN workstation to NAS'}
 catch {Add-Test "TCP port $port" 'FAIL' $_.Exception.Message}
}
$unc='\\'+$NasHost+'\'+$Share
try {$exists=Test-Path -LiteralPath $unc;Add-Test 'Authorized share path' $(if($exists){'PASS'}else{'REVIEW'}) $unc}
catch {Add-Test 'Authorized share path' 'REVIEW' $_.Exception.Message}
$tests | Export-Csv -LiteralPath $OutputCsv -NoTypeInformation -Encoding UTF8
$tests | Format-Table -AutoSize
Write-Warning 'This report can contain internal network details. Save ONLY to private Drive; never commit it.'
Write-Host "Saved $OutputCsv. Access denial, actual SMB ACLs, WAN security, Cloud Sync, snapshots, backup and dashboard authorization require separate manual UAT."
