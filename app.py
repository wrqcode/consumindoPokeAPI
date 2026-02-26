import http.client
import json
from urllib.parse import urlparse
import pandas as pd

def fazer_get(host, path):
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", path)
    response = conn.getresponse()
    if response.status == 200:
        data = response.read().decode()
        conn.close()
        return json.loads(data)
    conn.close()
    return None

lista = fazer_get("pokeapi.co", "/api/v2/pokemon?limit=20&offset=0")

dados = []

for item in lista["results"]:
    parsed = urlparse(item["url"])
    pokemon = fazer_get(parsed.netloc, parsed.path)

    if pokemon:
        tipos_lista = []

        for t in pokemon["types"]:
            nome_tipo = t["type"]["name"]
            tipos_lista.append(nome_tipo)

        tipos = ", ".join(tipos_lista)

        dados.append({
            "ID": pokemon["id"],
            "Nome": pokemon["name"],
            "Altura": pokemon["height"],
            "Peso": pokemon["weight"],
            "Tipos": tipos,
            "Base Experience": pokemon["base_experience"]
        })

df = pd.DataFrame(dados)

df.to_excel("pokemons.xlsx", index=False)