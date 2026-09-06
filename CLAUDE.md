# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Django app for managing a private/public sheet music database. Registered users browse/search/filter sheets; staff/superusers (and members of the "Internal" group) can additionally add, edit, and delete records and see non-public sheets. Detail pages use slugs (`/noty/<slug>`) with a legacy numeric-ID route that redirects to the slug.

Full docs live in `docs/` (`getting-started.md`, `architecture.md`, `configuration.md`, `database.md`, `api.md`, `deployment.md`, `development.md`, `troubleshooting.md`) — read the relevant one before making non-trivial changes in that area.

## Commands

All Django management commands run from `django_project/` (where `manage.py` lives).

```bash
# Setup
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Local dev — create .env.local with DEBUG=True first (see below)
python django_project/manage.py migrate
python django_project/manage.py createsuperuser
python django_project/manage.py runserver

# Migrations after editing models.py
python django_project/manage.py makemigrations
python django_project/manage.py migrate

# Tests (pytest is in requirements.txt, but sheet_music_app/tests.py is currently empty)
python django_project/manage.py test

# Static files
python django_project/manage.py collectstatic --noinput

# Docker (production-like stack: Nginx + Gunicorn + Postgres + Certbot)
docker-compose up --build -d
docker-compose logs -f
```

## Required environment (`.env.local` for dev, `.env` for the Docker/prod stack — neither committed)

`settings.py` loads `.env.local` then `.env` from the repo root via `python-dotenv` (first value wins; real process env vars, e.g. from Docker, always win over both). `DEBUG` (default `False`) is the single switch that determines the rest of the environment:
- `DEBUG=True` → SQLite (`db.sqlite3`), console email backend, no HTTPS/HSTS/secure-cookie enforcement, Turnstile verification skipped and widget hidden. Only `SECRET_KEY` is really needed on top of this — put both in `.env.local`.
- `DEBUG=False` (prod/Docker) → requires `SECRET_KEY`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`, and for real bot protection `TURNSTILE_SITE_KEY`/`TURNSTILE_SECRET_KEY` — all read via plain `os.getenv` with no defaults.

`ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` are hardcoded lists in `settings.py` (already include `localhost`/`127.0.0.1` for dev, plus the production domain) — update them there if a new host/origin is needed.

## Architecture

Single Django app (`sheet_music_app`) inside project `sheet_music_database`. No REST API — server-rendered HTML only (Bootstrap 5 templates).

- **Models** (`sheet_music_app/models.py`): `Sheet` (title, composer, arranger, cast/season/use choice fields, publisher/isbn/description, `sheet_file` FileField, `preview_image` ImageField, `public` bool, auto-generated unique `slug`, `created_by`/`modified_by` FKs to `auth.User`, M2M `tags`) and `Tag`. Note: `Sheet`'s `Meta` class is accidentally declared at module scope (not nested inside `Sheet`), so the intended default ordering/`can_view_private` permission do **not** actually apply — be aware of this if you touch ordering/permissions logic, and prefer fixing it properly (nest it in `Sheet`) over building around it.
- **Views** (`sheet_music_app/views.py`): plain function-based views, no DRF/ModelForms — `add_sheet`/`edit_sheet` read straight from `request.POST`/`request.FILES` and manually normalize blank strings to `None`. Tags are parsed from a comma-separated text input, matched case-insensitively, created if missing. Visibility rule: staff, superusers, and users in the "Internal" group see all sheets; everyone else sees only `public=True`.
- **URLs** (`sheet_music_app/urls.py`): included from the project's `sheet_music_database/urls.py`. Slug route (`noty/<slug:slug>`) is canonical; numeric routes (`noty/id/<pk>`, `noty/<pk>`) exist only to redirect to the slug, backfilling the slug via `save()` if missing.
- **Permissions in templates**: `{% load permissions %}` exposes custom filters `is_editor`, `is_superuser`, `in_group` (`sheet_music_app/templatetags/permissions.py`) — use these in templates rather than re-checking `user.is_staff` inline.
- **Auth**: mix of Django's built-in auth views (login/logout/password reset) and `django-allauth` (mandatory email verification, `ACCOUNT_EMAIL_VERIFICATION = "mandatory"`). Registration is a custom view (`views.register`) that sends a confirmation email via `EmailMultiAlternatives` using templates in `sheet_music_app/templates/emails/`.
- **Deployment**: Docker Compose stack of Nginx + Gunicorn (via `entrypoint.sh`: collectstatic → migrate → gunicorn) + Postgres + Certbot, per `docker-compose.yml`/`Dockerfile`/`nginx.conf`. See `docs/deployment.md` for details.

## Conventions

- User-facing strings (messages, choice labels) are in Czech; keep new user-facing text consistent with that.
- No DRF, no ModelForms for `Sheet` CRUD — the existing add/edit views intentionally build the model from raw `request.POST`/`request.FILES`. Match that style rather than introducing `forms.ModelForm` for `Sheet` unless asked to refactor it.
