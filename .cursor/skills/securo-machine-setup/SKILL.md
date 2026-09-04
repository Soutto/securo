---
name: securo-machine-setup
description: >-
  Configures a Linux PC to run this Securo fork (branch lucas): Docker,
  official rclone for Proton Drive, host backup/update scripts, systemd 12:30
  timer, and restore from encrypted backup. Use when the user formatted the
  machine, changed computers, pasted SETUP-MAQUINA.txt, asks to set up Securo
  on a new Zorin/Ubuntu box, restore from Proton Drive, or reinstall rclone,
  systemd timers, or host scripts.
---

# Securo — setup de máquina nova

Speak Portuguese (Brazil) with the user. Never write secrets into git. The fork `Soutto/securo` is public.

If this chat is not already rooted at the clone, call `move_agent_to_root` on `~/Projects/securo` as soon as that directory exists.

Read [reference.md](reference.md) for paths, remotes, and compose flags.

## What success looks like

- App at `http://localhost:3000`, ports bound to `127.0.0.1`
- Images built from this checkout (`docker-compose.prod.yml` **and** `docker-compose.lucas.yml`)
- `origin` = fork, `upstream` = community, branch `lucas`
- Daily user timer `securo-backup.timer` at 12:30 (backup then rebase/update)
- Proton Drive remote `proton:Backup/securo` working
- GPG passphrase only in `~/.config/securo/backup-passphrase` (mode 600) and Proton Pass

## Ask the user (do not invent)

Ask before writing credentials. They live in Proton Pass:

1. GitHub login for `Soutto` (`gh auth login`) if push/clone needs it
2. Proton account email + password + 2FA
3. GPG backup passphrase (paste once; you write the file)
4. Confirmation they have the Proton **recovery PDF** on paper (not only inside Proton)

Never echo passphrases back in chat after writing the file.

## Workflow

Copy and tick:

```
- [ ] Docker + git + curl + unzip + gpg + python3
- [ ] Official rclone in ~/.local/bin (protondrive backend)
- [ ] Clone Soutto/securo → ~/Projects/securo, branch lucas
- [ ] Remotes origin/upstream
- [ ] host-setup/install.sh
- [ ] Passphrase file 600
- [ ] rclone remote proton + securo-proton-login
- [ ] compose build/up
- [ ] restore from Proton (type RESTORE)
- [ ] timer enabled, localhost opens, user logs in
```

### 1. Packages

On Zorin/Ubuntu:

```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-v2 git curl unzip gnupg python3
sudo usermod -aG docker "$USER"
```

If Docker was just granted, the user must re-login (or `newgrp docker`) before `docker info` works without sudo.

Enable Docker: `sudo systemctl enable --now docker`.

### 2. Clone and remotes

```bash
mkdir -p "$HOME/Projects"
git clone https://github.com/Soutto/securo.git "$HOME/Projects/securo"
cd "$HOME/Projects/securo"
git checkout lucas
git remote add upstream https://github.com/securo-finance/securo.git 2>/dev/null || git remote set-url upstream https://github.com/securo-finance/securo.git
git fetch origin
git fetch upstream
```

`origin` must be `Soutto/securo`. `upstream` must be `securo-finance/securo`. Do not push to `upstream`.

Then `move_agent_to_root` → `/home/<user>/Projects/securo`.

### 3. Host scripts + rclone + timer

```bash
bash host-setup/install.sh
```

That copies `host-setup/bin/*` to `~/.local/bin`, user systemd units, installs rclone if it lacks `protondrive`, and enables `securo-backup.timer`.

Zorin’s `/usr/bin/rclone` (1.60) cannot talk to Proton. Scripts must prefer `$HOME/.local/bin/rclone`.

Optional: `loginctl enable-linger "$USER"` so the timer can fire without a desktop session.

### 4. Secrets on disk (not in git)

```bash
install -d -m 700 "$HOME/.config/securo"
# write passphrase from Proton Pass, then:
chmod 600 "$HOME/.config/securo/backup-passphrase"
```

`.env` is restored from the backup archive. If restoring later, compose still needs a placeholder `.env` with `SECRET_KEY` to start `db` — prefer restore which copies `env` from the archive.

Do not commit `.env`, `secrets/`, or the passphrase file.

### 5. Proton Drive

If remote `proton` is missing:

```bash
rclone config create proton protondrive username "<email from user>" --non-interactive
```

Then ask the user to run in **their** terminal (needs TTY):

```bash
securo-proton-login
```

Wait until they confirm. `rclone config reconnect` is **unsupported** for protondrive — always password + `--protondrive-2fa`. Do not use `rclone lsd proton: --non-interactive` (invalid flag).

### 6. Start empty, then restore

```bash
cd "$HOME/Projects/securo"
mkdir -p secrets
docker compose -f docker-compose.prod.yml -f docker-compose.lucas.yml up -d --build
```

Wait until `db` is healthy. Then:

```bash
securo-restore --from-drive
```

The user must type `RESTORE`. After restore, recreate backend/frontend (the script already force-recreates).

Official GHCR images **ignore** this fork. Always include `docker-compose.lucas.yml`.

### 7. Verify

- `curl -sf http://127.0.0.1:8000/api/health`
- Open `http://localhost:3000` — user logs in from Proton Pass
- `systemctl --user list-timers | grep securo`
- `rclone lsd proton:Backup`

In-app “Atualização do servidor” only **checks** GitHub releases. Do **not** run the dialog’s `git pull && docker compose up`. Real update is `securo-update`.

Bank connections: **MeuPluggy**, never the bank’s own tile in the Pluggy widget.

## Commands the user already has

| Command | Job |
|---|---|
| `securo-backup` | Dump + GPG + Proton |
| `securo-update` | Backup, rebase `upstream/main` onto `lucas`, build/up, push fork |
| `securo-restore --from-drive` | Decrypt latest Proton archive into Docker |
| `securo-proton-login` | Save Proton session in rclone |

If rebase conflicts: script aborts rebase, keeps previous app, logs failure in `ops_logs`. If the working tree is dirty, update is skipped — commit or stash first.

## After setup

Point them to `docs/mapa.html` (memory map). Do not add secrets to that page.
