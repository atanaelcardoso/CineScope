from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='catalog_index'),
    path('favoritos/', views.favorites_view, name='catalog_favorites'),
    path('assistidos/', views.watched, name='catalog_watched'),  # <-- Rota de assistidos conectada!
]