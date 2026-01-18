# Documentation Home

Welcome — this folder contains developer and operational documentation for the Sheet Music Database.

## Project overview (detailed)
Sheet Music Database is a Django web application that provides a searchable, filterable catalog of sheet music records. Users can preview (embedded PDFs/images), download, and (if authorized) upload and edit records. The app supports role-aware features (editor/admin) and stable human-friendly URLs (slugs) with compatibility redirects for legacy numeric IDs.

## Problem solved
- Centralized, searchable repository of sheet music for a choir/ensemble.
- Simple upload and moderation workflow with role-based access.
- Stable public-facing links for references and printed materials.

## High-level architecture
- Django app serves HTML pages and manages media files.
- Static assets are collected to `staticfiles/`.
- Production runs Gunicorn behind Nginx; Certbot handles TLS.
- Database: PostgreSQL in production; SQLite included for local dev.

Primary files & entry points:
- Project settings: [`django_project/sheet_music_database/settings.py`](django_project/sheet_music_database/settings.py)
- URL routing: [`django_project/sheet_music_app/urls.py`](django_project/sheet_music_app/urls.py)
- Main views: [`django_project/sheet_music_app/views.py`](django_project/sheet_music_app/views.py)
- WSGI/ASGI entrypoints: [`django_project/sheet_music_database/asgi.py`](django_project/sheet_music_database/asgi.py), `manage.py` (`django_project/manage.py`)

## Links to other docs
- [Getting started](getting-started.md)
- [Architecture](architecture.md)
- [Configuration](configuration.md)
- [API (endpoints)](api.md)
- [Database](database.md)
- [Deployment](deployment.md)
- [Development workflow](development.md)
- [Troubleshooting](troubleshooting.md)