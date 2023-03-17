from django.shortcuts import render
from rest_framework import viewsets, generics

from .models import Audd
from .serializers import AuddSerializer


def index(request):
    return render(request, 'index.html')


class AuddView(viewsets.ModelViewSet):
    queryset = Audd.objects.all()
    http_method_names = ['get']
    serializer_class = AuddSerializer


class TrackList(generics.ListCreateAPIView):
    queryset = Audd.objects.all()
    serializer_class = AuddSerializer


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Audd.objects.all()
    serializer_class = AuddSerializer