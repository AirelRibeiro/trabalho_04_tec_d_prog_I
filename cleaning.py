import matplotlib.pyplot as plt
import pandas as pd
from unidecode import unidecode
import re


# Lê dos arquivos CSV
escolas_df = pd.read_csv("data/escolas.csv")
subprefeituras_df = pd.read_csv("data/subprefeituras.csv")
material_didatico_df = pd.read_csv("data/material_didatico.csv")

# Converte colunas em snake_case
escolas_df.columns = [
    unidecode(col.lower().strip()) for col in escolas_df.columns
]
subprefeituras_df.columns = [
    unidecode(col.lower().strip()) for col in subprefeituras_df.columns
]
material_didatico_df.columns = [
    unidecode(col.lower().strip()) for col in material_didatico_df.columns
]

# Formata IDs com 3 caracteres
escolas_df["id"] = escolas_df["id"].astype(str).str.zfill(3)
material_didatico_df["id"] = (
    material_didatico_df["id"].astype(str).str.zfill(3))

material_didatico_df["quantidade"] = pd.to_numeric(material_didatico_df["quantidade"].fillna(
    0), errors='coerce')

material_didatico_df["quantidade"].fillna(0, inplace=True)


def padronizar_endereco(endereco):
    palavras = endereco.split()

    # Retira caracteres especiais
    endereco_padronizado = " ".join(
        [unidecode(palavra) for palavra in palavras]
    )
    endereco_padronizado = endereco_padronizado.upper()

    # Padroniza o nome dos logradouros sem abreviação
    endereco_padronizado = re.sub(r"\bR\.?\b", "RUA", endereco_padronizado)
    endereco_padronizado = re.sub(
        r"\bAV\.?\b", "AVENIDA", endereco_padronizado
    )
    endereco_padronizado = re.sub(
        r"\bTR\.?\b", "TRAVESSA", endereco_padronizado
    )
    endereco_padronizado = re.sub(
        r"\bESTR\.?\b", "ESTRADA", endereco_padronizado
    )
    endereco_padronizado = re.sub(
        r"\bPÇA\.?\b", "ESTRADA", endereco_padronizado
    )
    return endereco_padronizado.replace(".", "")


def padronizar_subprefeituras(subprefeituras):
    palavras = subprefeituras.split()

    # Retira caracteres especiais
    subprefeituras_padronizado = " ".join(
        [unidecode(palavra) for palavra in palavras]
    )

    return subprefeituras_padronizado.upper()


# Normaliza endereços usando função 'padronizar_endereco'
escolas_df["endereco"] = escolas_df["endereco"].map(padronizar_endereco)

# Normaliza escolas
escolas_df["escolas_postos"] = escolas_df["escolas_postos"].map(
    lambda x: "".join([unidecode(palavra) for palavra in x])
)

# Normaliza bairros
escolas_df["bairro"] = escolas_df["bairro"].map(
    lambda x: "".join([unidecode(palavra) for palavra in x])
)

# Normaliza latitude e longitude
escolas_df["lat"] = escolas_df["lat"].apply(
    lambda x: float(x.replace(",", ".")).__round__(5)
)
escolas_df["lon"] = escolas_df["lon"].apply(
    lambda x: float(x.replace(",", ".")).__round__(5)
)

# Normaliza subprefeituras usando função 'padronizar_subprefeituras'
subprefeituras_df = subprefeituras_df.map(
    padronizar_subprefeituras)

# Ligando tabelas e normalizando nome da tabela de subprefeitura
subprefeituras_df.rename(columns={"nome": "bairro"}, inplace=True)
join_escola_material = pd.merge(
    escolas_df, material_didatico_df, on="id", how="inner")
join_tabelas = pd.merge(join_escola_material, subprefeituras_df,
                        on="bairro", how="inner")

join_tabelas.rename(
    columns={"id": "id_escola", "escolas_postos": "nome_da_escola", "endereco": "logradouro_da_entrega", "lat": "latitude", "lon": "longitude", "quantidade": "quantidade_material"}, inplace=True)

# Padronização das escolas


def padronizar_escolas(escolas):
    nome = escolas.upper().strip()

    if "CIEP" in nome or "CENTRO INTEGRADO DE EDUCACAO PUBLICA" in nome:
        return "CIEP"
    elif nome.startswith("EM ") or nome.startswith("E.M. ") or nome.startswith("E.M ") or "ESCOLA MUNICIPAL" in nome:
        return "EM"
    else:
        return "COLÉGIO"


join_tabelas["tipo_da_escola"] = join_tabelas["nome_da_escola"].apply(
    padronizar_escolas)

join_tabelas["numero"] = join_tabelas['logradouro_da_entrega'].str.extract(
    r'(\d+|\bS/NO\b)')

join_tabelas["numero"].fillna('S/NO', inplace=True)

join_tabelas['logradouro_da_entrega'] = join_tabelas['logradouro_da_entrega'].str.replace(
    r'\d+|S/NO', '', regex=True).str.rstrip(', ').str.strip()

join_tabelas = join_tabelas.reindex(
    columns=join_tabelas.columns[[0, 1, -2, 3, -1, 2, 7, 4, 5, 6]])


# Agora, calcule a média agrupada por 'subprefeitura'
group_prefei_material = join_tabelas.groupby('subprefeitura')[
    'quantidade_material'].sum()

join_tabelas.to_csv('rotas_seguidas.csv', index=False)

group_prefei_material.to_csv('total_material.csv')


# print(group_prefei_material, end="\n\n")
# print(join_tabelas["longitude"].tolist(), end="\n\n")

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(join_tabelas["longitude"].head(100).tolist(),
            join_tabelas["latitude"].head(100).tolist(), c='red', label='Rota')

plt.plot(join_tabelas["longitude"].head(100).tolist(), join_tabelas["latitude"].head(100).tolist(),
         c='blue',  linestyle='-', label='Escolas')

plt.xlabel('longitude')
plt.ylabel('latitude')
plt.title('Rota Otimizada de Entrega')
plt.legend()
plt.grid(True)
plt.show()
