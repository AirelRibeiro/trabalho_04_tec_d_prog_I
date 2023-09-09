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


# Formata IDs da escola com 3 caracteres
escolas_df["id"] = escolas_df["id"].astype(str).str.zfill(3)


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
    return endereco_padronizado


# Normaliza endereços usando função 'padronizar_endereco'
escolas_df["endereco"] = escolas_df["endereco"].map(padronizar_endereco)

print("teste")
print("teste novo")
