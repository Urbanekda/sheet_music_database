# API / Endpoints (HTTP routes)

This project does not expose a public REST API; it serves HTML pages via Django views. Below are the main HTTP endpoints (from [`django_project/sheet_music_app/urls.py`](django_project/sheet_music_app/urls.py)).

## Public / UI endpoints
- Home / listing:
  - GET `/` -> [`sheet_music_app.views.home`](django_project/sheet_music_app/views.py)
- Add sheet (form):
  - GET/POST `/sheet/add` -> [`sheet_music_app.views.add_sheet`](django_project/sheet_music_app/urls.py)
- Edit sheet:
  - GET/POST `/edit/<int:pk>` -> [`sheet_music_app.views.edit_sheet`](django_project/sheet_music_app/urls.py)
- Delete sheet:
  - POST `/delete/<int:pk>/` -> [`sheet_music_app.views.delete_sheet`](django_project/sheet_music_app/urls.py)
- Sheet detail (slug preferred):
  - GET `/noty/<slug:slug>` -> [`sheet_music_app.views.sheet_profile`](django_project/sheet_music_app/views.py)
- Legacy ID redirect:
  - GET `/noty/id/<int:pk>` -> [`sheet_music_app.views.sheet_profile_redirect_by_pk`](django_project/sheet_music_app/urls.py) (auto-generates slug if missing then redirects)

## Auth endpoints (Django auth and allauth)
- Login: `/login/` (`auth_views.LoginView` in `urls.py`)
- Logout: `/logout/`
- Register: `/register/` -> custom `views.register`
- Password reset flow:
  - `/password_reset/`
  - `/password_reset/done/`
  - `/reset/<uidb64>/<token>/`
  - `/reset/done/`

## Example usage (curl)
Fetch homepage:
```bash
curl -v http://127.0.0.1:8000/
```

Fetch a sheet detail (public):
```bash
curl -v http://127.0.0.1:8000/noty/some-sheet-slug/
```

> NOTE: Authentication-protected actions (add/edit/delete) require login and CSRF token; use browser or automated test client to perform authenticated requests.

## Authentication & Authorization
- Uses Django built-in auth and custom template tags for permission checks (`{% load permissions %}` in templates).
- Editor and superuser checks appear in templates via `is_editor` and `is_superuser` filters (implemented in app templatetags).
- Admin panel available at `/admin/` (Django admin).

## Errors
- Standard Django HTTP status codes apply (401/403 for unauthorized/forbidden, 404 for not found, 500 for server error).
- Form validation errors are displayed in templates using Django form error handling.