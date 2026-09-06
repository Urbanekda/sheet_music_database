# Configuration

This page summarizes environment variables, config files, and runtime configuration.

## Key environment variables (examples from `settings.py`)
Important file: [`django_project/sheet_music_database/settings.py`](django_project/sheet_music_database/settings.py)

- `SECRET_KEY` (required) — Django secret key
  - Example: `SECRET_KEY='change-me-in-prod'`
- `DEBUG` — `False` if unset. Setting it to `True` switches several other settings at once (see "Dev / Staging / Production differences" below) — this is the one flag that turns the local/testing environment on.
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT` (required only when `DEBUG=False`; ignored otherwise)
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` — SMTP settings, only used when `DEBUG=False` (see settings lines near email config)
- `ALLOWED_HOSTS` — also configured in `settings.py` but often safer to read from env in production
- `TURNSTILE_SITE_KEY`, `TURNSTILE_SECRET_KEY` — Cloudflare Turnstile widget/verification keys used on the login and registration forms (see [`sheet_music_app/turnstile.py`](../django_project/sheet_music_app/turnstile.py)); verification and the widget itself are skipped entirely when `DEBUG=True`, so these aren't needed locally.

## Env files and load order
`settings.py` loads env files itself via `python-dotenv`, in this order (first one to set a given key wins; real process env vars — e.g. injected by Docker — always win over both):
1. `.env.local` (repo root, gitignored) — for local development/testing. Not used by `docker-compose.yml`.
2. `.env` (repo root, gitignored) — used by `docker-compose.yml` for the prod-like Docker stack (`env_file: .env` on each service).

For local dev/testing, create `.env.local`:
```env
DEBUG=True
SECRET_KEY=any-value-for-local-dev
DEFAULT_FROM_EMAIL=dev@localhost
```
Nothing else is required — Postgres/SMTP/Turnstile vars are unused while `DEBUG=True`.

Example `.env` (production, do not commit):
```env
SECRET_KEY=super-secret-key
DEBUG=False
POSTGRES_DB=sheetmusic
POSTGRES_USER=sm_user
POSTGRES_PASSWORD=sm_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=secret
DEFAULT_FROM_EMAIL=noreply@example.com
TURNSTILE_SITE_KEY=...
TURNSTILE_SECRET_KEY=...
```

> WARNING: Never commit `SECRET_KEY` or production credentials into repo.

## Configuration files
- [`django_project/sheet_music_database/settings.py`](django_project/sheet_music_database/settings.py) — main Django configuration
- [`docker-compose.yml`](docker-compose.yml) — orchestration for containers
- [`Dockerfile`](Dockerfile) — image build
- [`nginx.conf`](nginx.conf) — reverse proxy configuration for production
- [`entrypoint.sh`](django_project/entrypoint.sh) — container entrypoint (runs collectstatic, migrate, gunicorn)

## Dev / Staging / Production differences
Everything below is driven by the single `DEBUG` flag in `settings.py`:
- Database: SQLite (`db.sqlite3`, no setup needed) when `DEBUG=True`; PostgreSQL (`POSTGRES_*` env vars) when `DEBUG=False`.
- Email: console backend (prints to stdout) when `DEBUG=True`; real SMTP when `DEBUG=False`.
- HTTPS/proxy enforcement: `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, and HSTS are all off when `DEBUG=True`, on when `DEBUG=False`. These assume the production Nginx proxy terminates TLS and sets `X-Forwarded-Proto`; without a proxy in front, `DEBUG=False` locally would redirect-loop on plain HTTP.
- Turnstile: skipped (no verification, widget hidden) when `DEBUG=True`.
- Static/media: Django serves media itself when `DEBUG=True` (see `urls.py` [`django_project/sheet_music_database/urls.py`](django_project/sheet_music_database/urls.py)); in production Nginx serves `staticfiles/` and `media/` directly (`nginx.conf`).

## Secrets management
- Recommended: use environment variables injected by orchestration (docker-compose secrets, Kubernetes Secrets, or cloud secret manager).
- Avoid storing secrets in repository — `.env` and `.env.local` are both gitignored.

## Where to change settings
- Edit [`django_project/sheet_music_database/settings.py`](django_project/sheet_music_database/settings.py)
- For per-environment layering, consider splitting into `settings_dev.py` / `settings_prod.py` or use 12-factor env-based overrides.