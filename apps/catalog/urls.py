from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='catalog_index'),
    path('favoritos/', views.favorites_view, name='catalog_favorites'),
    path('assistidos/', views.watched, name='catalog_watched'),
    path('api/evento-aws/', views.emitir_evento_aws, name='api_evento_aws'),
]