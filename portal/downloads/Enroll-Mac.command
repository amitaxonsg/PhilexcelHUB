#!/bin/bash
set -euo pipefail
NAS='__NAS__'
USER_NAME='__USER__'
SHARES=(__SHARES__)
printf '%s\n' 'Philexcel Mac setup' 'Connect to office Wi-Fi or LAN first.' 'Existing Finder shares will be kept. Eject an old share in Finder only after closing its files.'
for SHARE in "${SHARES[@]}"; do
  printf 'Opening %s. Use your personal NAS password when Finder asks.\n' "$SHARE"
  open "smb://${USER_NAME}@${NAS}/${SHARE}"
done
printf '%s\n' 'In Finder, add the shares to your sidebar. For reconnection, add mounted volumes under System Settings > General > Login Items.' 'Away from the office? Open https://data.philexcel.com and sign in with Microsoft 365.'
read -r -p 'Press Enter to close.'
