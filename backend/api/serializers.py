# Cards - отображение главных 6 проектов на HomePage
from rest_framework import serializers

from .models import Audd


class AuddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audd
        fields = ('id', 'name', 'artist', 'genre', 'style', 'release', 'text')