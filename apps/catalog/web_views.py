from django.shortcuts import render

from integrations.tmdb.client import TMDBClient


def index(request):
    movies_data = TMDBClient().get_popular_movies()

    if movies_data is None:
        return render(
            request,
            'catalog/index.html',
            {'error': 'Não foi possível carregar os filmes. Verifique a conexão e o token do TMDB.'},
            status=502,
        )

    return render(
        request,
        'catalog/index.html',
        {'movies': movies_data.get('results', [])},
    )
