# Deployment

This section outlines production deployment using Docker, Gunicorn and Nginx. Several files are relevant:
- [Dockerfile](../Dockerfile)
- [docker-compose.yml](../docker-compose.yml)
- [entrypoint.sh](../django_project/entrypoint.sh)
- [nginx.conf](../nginx.conf)
- Certbot integration: [`Dockerfile.certbot`](../Dockerfile.certbot) and `certbot/` folder.

## Deployment architecture
- Nginx as reverse proxy and static file server.
- Gunicorn runs Django app (see `entrypoint.sh` -> `gunicorn ... sheet_music_database.wsgi:application`).
- PostgreSQL as database (external or container).
- Media files mounted on persistent volume or stored in object storage.

## Step-by-step (simple Docker Compose)
1. Provide production env vars (SECRET_KEY, DB credentials, ALLOWED_HOSTS).
2. Build and start:
```bash
docker-compose up --build -d
```
3. Check logs and containers:
```bash
docker-compose logs -f
```

## SSL/TLS (Certbot, Nginx)
- `nginx.conf` contains server directives. Use Certbot to request certificates and configure Nginx to serve with TLS.
- The repo contains `Dockerfile.certbot` and `certbot/` folder with scripts and conf placeholders.

## Gunicorn process
The container runs:
```bash
python -m gunicorn --bind 0.0.0.0:8000 --workers 3 sheet_music_database.wsgi:application
```
This is started from [`entrypoint.sh`](django_project/entrypoint.sh) after `collectstatic` and `migrate`.

## Monitoring & logging
- Use Docker logs (`docker-compose logs`) and application logs (configure `LOGGING` in [`settings.py`](django_project/sheet_music_database/settings.py) if needed).
- Consider external monitoring (Prometheus, Sentry) for error tracking.

## Rollback
- Rolling back can be done by re-deploying the previous image tag or docker-compose config and restoring database from backup if schema changes require it.
- Always test migration rollback strategy in staging.

> WARNING: When changing DB migrations in production, test in staging and ensure backups exist before running `migrate`.