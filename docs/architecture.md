# Architecture

## System diagram (Mermaid)
```mermaid
graph LR
  Browser -->|HTTP(S)| Nginx
  Nginx --> Gunicorn
  Gunicorn --> DjangoApp[DJANGO APP]
  DjangoApp -->|Reads/Writes| Media[Media Files (volume/S3)]
  DjangoApp -->|SQL| Postgres[PostgreSQL]
  DjangoApp -->|Static| Staticfiles[Collected staticfiles]
  Certbot --> Nginx
```

> The diagram describes production deployment. For local dev, the Django dev server replaces Nginx+Gunicorn.

## Component breakdown
- Web frontend (templates + Bootstrap): `django_project/sheet_music_app/templates/` — base, home, detail, forms.
  - Example: [base.html](django_project/sheet_music_app/templates/base.html)
- Views & routing:
  - Routes: [`django_project/sheet_music_app/urls.py`](django_project/sheet_music_app/urls.py)
  - Controllers: [`django_project/sheet_music_app/views.py`](django_project/sheet_music_app/views.py)
    - Key symbol: [`sheet_music_app.views.sheet_profile`](django_project/sheet_music_app/views.py)
    - Redirect helper: [`sheet_music_app.views.sheet_profile_redirect_by_pk`](django_project/sheet_music_app/views.py)
- Models & persistence:
  - App models live in: [`django_project/sheet_music_app/models.py`](django_project/sheet_music_app/models.py) (schema definitions, FileField/ImageField usage)
- Settings & configuration:
  - [`django_project/sheet_music_database/settings.py`](django_project/sheet_music_database/settings.py)
- Entry points:
  - CLI management: [`django_project/manage.py`](django_project/manage.py)
  - ASGI: [`django_project/sheet_music_database/asgi.py`](django_project/sheet_music_database/asgi.py)
  - Docker entrypoint: [entrypoint.sh](django_project/entrypoint.sh)
  - Dockerfile: [Dockerfile](Dockerfile)

## Data flow (high-level)
1. User requests homepage `/` -> handled by [`sheet_music_app.views.home`](django_project/sheet_music_app/views.py) -> queries DB -> returns rendered template.
2. User opens detail `/noty/<slug>` -> [`sheet_music_app.views.sheet_profile`](django_project/sheet_music_app/views.py) -> loads sheet record -> template embeds PDF or image from `MEDIA_URL`.
3. Editors upload files via form -> Django receives `multipart/form-data` -> saves `FileField` to `MEDIA_ROOT` and metadata to DB -> optionally generates slug.

## Technology choices / rationale
- Django for rapid development and built-in auth, admin, forms.
- PostgreSQL for production reliability; SQLite included for quick local dev.
- Docker + Gunicorn + Nginx for containerized, stable deployments.
- Static files collected to `staticfiles/` and served by Nginx in production for efficiency.

## Directory structure (high-level)
- `django_project/` — Django project root
  - `sheet_music_database/` — project settings & URLs
    - [`settings.py`](django_project/sheet_music_database/settings.py)
    - [`asgi.py`](django_project/sheet_music_database/asgi.py)
  - `sheet_music_app/` — application code (views, models, templates, static)
    - `templates/` — HTML templates (e.g., [sheet_profile.html](django_project/sheet_music_app/templates/sheet_profile.html))
    - `static/` — app-specific CSS/JS (e.g., [style.css](django_project/sheet_music_app/static/css/style.css))
- `staticfiles/` — collected static for serving
- `media/` — uploaded user files (PDFs, images)
- `Dockerfile`, `docker-compose.yml`, `entrypoint.sh` — deployment artifacts