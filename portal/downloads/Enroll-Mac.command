#!/bin/bash
set -euo pipefail
NAS='__NAS__'
USER_NAME='__USER__'
SHARES=(__SHARES__)
printf '%s\n' 'Philexcel Mac setup' 'Connect to office Wi-Fi or LAN first.' 'Existing Finder shares will be kept. Eject an old share in Finder only after closing its files.'
printf '%s\n' 'Existing SMB connections (shown only on this device):'
mount | grep 'smbfs' || true
read -r -p 'Type CONNECT to open company folders, or press Enter to finish without changes: ' CHOICE
if [ "$CHOICE" != CONNECT ]; then exit 0; fi
for SHARE in "${SHARES[@]}"; do
  if mount | grep 'smbfs' | grep -F "@${NAS}/${SHARE} on " >/dev/null; then
    printf '%s already has a connection. Keeping it.\n' "$SHARE"
    continue
  fi
  printf 'Opening %s. Use your personal NAS password when Finder asks.\n' "$SHARE"
  open "smb://${USER_NAME}@${NAS}/${SHARE}"
done
printf '%s\n' 'Finder may ask you to approve each connection. Check each folder opens successfully. In Finder, add the shares to your sidebar. For reconnection, add mounted volumes under System Settings > General > Login Items.' 'Away from the office? Open https://data.philexcel.com and sign in with Microsoft 365.'
read -r -p 'Press Enter to close.'

