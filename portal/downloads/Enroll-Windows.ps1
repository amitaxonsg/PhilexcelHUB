# Philexcel Windows setup. Run as your normal Windows user, not Administrator.
# Personalised by the enrollment portal. No password is embedded.
$ErrorActionPreference = 'Stop'
$NasHost = '__NAS__'
$NasUser = '__USER__'
$Mappings = @(
__MAPS__
)
if (-not (Test-NetConnection $NasHost -Port 445 -InformationLevel Quiet -WarningAction SilentlyContinue)) {
    throw 'The office file server cannot be reached. Connect to office Wi-Fi/LAN, or use https://data.philexcel.com while away.'
}
Write-Host 'These are your approved file drives:'
$Mappings | Format-Table Share,Letter
$Replace = @()
foreach ($Map in $Mappings) {
    $Map.Remote = "\\$NasHost\$($Map.Share)"
    $Existing = Get-SmbMapping -LocalPath "$($Map.Letter):" -ErrorAction SilentlyContinue
    $Drive = Get-PSDrive -Name $Map.Letter -ErrorAction SilentlyContinue
    if ($Existing -and $Existing.RemotePath -ieq $Map.Remote) { $Map.Skip=$true; continue }
    if ($Drive -and -not $Existing) { throw "Drive $($Map.Letter): is occupied. Ask Axon to check it. Nothing has been changed." }
    if ($Existing) {
        Write-Host "Drive $($Map.Letter): currently points to $($Existing.RemotePath)."
        Write-Host 'Close files on that drive before replacing it. Your files will not be deleted.'
        $Answer = Read-Host "Type REPLACE $($Map.Letter) only if your administrator approved this change; otherwise press Enter to cancel"
        if ($Answer -cne "REPLACE $($Map.Letter)") { throw 'Setup cancelled. Existing drives have been kept.' }
        $Replace += [pscustomobject]@{Letter=$Map.Letter; Remote=$Existing.RemotePath}
    }
}
$Credential = Get-Credential -UserName $NasUser -Message 'Enter your personal Philexcel NAS password. This may differ from your email password.'
if (-not $Credential) { throw 'Setup cancelled.' }
# Verify each target with a temporary, non-persistent PS drive before removing old mappings.
foreach ($Map in $Mappings) {
    if ($Map.Skip) {continue}
    $Probe = 'HubProbe' + [guid]::NewGuid().ToString('N').Substring(0,8)
    try {
        New-PSDrive -Name $Probe -PSProvider FileSystem -Root $Map.Remote -Credential $Credential | Out-Null
        Get-ChildItem -LiteralPath ($Probe + ':\') -ErrorAction Stop | Select-Object -First 1 | Out-Null
    } finally { Remove-PSDrive -Name $Probe -ErrorAction SilentlyContinue }
}
$BackupDir = Join-Path $env:LOCALAPPDATA 'PhilexcelHub'
New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
$Backup = Join-Path $BackupDir ('previous-drives-' + (Get-Date -Format yyyyMMdd-HHmmss) + '.json')
ConvertTo-Json -InputObject @($Replace) | Set-Content -LiteralPath $Backup -Encoding UTF8
$Created = @()
try {
    foreach ($Map in $Mappings) {
        if ($Map.Skip) { Write-Host "$($Map.Letter): is already ready."; continue }
        $Old = $Replace | Where-Object Letter -eq $Map.Letter
        if ($Old) { Remove-SmbMapping -LocalPath "$($Map.Letter):" -UpdateProfile -Confirm:$false -ErrorAction Stop }
        New-PSDrive -Name $Map.Letter -PSProvider FileSystem -Root $Map.Remote -Persist -Scope Global -Credential $Credential | Out-Null
        $Created += $Map.Letter
        Get-Item -LiteralPath "$($Map.Letter):\" -ErrorAction Stop | Out-Null
        Write-Host "$($Map.Letter): $($Map.Share) is ready."
    }
} catch {
    foreach ($Letter in $Created) { Remove-SmbMapping -LocalPath ($Letter+':') -UpdateProfile -Confirm:$false -ErrorAction SilentlyContinue }
    foreach ($Old in $Replace) {
        if (-not (Get-PSDrive -Name $Old.Letter -ErrorAction SilentlyContinue)) {
            try { New-PSDrive -Name $Old.Letter -PSProvider FileSystem -Root $Old.Remote -Persist -Scope Global | Out-Null }
            catch { Write-Warning "Ask Axon to reconnect $($Old.Letter): to $($Old.Remote). Old server credentials may be required." }
        }
    }
    throw "Setup did not finish. Previous mappings recorded at $Backup. $($_.Exception.Message)"
} finally { $Credential=$null }
Write-Host 'Done. Open File Explorer > This PC. Windows may ask for your NAS password again after restarting.'
Write-Host 'Away from the office? Open https://data.philexcel.com and use your Microsoft 365 sign-in.'
Read-Host 'Press Enter to close'
