import requests
import urllib.parse 
from django.shortcuts import render
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
from integrations.tmdb.client import TMDBClient
from integrations.aws.client import AWSClient 

def emitir_evento_aws(request):
    if request.method == "GET":
        movie_id = request.GET.get('id')
        movie_title = request.GET.get('title', 'Filme Desconhecido')
        tipo_acao = request.GET.get('action', 'added_to_collection') 

        if movie_id:
            aws = AWSClient()
            aws.publish_movie_event(
                event_type=f"movie.{tipo_acao}",
                movie_id=movie_id,
                movie_title=movie_title
            )
            return JsonResponse({"status": "Evento enviado para a AWS local com sucesso!"})
            
    return JsonResponse({"erro": "Requisição inválida"}, status=400)

@csrf_exempt
def backup_poster_to_s3_view(request):
    movie_id = request.GET.get('id')
    poster_path_bruto = request.GET.get('poster_path')
    
    if movie_id and poster_path_bruto:
        poster_path = urllib.parse.unquote(poster_path_bruto).strip()
        
        if not poster_path.startswith('/'):
            poster_path = f"/{poster_path}"
            
        tmdb_image_url = f"https://tmdb.org{poster_path}"
        
        try:
            response = requests.get(tmdb_image_url, timeout=5)
            if response.status_code == 200:
                aws = AWSClient()
                file_name = f"movie_{movie_id}.jpg"
                s3_link = aws.upload_poster_to_s3(file_name, response.content)
                return JsonResponse({"status": "sucesso", "s3_url": s3_link})
            else:
                print(f"⚠️ [TMDB] Imagem não encontrada para o filme {movie_id}. Status: {response.status_code}")
                return JsonResponse({"status": "aviso", "mensagem": "Filme não possui imagem oficial no TMDB."}, status=200)
        except Exception as e:
            print(f"❌ [S3 ERROR] Falha no processamento: {e}")
            return JsonResponse({"status": "erro", "detalhes": str(e)}, status=500)
            
    return JsonResponse({"status": "erro", "mensagem": "Parâmetros inválidos"}, status=400)

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

def favorites_view(request):
    """Renderiza a página que exibe os filmes favoritados pelo usuário"""
    return render(request, 'catalog/favorites.html')

def watched(request):
    """Renderiza a página de filmes assistidos."""
    return render(request, 'catalog/watched.html')
