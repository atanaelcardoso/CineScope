from django.http import JsonResponse

from integrations.tmdb.client import TMDBClient


def index(request):
    query = request.GET.get('query', '').strip()
    try:
        page = max(1, int(request.GET.get('page', 1)))
    except (TypeError, ValueError):
        page = 1

    client = TMDBClient()
    movies_data = (
        client.search_movies(query=query, page=page)
        if query
        else client.get_popular_movies(page=page)
    )

    if movies_data is None:
        return JsonResponse(
            {'erro': 'Não foi possível conectar ao TMDB. Verifique o token e os logs do servidor.'},
            status=502,
        )

    return JsonResponse(movies_data)
