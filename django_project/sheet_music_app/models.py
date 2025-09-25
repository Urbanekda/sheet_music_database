from django.db import models
from django.utils.text import slugify

class Sheet(models.Model):
    
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
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not set
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
    
class Meta:
    ordering = ['-date_created']

