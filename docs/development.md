# Development

This document explains common development tasks and conventions.

## Workflow
1. Create a feature branch from `main`:
```bash
git checkout -b feature/short-description
```
2. Implement changes, add tests, run locally.
3. Commit, open PR, request review.

## Code style & conventions
- Python: follow PEP8; use tools like `flake8` / `black` if added.
- Templates: Django template language, load custom tags with `{% load permissions %}` (see [base.html](../django_project/sheet_music_app/templates/base.html)).
- Static CSS: project uses Bootstrap and custom CSS in `sheet_music_app/static/css/style.css` and `staticfiles/css/style.css`.

## Running tests
- If tests exist, run:
```bash
python django_project/manage.py test
```
(Repository does not show test files by default; add tests under `sheet_music_app/tests/`)

## Debugging tips
- Use Django debug toolbar in development (not present by default).
- Check server logs when running with Gunicorn: `docker-compose logs -f`.
- Templates: enable `DEBUG=True` to see full tracebacks.

## Add a new feature
1. Add/modify model in `sheet_music_app/models.py`.  
2. Create migrations:
```bash
python django_project/manage.py makemigrations
python django_project/manage.py migrate
```
3. Implement view in `views.py` and route in `urls.py` (`django_project/sheet_music_app/urls.py`).
4. Add template under `sheet_music_app/templates/`.
5. Add unit tests under `sheet_music_app/tests/`.

## Branch strategy
- `main` contains deployable code.
- Feature branches named `feature/<desc>`.
- Use PRs and reviews before merging.

## Local assets
- Collect static files for testing:
```bash
python django_project/manage.py collectstatic --noinput
```

## Useful file references
- Entrypoints: [`manage.py`](../django_project/manage.py), [`entrypoint.sh`](../django_project/entrypoint.sh)
- Settings: [`settings.py`](../django_project/sheet_music_database/settings.py)