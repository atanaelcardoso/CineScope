from django.http import JsonResponse
from integrations.tmdb.client import TMDBClient

def index(request):
    
    client = TMDBClient()
    
    dados_dos_filmes = client.get_popular_movies()

    if dados_dos_filmes is None:
        return JsonResponse({"erro": "Não foi possível conectar ao TMDB. Verifique o token no arquivo .env ou os logs do Docker."}, status=500)
    
    return JsonResponse(dados_dos_filmes)
