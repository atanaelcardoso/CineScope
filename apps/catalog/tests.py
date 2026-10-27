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
