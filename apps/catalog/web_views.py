from django.shortcuts import render

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

    context = {
        'termo_pesquisa': query,
        'pagina_atual': page,
        'pagina_anterior': page - 1 if page > 1 else None,
        'proxima_pagina': page + 1,
    }
    if movies_data is None:
        context['error'] = 'Não foi possível carregar os filmes. Verifique a conexão e o token do TMDB.'
        return render(request, 'catalog/index.html', context, status=502)

    context['movies'] = movies_data.get('results', [])
    return render(request, 'catalog/index.html', context)
