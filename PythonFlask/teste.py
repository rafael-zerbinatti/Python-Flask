import urllib.request, json

url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=758b036ebdeae222d06885d1e3fb555a"

resposta = urllib.request.urlopen(url)

dados = resposta.read()

jsondata = json.loads(dados)

print(jsondata['results'])