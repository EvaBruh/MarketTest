# Generated by Django 4.1.7 on 2023-03-18 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_discogs_artist'),
    ]

    operations = [
        migrations.AddField(
            model_name='songdata',
            name='gen_tracklist',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='songdata',
            name='gen_url',
            field=models.JSONField(null=True),
        ),
    ]
