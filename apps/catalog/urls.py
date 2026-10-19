from django.urls import path
from . import api_views, web_views

urlpatterns = [
    path('', web_views.index, name='catalog_index'),
    path('api/filmes/', api_views.index, name='catalog_movies_api'),
]