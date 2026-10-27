from django.urls import path
from django.views.decorators.csrf import csrf_exempt 
from . import views

urlpatterns = [
    path('', views.index, name='catalog_index'),
    path('favoritos/', views.favorites_view, name='catalog_favorites'),
    path('assistidos/', views.watched, name='catalog_watched'),
    path('api/evento-aws/', csrf_exempt(views.emitir_evento_aws), name='api_evento_aws'),
    path('api/backup-s3/', csrf_exempt(views.backup_poster_to_s3_view), name='api_backup_s3'),
]