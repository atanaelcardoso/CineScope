from django.urls import path
from . import views, web_views

urlpatterns = [
    path('', web_views.index, name='catalog_index'),
    path('api/filmes/', views.index, name='catalog_movies_api'),
]