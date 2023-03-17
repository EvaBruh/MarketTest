from django.contrib import admin

from .models import Audd


class AuddAdmin(admin.ModelAdmin):

    class Meta:
        model = Audd

    list_display = ('id', 'name', 'artist', 'genre', 'style', 'release', 'text')
    list_display_links = ('id', 'name', 'artist', 'genre', 'style', 'release', 'text')
    search_fields = ('id', 'name', 'artist', 'genre', 'style', 'release', 'text')


admin.site.register(Audd, AuddAdmin)