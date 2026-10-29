import os
import pytest
from unittest.mock import patch, Mock
from django.urls import reverse
from requests.exceptions import ConnectionError as RequestsConnectionError

@pytest.mark.django_db
def test_pagina_inicial_carrega_com_sucesso(client):
    url = reverse('catalog_index')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
@patch.dict(os.environ, {'TMDB_BEARER_TOKEN': 'test-token'})
@patch('integrations.tmdb.client.requests.get')
def test_homepage_shows_error_when_tmdb_is_unavailable(mock_get, client):
    mock_get.side_effect = RequestsConnectionError('TMDB unavailable')
    
    url = reverse('catalog_index')
    response = client.get(url)
    
    assert response.status_code == 200
    assert "Não foi possível carregar os filmes" in response.content.decode('utf-8')

@pytest.mark.django_db
@patch.dict(os.environ, {'TMDB_BEARER_TOKEN': 'test-token'})
@patch('integrations.aws.client.boto3.client')
def test_movies_api_aws_events_returns_success(mock_boto, client):
    mock_sns = Mock()
    mock_sns.publish.return_value = {'MessageId': '12345'}
    mock_boto.return_value = mock_sns

    url = reverse('api_evento_aws')
    response = client.get(f"{url}?id=1058424&title=SpiderMan&action=favorited")
    
    assert response.status_code == 200
    assert 'status' in response.json()

@patch('apps.catalog.views.AWSClient')
@patch('apps.catalog.views.requests.get')
def test_backup_poster_uploads_tmdb_image_to_s3(mock_get, mock_aws, client):
    mock_get.return_value = Mock(status_code=200, content=b'image-content')
    mock_aws.return_value.upload_poster_to_s3.return_value = (
        'http://localhost:4566/cinescope-media-bucket/posters/movie_123.jpg'
    )

    url = reverse('api_backup_s3')
    response = client.get(f"{url}?id=123&poster_path=poster.jpg")

    assert response.status_code == 200
    assert response.json() == {
        'status': 'sucesso',
        's3_url': 'http://localhost:4566/cinescope-media-bucket/posters/movie_123.jpg',
    }
    mock_get.assert_called_once_with(
        'https://image.tmdb.org/t/p/original/poster.jpg',
        timeout=5,
    )
    mock_aws.return_value.upload_poster_to_s3.assert_called_once_with(
        'movie_123.jpg',
        b'image-content',
    )

@patch('apps.catalog.views.AWSClient')
@patch('apps.catalog.views.requests.get')
def test_backup_poster_reports_s3_upload_failure(mock_get, mock_aws, client):
    mock_get.return_value = Mock(status_code=200, content=b'image-content')
    mock_aws.return_value.upload_poster_to_s3.return_value = None

    url = reverse('api_backup_s3')
    response = client.get(f"{url}?id=123&poster_path=poster.jpg")

    assert response.status_code == 500
    assert response.json() == {
        'status': 'erro',
        'mensagem': 'Falha ao enviar imagem para o S3.',
    }
