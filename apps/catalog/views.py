from django.shortcuts import render
from integrations.tmdb.client import TMDBClient

def index(request):
    termo_pesquisa = request.GET.get('query', '').strip()
    
    try:
        pagina_atual = int(request.GET.get('page', 1))
    except (ValueError, TypeError):
        pagina_atual = 1
    
    client = TMDBClient()
    
    if termo_pesquisa:
        dados_dos_filmes = client.search_movies(query=termo_pesquisa, page=pagina_atual)
    else:
        dados_dos_filmes = client.get_popular_movies(page=pagina_atual)
        
    if dados_dos_filmes is None:
        contexto_erro = {
            "error": "Não foi possível carregar os filmes. Verifique a conexão e o token do TMDB.",
            "pagina_atual": pagina_atual,
            "termo_pesquisa": termo_pesquisa
        }
        return render(request, 'catalog/index.html', contexto_erro)
        
    lista_de_filmes = dados_dos_filmes.get('results', [])
    
    pagina_anterior = pagina_atual - 1 if pagina_atual > 1 else None
    proxima_pagina = pagina_atual + 1
    
    contexto = {
        'movies': lista_de_filmes,
        'termo_pesquisa': termo_pesquisa,
        'pagina_atual': pagina_atual,
        'pagina_anterior': pagina_anterior,
        'proxima_pagina': proxima_pagina,
    }
    
    return render(request, 'catalog/index.html', contexto)
