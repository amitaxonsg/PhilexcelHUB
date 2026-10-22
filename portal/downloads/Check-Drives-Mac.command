#!/bin/bash
set -euo pipefail
printf '%s\n' 'Philexcel Mac connection check - no changes or uploads.'
/sbin/mount | /usr/bin/grep 'smbfs' || true
printf '%s\n' 'These are mounted SMB volumes visible to this session.' 'Saved Finder favourites and unmounted connections are not listed.' 'Keep working company volumes. Eject an old volume only after closing its files.'
read -r -p 'Press Return to close. '
