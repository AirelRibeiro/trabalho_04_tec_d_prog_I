import pandas as pd
# Lê dos arquivos CSV
escolas_df = pd.read_csv("data/escolas.csv")
subprefeituras_df = pd.read_csv("data/subprefeituras.csv")
material_didatico_df = pd.read_csv("data/material_didatico.csv")

# Padronização dos dados

# Converte nomes de colunas para snake_case
escolas_df.columns = [unidecode(col.lower()) for col in escolas_df.columns]
subprefeituras_df.columns = [
    unidecode(col.lower()) for col in subprefeituras_df.columns
]
material_didatico_df.columns = [
    unidecode(col.lower()) for col in material_didatico_df.columns
]

