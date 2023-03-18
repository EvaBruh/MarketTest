from django.db import models


# Модель для api/audd
class SongData(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=255, null=True, blank=True)
    style = models.CharField(max_length=255, null=True, blank=True)
    lyrics = models.TextField(null=True, blank=True)
    gen_tracklist = models.JSONField(null=True)
    gen_url = models.JSONField(null=True)

    def __str__(self):
        return f'{self.artist} - {self.title}'


# Модель для api/discogs
class Discogs(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(null=True, max_length=255)
    year = models.IntegerField(null=True)
    label = models.CharField(max_length=255)
    catno = models.CharField(max_length=255)
    format = models.CharField(max_length=255)

    def __str__(self):
        return self.title