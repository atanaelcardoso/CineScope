import os
import requests

class TMDBClient:
    def __init__(self):
        self.token = os.getenv('TMDB_BEARER_TOKEN')
        self.base_url = 'https://api.themoviedb.org/3'
        
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'accept': 'application/json'
        }

    def _get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=5)
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na chamada do TMDB [{endpoint}]: {e}")
            return None

    def get_popular_movies(self, page=1):
        params = {
            'language': 'pt-BR', 
            'page': page
        }
        return self._get('movie/popular', params=params)
