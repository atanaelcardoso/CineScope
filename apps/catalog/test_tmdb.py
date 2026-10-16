import os
from unittest.mock import Mock, patch

from django.test import SimpleTestCase
from requests.exceptions import ConnectionError as RequestsConnectionError

from integrations.tmdb.client import TMDBClient


class TMDBClientTests(SimpleTestCase):
    @patch.dict(os.environ, {'TMDB_BEARER_TOKEN': 'test-token'})
    @patch('integrations.tmdb.client.requests.get')
    def test_get_popular_movies_uses_tmdb_api_v3(self, mock_get):
        response = Mock()
        response.json.return_value = {'results': [{'title': 'Filme teste'}]}
        mock_get.return_value = response

        result = TMDBClient().get_popular_movies()

        self.assertEqual(result, {'results': [{'title': 'Filme teste'}]})
        mock_get.assert_called_once_with(
            'https://api.themoviedb.org/3/movie/popular',
            headers={
                'Authorization': 'Bearer test-token',
                'accept': 'application/json',
            },
            params={'language': 'pt-BR', 'page': 1},
            timeout=5,
        )


class CatalogViewTests(SimpleTestCase):
    @patch.dict(os.environ, {'TMDB_BEARER_TOKEN': 'test-token'})
    @patch('integrations.tmdb.client.requests.get')
    def test_homepage_renders_popular_movies(self, mock_get):
        response = Mock()
        response.json.return_value = {
            'results': [
                {
                    'id': 1,
                    'title': 'Filme teste',
                    'poster_path': '/poster.jpg',
                    'overview': 'Uma sinopse.',
                },
            ],
        }
        mock_get.return_value = response

        result = self.client.get('/', HTTP_HOST='localhost')

        self.assertEqual(result.status_code, 200)
        self.assertContains(result, 'CineScope')
        self.assertContains(result, 'Filme teste')
        self.assertContains(result, 'Uma sinopse.')
        self.assertContains(result, 'https://image.tmdb.org/t/p/w500/poster.jpg')

    @patch.dict(os.environ, {'TMDB_BEARER_TOKEN': 'test-token'})
    @patch('integrations.tmdb.client.requests.get')
    def test_movies_api_keeps_json_response(self, mock_get):
        response = Mock()
        response.json.return_value = {'results': [{'title': 'Filme teste'}]}
        mock_get.return_value = response

        result = self.client.get('/api/filmes/', HTTP_HOST='localhost')

        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            result.json(),
            {'results': [{'title': 'Filme teste'}]},
        )

    @patch.dict(os.environ, {'TMDB_BEARER_TOKEN': 'test-token'})
    @patch('integrations.tmdb.client.requests.get')
    def test_homepage_shows_error_when_tmdb_is_unavailable(self, mock_get):
        mock_get.side_effect = RequestsConnectionError('TMDB unavailable')

        result = self.client.get('/', HTTP_HOST='localhost')

        self.assertEqual(result.status_code, 502)
        self.assertContains(result, 'Não foi possível carregar os filmes', status_code=502)
