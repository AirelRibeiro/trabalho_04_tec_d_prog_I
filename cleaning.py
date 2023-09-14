import pandas as pd
from unidecode import unidecode

from e_rotas.data_analyzer_class import DataAnalyzer
from e_rotas.data_normalizer_class import DataNormalizer
from e_rotas.plot_manager_class import PlotManager

# Lê dos arquivos CSV
escolas_df = pd.read_csv("data/escolas.csv")
subprefeituras_df = pd.read_csv("data/subprefeituras.csv")
material_didatico_df = pd.read_csv("data/material_didatico.csv")

# Instânciando classes
data_manager = DataNormalizer()
data_analyzer = DataAnalyzer()
data_plot_manager = PlotManager()

# Converte colunas em snake_case
escolas_df.columns = [
    unidecode(col.lower().strip()) for col in escolas_df.columns]
subprefeituras_df.columns = [
    unidecode(col.lower().strip()) for col in subprefeituras_df.columns]
material_didatico_df.columns = [
    unidecode(col.lower().strip()) for col in material_didatico_df.columns]

# Formata IDs com 3 caracteres
escolas_df["id"] = escolas_df["id"].astype(str).str.zfill(3)
material_didatico_df["id"] = (
    material_didatico_df["id"].astype(str).str.zfill(3))

material_didatico_df["quantidade"] = pd.to_numeric(material_didatico_df["quantidade"].fillna(
    0), errors='coerce')

material_didatico_df["quantidade"].fillna(0, inplace=True)

# Normaliza endereços usando função 'padronizar_endereco'
escolas_df["endereco"] = escolas_df["endereco"].map(
    DataNormalizer.normalize_endereco)

# Normaliza escolas
escolas_df["escolas_postos"] = escolas_df["escolas_postos"].map(
    lambda x: "".join([unidecode(palavra) for palavra in x]))

# Normaliza bairros
escolas_df["bairro"] = escolas_df["bairro"].map(
    lambda x: "".join([unidecode(palavra) for palavra in x]))

# Normaliza latitude e longitude
escolas_df["lat"] = escolas_df["lat"].apply(
    lambda x: float(x.replace(",", ".")).__round__(5)
)
escolas_df["lon"] = escolas_df["lon"].apply(
    lambda x: float(x.replace(",", ".")).__round__(5)
)

# Normaliza subprefeituras
subprefeituras_df = subprefeituras_df.map(
    DataNormalizer.normalize_subprefeituras)

# Ligando tabelas e normalizando nome da tabela de subprefeitura
subprefeituras_df.rename(columns={"nome": "bairro"}, inplace=True)

# Merge das tabelas
join_escola_material = pd.merge(
    escolas_df, material_didatico_df, on="id", how="inner")

join_tabelas = pd.merge(join_escola_material, subprefeituras_df,
                        on="bairro", how="inner")

# Renomeando colunas do dataframe
join_tabelas.rename(
    columns={"id": "id_escola", "escolas_postos": "nome_da_escola", "endereco": "logradouro_da_entrega", "lat": "latitude", "lon": "longitude", "quantidade": "quantidade_material"}, inplace=True)

# Normalizando escola
join_tabelas["tipo_da_escola"] = join_tabelas["nome_da_escola"].apply(
    DataNormalizer.normalize_escolas)

# Exemplo de regex usando str replace
join_tabelas["numero"] = join_tabelas['logradouro_da_entrega'].str.extract(
    r'(\d+|(?<=\bS/NO\b)[^\d\s]+|(?<=\bS/NO\b)\s*\d+|\bS/NO\b)')


join_tabelas["numero"].fillna('S/NO', inplace=True)

# Exemplo de regex usando str replace
join_tabelas['logradouro_da_entrega'] = join_tabelas['logradouro_da_entrega'].str.replace(
    r'(\d+|(?<=\bS/NO\b)[^\d\s]+|(?<=\bS/NO\b)\s*\d+|\bS/NO\b|\bS/NDEG\b|\bS/N\b|\b,.*\b)', '', regex=True).str.rstrip(', ').str.strip()

join_tabelas = join_tabelas.reindex(
    columns=join_tabelas.columns[[0, 1, -2, 3, -1, 2, 7, 4, 5, 6]])

join_tabelas = join_tabelas.drop_duplicates(
    subset=["id_escola", "subprefeitura"])

# Agora, calcule a média agrupada por 'subprefeitura'
group_prefei_material = join_tabelas.groupby('subprefeitura')[
    'quantidade_material'].sum()

join_tabelas = join_tabelas[join_tabelas['quantidade_material'] > 0]

# Obtem a próxima latitude e longitude
join_tabelas['next_latitude'] = join_tabelas['latitude'].shift(-1)
join_tabelas['next_longitude'] = join_tabelas['longitude'].shift(-1)

# Calculo da distância entre a escola atual e a próxima
join_tabelas['distancia'] = join_tabelas.apply(lambda row: data_analyzer.haversine(
    row['latitude'], row['longitude'], row['next_latitude'], row['next_longitude']), axis=1)

# Plotando gráfico
pontos_entrega_df = join_tabelas[['latitude', 'longitude']]

best_route = data_analyzer.nearest_neighbor(pontos_entrega_df)
ordered_df = join_tabelas.iloc[best_route].reset_index(drop=True)

data_plot_manager.plot_route(ordered_df)

map_obj = data_plot_manager.plot_on_map(ordered_df)
map_obj.save('map.html')

# Exportando dados para csv
join_tabelas.to_csv('rotas_seguidas.csv', index=False)
group_prefei_material.to_csv('total_material.csv')
