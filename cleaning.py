import pandas as pd
from unidecode import unidecode
import re


# Lê dos arquivos CSV
escolas_df = pd.read_csv("data/escolas.csv")
subprefeituras_df = pd.read_csv("data/subprefeituras.csv")
material_didatico_df = pd.read_csv("data/material_didatico.csv")

# Padronização dos dados

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

print(join_tabelas, end="\n\n")
