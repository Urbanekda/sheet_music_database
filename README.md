# Sheet Music Database

A Django-based web application for managing a private/public database of sheet music. Users can browse, filter, and search entries; editors and admins can add, edit, and delete sheet records. Slug-based detail URLs provide stable, human-friendly links with backwards-compatible redirects from legacy numeric IDs.

## Features
- **Authentication-gated homepage** with filters for genre, difficulty, and publication year.
- **Search** across title, composer, arranger, publisher, ISBN, and description.
- **Pagination** for scalable browsing.
- **Role-aware UI** using custom permission template tags (e.g., `is_editor`, `is_superuser`).
- **CRUD for editors/admins** with optional file upload (PDF/images) and preview image.
- **Auto-generated slugs** with collision handling for detail pages.

## Tech Stack
- **Backend**: Django (5.2.x)
- **Database**: SQLite by default (changeable via Django settings)
- **Static/UI**: Bootstrap 5, Bootstrap Icons
- **Media**: Managed via Django `FileField`/`ImageField` (requires Pillow)

## Project Layout
- App code: `django_project/sheet_music_app/`
  - Models: `models.py`
  - Views: `views.py`
  - Routes: `urls.py`
  - Templates: `templates/`
- Requirements: `requirements.txt`

## Getting Started (Local Development)

### 1) Prerequisites
- Python 3.10+
- Virtualenv recommended

### 2) Setup
```bash
# Create and activate a virtual environment (example)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3) Configure settings
By default the Django settings should point to SQLite and local static/media handling. If you need to configure media/static paths, edit your project settings (usually in `django_project/<project_name>/settings.py`). Ensure MEDIA and STATIC dirs exist and are writable in development.

### 4) Run migrations and create a superuser
```bash
python django_project/manage.py migrate
python django_project/manage.py createsuperuser
```

### 5) Run the development server
```bash
python django_project/manage.py runserver
```
Open http://127.0.0.1:8000/ to access the app. Admin is at http://127.0.0.1:8000/admin/.

## Usage Notes
- The homepage (`views.home`) shows only public records to regular users; staff/superusers see all records.
- Filters and search are passed via GET parameters and preserved across pagination.
- Detail pages prefer the slug route: `noty/<slug>/`. Legacy numeric routes redirect to the slug.
- Editors/superusers can upload a sheet file (PDF or image) and an optional preview image.

## Media & Static Files (Dev)
- Make sure `MEDIA_ROOT` and `MEDIA_URL` are configured in settings.
- During development, you may serve media with `django.conf.urls.static.static` in the project `urls.py` (guard with `DEBUG`).

## Custom Template Tags
The templates load `{% load permissions %}`. This implies a custom template tag library that exposes helpers like `is_editor` and `is_superuser`. Ensure this library exists on the Python path (e.g., `templatetags/permissions.py`) and is discoverable by Django.

## Deployment (Overview)
- Configure a production-ready database and storage for media (e.g., S3, local volume).
- Collect static files: `python manage.py collectstatic`.
- Run with a WSGI/ASGI server (Gunicorn/Uvicorn + reverse proxy like Nginx).
- Set `DEBUG = False` and configure `ALLOWED_HOSTS`.

## Troubleshooting
- If slugs are missing for old rows, visiting `noty/<pk>` will auto-generate the slug and redirect to `noty/<slug>`.
- If image previews fail to load, ensure Pillow is installed and media storage is configured.

## License
Private/Proprietary unless specified otherwise by the repository owner.
