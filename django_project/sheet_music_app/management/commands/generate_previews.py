from django.core.management.base import BaseCommand
from django.db.models import Q

from sheet_music_app.models import Sheet, generate_pdf_preview


class Command(BaseCommand):
    help = "Backfill preview_image for existing sheets with a PDF sheet_file and no preview yet."

    def handle(self, *args, **options):
        sheets = Sheet.objects.filter(Q(preview_image="") | Q(preview_image__isnull=True))
        generated = 0
        skipped = 0

        for sheet in sheets:
            preview = generate_pdf_preview(sheet.sheet_file)
            if not preview:
                skipped += 1
                continue
            sheet.preview_image = preview
            sheet.save(update_fields=["preview_image"])
            generated += 1
            self.stdout.write(f"Generated preview for '{sheet.title}'")

        self.stdout.write(self.style.SUCCESS(
            f"Done. Generated {generated} preview(s), skipped {skipped} non-PDF sheet(s)."
        ))
