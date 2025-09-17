from django.db import models

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

    title = models.CharField(max_length=200)
    composer = models.CharField(max_length=200)
    arranger = models.CharField(max_length=200, blank=True, null=True)
    genre = models.CharField(choices=GENRE_CHOICES, blank=True, null=True)


    difficulty_level = models.IntegerChoices(choices=[(i, str(i)) for i in range(1, 10)])
    publication_year = models.IntegerField(blank=True, null=True)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    modified_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='modified_sheets')
    sheet_file = models.FileField(upload_to='sheets/')
    
    def __str__(self):
        return self.title
    
class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Meta:
    ordering = ['-date_created']

