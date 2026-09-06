# Getting Started

This guide walks you through local development setup and verification.

## Prerequisites
- Python 3.10+ (project uses Python 3.13 in Dockerfile)  
- pip
- virtualenv (recommended)
- Node/NPM not required (static assets are prebuilt)
- For production testing with Docker: Docker & docker-compose

Useful files:
- [requirements.txt](../requirements.txt)
- [Dockerfile](../Dockerfile)
- [docker-compose.yml](../docker-compose.yml)
- Django manage script: [`django_project/manage.py`](../django_project/manage.py)

## Installation (local)
1. Clone repository and create virtualenv:
```bash
git clone <repo>
cd <repo>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2. Create a `.env.local` file in the repo root with at least:
```env
DEBUG=True
SECRET_KEY=any-value-for-local-dev
```
With `DEBUG=True`, `settings.py` automatically switches to SQLite (`db.sqlite3`, no Postgres/Docker needed), prints emails to the console instead of sending via SMTP, and disables the production-only HTTPS/proxy enforcement (`SECURE_SSL_REDIRECT`, secure cookies, HSTS) that otherwise blocks plain `runserver`. `.env.local` is loaded automatically and is gitignored — see [configuration.md](configuration.md) for the full list of variables and how `.env.local`/`.env` interact.

3. Initialize database and create superuser:
```bash
python django_project/manage.py migrate
python django_project/manage.py createsuperuser
```

4. Collect static (dev optional):
```bash
python django_project/manage.py collectstatic --noinput
```

5. Run development server:
```bash
python django_project/manage.py runserver
```

Open http://127.0.0.1:8000/

## Run with Docker (production-like)
1. Build and start:
```bash
docker-compose up --build
```
2. The app runs via Gunicorn in container per [entrypoint.sh](django_project/entrypoint.sh).

## Verify installation
- Visit the homepage: `/` (root). Main view is implemented by [`sheet_music_app.views.home`](django_project/sheet_music_app/views.py).
- Admin panel: `/admin/` — login with the superuser.
- Upload test sheet: Use UI "Add sheet" -> endpoint [`sheet_music_app.urls.add_sheet`](django_project/sheet_music_app/urls.py).

## Common setup issues
- Missing environment variables -> app may fail at startup. Check [`settings.py`](django_project/sheet_music_database/settings.py) for required env vars.
> Tip: If DEBUG=False you must serve media in production; in dev the urlpatterns in [`django_project/sheet_music_database/urls.py`](django_project/sheet_music_database/urls.py) expose MEDIA only when DEBUG=True.

- Media files not found: ensure `MEDIA_ROOT` exists and Django has write permissions (see `MEDIA_ROOT` in [`settings.py`](django_project/sheet_music_database/settings.py)).

- Slugs missing for legacy rows: visit `/noty/id/<pk>` which triggers [`sheet_music_app.views.sheet_profile_redirect_by_pk`](django_project/sheet_music_app/views.py) to auto-generate a slug.