# Configuration

This page summarizes environment variables, config files, and runtime configuration.

## Key environment variables (examples from `settings.py`)
Important file: [`django_project/sheet_music_database/settings.py`](django_project/sheet_music_database/settings.py)

- `SECRET_KEY` (required) — Django secret key
  - Example: `SECRET_KEY='change-me-in-prod'`
- `DEBUG` (recommended to set to `False` in production)
  - Note: In settings file DEBUG is set to `False` by default.
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT` (required in production)
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` — email SMTP settings (see settings lines near email config)
- `ALLOWED_HOSTS` — also configured in `settings.py` but often safer to read from env in production

Example .env (do not commit):
```env
SECRET_KEY=super-secret-key
DEBUG=True
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
```

> WARNING: Never commit `SECRET_KEY` or production credentials into repo.

## Configuration files
- [`django_project/sheet_music_database/settings.py`](django_project/sheet_music_database/settings.py) — main Django configuration
- [`docker-compose.yml`](docker-compose.yml) — orchestration for containers
- [`Dockerfile`](Dockerfile) — image build
- [`nginx.conf`](nginx.conf) — reverse proxy configuration for production
- [`entrypoint.sh`](django_project/entrypoint.sh) — container entrypoint (runs collectstatic, migrate, gunicorn)

## Dev / Staging / Production differences
- DEBUG:
  - Dev: DEBUG=True (easier static/media serving and error pages)
  - Prod: DEBUG=False — ensure `ALLOWED_HOSTS` is correctly set and static files served by Nginx.
- Database:
  - Dev: SQLite (db.sqlite3 present for convenience)
  - Prod: PostgreSQL (env vars in `settings.py`)
- Static/media:
  - Dev: Django serves media when DEBUG=True (see `urls.py` [`django_project/sheet_music_database/urls.py`](django_project/sheet_music_database/urls.py))
  - Prod: Serve `staticfiles/` and `media/` via Nginx or object storage (S3)

## Secrets management
- Recommended: use environment variables injected by orchestration (docker-compose secrets, Kubernetes Secrets, or cloud secret manager).
- Avoid storing secrets in repository.
- Example: use `.env` for local dev and platform-specific secrets in production.

## Where to change settings
- Edit [`django_project/sheet_music_database/settings.py`](django_project/sheet_music_database/settings.py)
- For per-environment layering, consider splitting into `settings_dev.py` / `settings_prod.py` or use 12-factor env-based overrides.