from django.urls import path, include
from .views import index, TrackList, TrackDetail
from rest_framework import routers
from .views import AuddView

# Пути на django rest API

router = routers.SimpleRouter()
router.register('api/audd', AuddView)

urlpatterns = [
     path('', index),
     path('', include(router.urls)),
]