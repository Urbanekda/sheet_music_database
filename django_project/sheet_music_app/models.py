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

    CAST_CHOICES = [
        ("SATB", "SATB"),
        ("SSATB", "SSATB"),
        ("SSAA", "SSAA"),
        ("SSAB", "SSAB"),
        ("SSA", "SSA"),
        ("SAT", "SAT"),
        ("SAB", "SAB"),
        ("UNISON", "Unisono"),
        ("OTHER", "Jiné")
    ]

    SEASON_CHOICES = [
        ("ADVENT", "Advent"),
        ("CHRISTMAS", "Vánoce"),
        ("LENT", "Půst"),
        ("EASTER", "Velikonoce"),
        ("PENTECOST", "Letnice"),
        ("HOLY_TRINITY", "Nejsvětější Trojice"),
        ("INTERLUDE", "Mezidobí"),
        ("OTHER", "Žádné")
    ]

    USE_CHOICES = [
        ("HYMNS", "Chvalozpěvy"),
        ("EUCHARIST", "Eucharistie"),
        ("HOLY_SPIRIT", "Duch Svatý"),
        ("VIRGIN_MARY", "Panna Maria"),
        ("SAINTS", "Svatí"),
        ("WEDDINGS", "Svatební obřady"),
        ("FUNERAL", "Pohřebí obřady"),
        ("FOLK", "Lidové písně"),
        ("MINE", "Hornické písně"),
        ("OTHER", "Ostatní")
    ]


    title = models.CharField(max_length=200)
    composer = models.CharField(max_length=200)
    arranger = models.CharField(max_length=200, blank=True, null=True)
    cast = models.CharField(choices=CAST_CHOICES, blank=True, null=True)
    season = models.CharField(choices=SEASON_CHOICES, blank=True, null=True)
    use = models.CharField(choices=USE_CHOICES, blank=True, null=True)
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

