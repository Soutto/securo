# Securo host reference

## Layout

| Thing | Path / value |
|---|---|
| Clone | `$HOME/Projects/securo` |
| Branch | `lucas` |
| origin | `https://github.com/Soutto/securo.git` |
| upstream | `https://github.com/securo-finance/securo.git` |
| App | `http://localhost:3000` |
| API health | `http://127.0.0.1:8000/api/health` |
| `.env` binds | `FRONTEND_PORT=127.0.0.1:3000` `BACKEND_PORT=127.0.0.1:8000` `FRONTEND_URL=http://localhost:3000` |
| GPG passphrase | `$HOME/.config/securo/backup-passphrase` |
| Local archives | `$HOME/.local/share/securo-backups/` (keep 3) |
| Proton dest | `proton:Backup/securo` (delete `.gpg` older than 14 days) |
| rclone | `$HOME/.local/bin/rclone` (≥ backend `protondrive`) |
| Scripts | `$HOME/.local/bin/securo-*` from `host-setup/bin/` |
| Timer | `~/.config/systemd/user/securo-backup.timer` `OnCalendar=*-*-* 12:30:00` `Persistent=true` `RandomizedDelaySec=5m` |
| Compose | `docker compose -f docker-compose.prod.yml -f docker-compose.lucas.yml` |
| Images | `securo-backend:lucas` `securo-frontend:lucas` (not GHCR `:latest`) |
| Volumes | `securo_pgdata` `securo_attachments` `securo_agent_knowledge` `securo_agent_embedding_models` |

## Timer behavior

Service `ExecStart` is `securo-update` (backup first, then git rebase, then compose build/up, then `git push --force-with-lease origin lucas`).

`GIT_TERMINAL_PROMPT=0` so a missing GitHub login does not hang the timer; local update can still succeed.

Ops UI: `GET /api/ops-logs?limit=5`, account menu “Log de backup e update”.

## Proton notes

- rclone 1.60 on Ubuntu/Zorin **cannot** use Proton Drive.
- `rclone config reconnect` does not work for protondrive.
- Username example on the first machine was stored in rclone config, not in git.

## Vault reminder (Proton Pass)

Suggested vaults (not machine setup): Identidade, Dinheiro, Trabalho, Casa e dia a dia.

Banks in Securo: connect via [MeuPluggy](https://meu.pluggy.ai), not the bank’s direct Pluggy connector.

Recovery PDF of the Proton account: paper copy. A Google Drive copy is extra, never the only copy, and never the only place for the GPG passphrase.
