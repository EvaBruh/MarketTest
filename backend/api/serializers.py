from rest_framework import serializers

from .models import SongData, Discogs


class TrackInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongData
        fields = '__all__'


class DiscogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discogs
        fields = '__all__'