# PHILEXCEL HUB | Read-only PowerShell-driven Synology NAS inventory
# Run from a trusted Windows PowerShell 5.1+ terminal. No administrative NAS changes.
# Do NOT commit generated reports: they contain private network and account information.
[CmdletBinding()]
param(
  [string]$NasHost = 'PHILEXCEL-NAS',
  [string]$SshUser = 'axonadmin',
  [string]$OutputDirectory = '.\\philexcel-private-audit'
)
$ErrorActionPreference = 'Stop'
if ($NasHost -notmatch '^[a-zA-Z0-9][a-zA-Z0-9.-]{0,252}$') { throw 'Invalid NAS hostname' }
if ($SshUser -notmatch '^[a-zA-Z0-9_.-]+$') { throw 'Invalid SSH username' }
if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) { throw 'Windows OpenSSH client is required' }
New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$report = Join-Path $OutputDirectory "NAS-Inventory-$timestamp.txt"
$commands = @(
 'echo === VERSION ===; cat /etc.defaults/VERSION',
 'echo === SYSTEM ===; hostname; uname -a; date',
 'echo === STORAGE ===; df -h /volume1 /volume2',
 'echo === STORAGE POOLS ===; cat /proc/mdstat',
 'echo === NETWORK ===; ip -4 addr show; ip route show',
 'echo === SMB PACKAGE ===; synopkg status SMBService',
 'echo === SMB LISTENERS ===; netstat -lnt 2>/dev/null | grep :445 || true',
 'echo === SHARES ===; ls -la /volume1 /volume2',
 'echo === LOCAL USERS ===; cut -d: -f1 /etc/passwd',
 'echo === LOCAL GROUPS ===; cut -d: -f1 /etc/group'
)
Write-Host "SSH target: $SshUser@$NasHost. Confirm the host-key fingerprint independently before accepting."
$results = New-Object 'System.Collections.Generic.List[string]'
foreach ($command in $commands) {
  $results.Add("COMMAND: $command")
  $response = & ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=ask "$SshUser@$NasHost" $command 2>&1
  $results.Add(($response | Out-String))
  $results.Add("EXIT CODE: $LASTEXITCODE")
}
$results | Set-Content -LiteralPath $report -Encoding UTF8
Write-Host "Private inventory saved: $report"
Write-Warning 'Output contains internal IPs, usernames, and inventory. Keep only in restricted Axon/PHILEXCEL storage. This script makes no NAS changes.'
