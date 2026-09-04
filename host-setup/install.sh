#!/usr/bin/env bash
# Install host scripts, rclone (Proton-capable), and the 12:30 systemd timer.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BIN="$HOME/.local/bin"
UNIT_DIR="$HOME/.config/systemd/user"

mkdir -p "$BIN" "$UNIT_DIR" "$HOME/.config/securo" "$HOME/.local/share/securo-backups"

install -m 0700 "$SCRIPT_DIR/bin/"* "$BIN/"
install -m 0644 "$SCRIPT_DIR/systemd/"*.service "$SCRIPT_DIR/systemd/"*.timer "$UNIT_DIR/"

need_rclone=1
if [[ -x "$BIN/rclone" ]] && "$BIN/rclone" help backends 2>/dev/null | grep -q protondrive; then
  need_rclone=0
fi
if [[ "$need_rclone" -eq 1 ]]; then
  echo "Installing rclone (Proton Drive) into $BIN ..."
  tmp="$(mktemp -d)"
  curl -fsSL -o "$tmp/rclone.zip" "https://downloads.rclone.org/rclone-current-linux-amd64.zip"
  unzip -o -q "$tmp/rclone.zip" -d "$tmp"
  rdir="$(ls -d "$tmp"/rclone-v*-linux-amd64 | head -n1)"
  install -m 0755 "$rdir/rclone" "$BIN/rclone"
  rm -rf "$tmp"
fi

"$BIN/rclone" help backends | grep -q protondrive

systemctl --user daemon-reload
systemctl --user enable --now securo-backup.timer

echo "Host setup installed."
echo "Next: put the GPG passphrase in $HOME/.config/securo/backup-passphrase"
echo "Then run: securo-proton-login"
