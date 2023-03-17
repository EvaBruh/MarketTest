from django.db import models


class Audd(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=150, verbose_name='Название трека')
    artist = models.CharField(max_length=150, verbose_name='Исполнитель')
    genre = models.CharField(max_length=150, verbose_name='Жанр')
    style = models.CharField(max_length=150, verbose_name='Стиль')
    release = models.DateField(verbose_name='Дата выхода')
    text = models.TextField(max_length=1000, verbose_name='Текст песни')

