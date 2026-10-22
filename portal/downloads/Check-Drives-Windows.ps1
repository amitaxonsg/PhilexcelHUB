# Read-only local inventory. No upload, password prompt, mapping or removal.
$ErrorActionPreference = 'Stop'
Write-Host 'Philexcel network drive check - no changes will be made.'
try {
    $Mappings = @(Get-SmbMapping -ErrorAction Stop)
    if ($Mappings.Count) { $Mappings | Select-Object LocalPath,RemotePath,Status | Format-Table -AutoSize }
    else { Write-Host 'No SMB mappings were reported for this Windows session.' }
    Get-PSDrive -PSProvider FileSystem | Select-Object Name,Root,DisplayRoot | Format-Table -AutoSize
    Write-Host 'Only this Windows user/session was checked. Run as your normal user. No report was uploaded.'
} catch { Write-Warning "Could not complete the check: $($_.Exception.Message)" }
Read-Host 'Press Enter to close'
