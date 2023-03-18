from django.urls import path, include
from .views import index, UploadFileView, DiscogsApi
from rest_framework import routers


# Пути на django API
router = routers.SimpleRouter()
router.register('api/audd', UploadFileView, basename='audd')
router.register('api/discogs', DiscogsApi, basename='discogs')
# просто пути на страницы
urlpatterns = [
     path('', index),
     path('', include(router.urls)),
]