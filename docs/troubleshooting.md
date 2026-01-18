# Troubleshooting

Common issues and how to resolve them.

## 1. Server fails to start
Check logs:
```bash
docker-compose logs web
# or for local dev
python django_project/manage.py runserver
```
Common causes:
- Missing env var `SECRET_KEY` or DB credentials.
- Port already in use.

## 2. Static files / styles not loading
- Ensure `collectstatic` has been run: `python django_project/manage.py collectstatic --noinput`
- In production, ensure Nginx serves `staticfiles/` and `MEDIA_ROOT` and permissions are correct.

## 3. Media files not visible
- If DEBUG=False, Django will not serve media — configure Nginx to serve `media/`.
- Verify `MEDIA_ROOT` in [`settings.py`](django_project/sheet_music_database/settings.py).

## 4. Slug or detail page issues
If a legacy record lacks a slug, hitting `/noty/id/<pk>` triggers auto-generation via [`sheet_music_app.views.sheet_profile_redirect_by_pk`](django_project/sheet_music_app/views.py):
- Check view at: [`django_project/sheet_music_app/views.py`](django_project/sheet_music_app/views.py)

## 5. Email sending issues
- Verify SMTP environment variables (`EMAIL_HOST`, `EMAIL_HOST_USER`, etc.) configured in [`settings.py`](django_project/sheet_music_database/settings.py).
- For local dev, consider Django console/email backend for testing.

## 6. Database errors / migrations
- Run migrations:
```bash
python django_project/manage.py migrate
```
- If migrations fail, inspect migration files under `sheet_music_app/migrations/` and roll back if necessary.

## Where to find logs
- Docker: `docker-compose logs -f`
- Gunicorn inside container logs to stdout (view via docker logs)
- Django logs can be configured via `LOGGING` in settings.

## Performance tips
- Serve static and media through Nginx (not Django).
- Use database indexing for frequently filtered fields (e.g., slug, publication_year).
- Cache heavy queries or templates (add caching backend).

> If you cannot resolve an issue, include relevant logs, steps to reproduce and environment details when asking for help.