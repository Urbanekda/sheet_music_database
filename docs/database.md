# Database

## Overview
- Development: `db.sqlite3` present in repo for convenience.
- Production: PostgreSQL (configured in [`settings.py`](../django_project/sheet_music_database/settings.py); env vars `POSTGRES_*`).

## Schema overview
Models are defined in the app model file:
- [`django_project/sheet_music_app/models.py`](../django_project/sheet_music_app/models.py)

Important model concepts (typical):
- `Sheet` (or similarly named model): stores metadata fields such as `title`, `composer`, `publisher`, `isbn`, `description`, `publication_year`, `slug`, `sheet_file` (FileField), `preview_image` (ImageField), `public` flag, timestamps.
  - See templates referencing fields in [edit_sheet.html](../django_project/sheet_music_app/templates/edit_sheet.html) and [sheet_profile.html](../django_project/sheet_music_app/templates/sheet_profile.html).

## Relationships
- Most data is likely single-table `Sheet` plus User relation for owner/uploader (ForeignKey to `auth.User`) if implemented.
- Refer to [`models.py`](../django_project/sheet_music_app/models.py) for exact fields and relationships.

## Migrations
- Create/run migrations with Django manage:
```bash
python django_project/manage.py makemigrations
python django_project/manage.py migrate
```
- Migrations are tracked in the app `migrations/` folder.

## Backup & restore
- For SQLite: copy `db.sqlite3` file as a backup.
- For PostgreSQL: use `pg_dump`/`pg_restore` or scheduled dumps.
- Repository includes `postgres_backup/` directory (see `postgres_backup/daily/`) for backups in this workspace.

Example backup:
```bash
pg_dump -U $POSTGRES_USER -h $POSTGRES_HOST -F c -b -v -f sheetmusic.dump $POSTGRES_DB
```

Restore example:
```bash
pg_restore -U $POSTGRES_USER -h $POSTGRES_HOST -d $POSTGRES_DB sheetmusic.dump
```

> NOTE: `POSTGRES_BACKUP_GENERATIONS = 3` is set in [`settings.py`](django_project/sheet_music_database/settings.py) — used by any backup scripts you may add.