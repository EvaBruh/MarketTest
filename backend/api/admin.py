from django.contrib import admin

from .models import SongData, Discogs


class AuddAdmin(admin.ModelAdmin):

    class Meta:
        model = SongData

    list_display = ('id', 'title', 'artist', 'genre', 'style', 'release_date', 'lyrics')
    list_display_links = ('id', 'title', 'artist', 'genre', 'style', 'release_date', 'lyrics')
    search_fields = ('id', 'title', 'artist', 'genre', 'style', 'release_date', 'lyrics')


class DiscogsAdmin(admin.ModelAdmin):

    class Meta:
        model = Discogs

    list_display = ('id', 'title', 'artist', 'year', 'label', 'catno', 'format')
    list_display_links = ('id', 'title', 'artist', 'year', 'label', 'catno', 'format')
    search_fields = ('id', 'title', 'artist', 'year', 'label', 'catno', 'format')


admin.site.register(SongData, AuddAdmin)
admin.site.register(Discogs, DiscogsAdmin)