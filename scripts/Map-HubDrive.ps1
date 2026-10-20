# Preview by default; maps only explicitly approved NAS share when -Apply supplied.
param([Parameter(Mandatory=$true)][string]$NasHost,[Parameter(Mandatory=$true)][string]$Share,[ValidatePattern('^[D-Z]$')][string]$DriveLetter='P',[switch]$Apply)
$path='\\'+$NasHost+'\'+$Share
if (-not $Apply) { Write-Host "PREVIEW: $DriveLetter`: -> $path (no changes)"; return }
if (Get-PSDrive -Name $DriveLetter -ErrorAction SilentlyContinue) { throw 'Drive letter occupied; nothing changed.' }
$cred=Get-Credential -Message 'Enter your own NAS credentials'
New-PSDrive -Name $DriveLetter -PSProvider FileSystem -Root $path -Credential $cred -Persist -Scope Global
