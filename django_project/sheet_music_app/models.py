from django.db import models
from django.utils.text import slugify

class Tag(models.Model):
    """Simple tag entity for labeling sheets."""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Sheet(models.Model):
    """Represents a single sheet-music record.

    Notes:
    - Choices below drive both form select options and display labels via
      get_FOO_display in templates.
    - Slug is auto-generated from title in save() if not provided.
    - Public flag controls visibility for non-staff users.
    """
    
    RELIGIOUS = "REL"
    CHORAL = "CHO"
    JAZZ = "JAZ"
    POPULAR = "POP"
    CLASSICAL = "CLA"
    SECULAR = "SEC"
    FOLCLORE = "FOL"

    GENRE_CHOICES = [
        (RELIGIOUS, "Duchovní"),
        (CHORAL, "Sborová"),
        (JAZZ, "Jazzová"),
        (POPULAR, "Populární"),
        (CLASSICAL, "Klasická"),
        (SECULAR, "Světská"),
        (FOLCLORE, "Folklórní"),
    ]

    # Difficulty is stored as a char code ("1".."5"). The labels are localized.
    DIFFICULTY_CHOICES = [
        (1, 'Velmi snadná'),
        (2, 'Snadná'),
        (3, 'Střední'),
        (4, 'Obtížná'),
        (5, 'Velmi obtížná'),
    ]

    title = models.CharField(max_length=200)
    composer = models.CharField(max_length=200)
    arranger = models.CharField(max_length=200, blank=True, null=True)
    genre = models.CharField(choices=GENRE_CHOICES, blank=True, null=True)


    # Stored as a single-character code for simplicity. Template uses
    # get_difficulty_level_display to show human label.
    difficulty_level = models.CharField(choices=DIFFICULTY_CHOICES, blank=True, null=True, max_length=1)
    publication_year = models.IntegerField(blank=True, null=True)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    modified_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='modified_sheets')
    sheet_file = models.FileField()
    preview_image = models.ImageField(blank=True, null=True)
    public = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    # Tags are editor-managed and visible to all users
    tags = models.ManyToManyField(Tag, blank=True, related_name="sheets")
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not set. Ensures uniqueness by suffixing
        # "-2", "-3", ... when a collision is found.
        if not self.slug and self.title:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 2
            # Ensure uniqueness
            while Sheet.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
# NOTE: This Meta class is currently at module scope, so its ordering will NOT apply
# to the Sheet model. If you want default ordering on queries, indent this class so it
# lives inside Sheet (as an inner class). Left unchanged here intentionally.
class Meta:
    ordering = ['-date_created'],
    permissions = [
        ("can_view_private", "Can view private sheets"),
    ]

