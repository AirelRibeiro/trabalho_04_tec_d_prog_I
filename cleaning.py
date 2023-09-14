import pandas as pd
from unidecode import unidecode

from e_rotas.data_analyzer_class import DataAnalyzer
from e_rotas.data_normalizer_class import DataNormalizer
from e_rotas.plot_manager_class import PlotManager

# Lê dos arquivos CSV
schools_df = pd.read_csv("data/escolas.csv")
subprefectures_df = pd.read_csv("data/subprefeituras.csv")
courseware_df = pd.read_csv("data/material_didatico.csv")

# Instânciando classes
data_manager = DataNormalizer()
data_analyzer = DataAnalyzer()
data_plot_manager = PlotManager()

# Converte colunas em snake_case
schools_df.columns = [
    unidecode(col.lower().strip()) for col in schools_df.columns]
subprefectures_df.columns = [
    unidecode(col.lower().strip()) for col in subprefectures_df.columns]
courseware_df.columns = [
    unidecode(col.lower().strip()) for col in courseware_df.columns]

# Formata IDs com 3 caracteres
schools_df["id"] = schools_df["id"].astype(str).str.zfill(3)
courseware_df["id"] = (
    courseware_df["id"].astype(str).str.zfill(3))

courseware_df["quantidade"] = pd.to_numeric(courseware_df["quantidade"].fillna(
    0), errors='coerce')

courseware_df["quantidade"].fillna(0, inplace=True)

# Normaliza endereços usando função 'padronizar_endereco'
schools_df["endereco"] = schools_df["endereco"].map(
    DataNormalizer.normalize_address)

# Normaliza escolas
schools_df["escolas_postos"] = schools_df["escolas_postos"].map(
    lambda x: "".join([unidecode(word) for word in x]))

# Normaliza bairros
schools_df["bairro"] = schools_df["bairro"].map(
    lambda x: "".join([unidecode(word) for word in x]))

# Normaliza latitude e longitude
schools_df["lat"] = schools_df["lat"].apply(
    lambda x: float(x.replace(",", ".")).__round__(5)
)
schools_df["lon"] = schools_df["lon"].apply(
    lambda x: float(x.replace(",", ".")).__round__(5)
)

# Normaliza subprefeituras
subprefectures_df = subprefectures_df.map(
    DataNormalizer.normalize_subprefectures)

# Ligando tabelas e normalizando nome da tabela de subprefeitura
subprefectures_df.rename(columns={"nome": "bairro"}, inplace=True)

# Merge das tabelas
join_schools_courseware_df = pd.merge(
    schools_df, courseware_df, on="id", how="inner")

join_tables = pd.merge(join_schools_courseware_df, subprefectures_df,
                       on="bairro", how="inner")

# Renomeando colunas do dataframe
join_tables.rename(
    columns={"id": "id_escola", "escolas_postos": "nome_da_escola", "endereco": "logradouro_da_entrega", "lat": "latitude", "lon": "longitude", "quantidade": "quantidade_material"}, inplace=True)

# Normalizando escola
join_tables["tipo_da_escola"] = join_tables["nome_da_escola"].apply(
    DataNormalizer.normalize_schools)

# Exemplo de regex usando str replace
join_tables["numero"] = join_tables['logradouro_da_entrega'].str.extract(
    r'(\d+|(?<=\bS/NO\b)[^\d\s]+|(?<=\bS/NO\b)\s*\d+|\bS/NO\b)')


join_tables["numero"].fillna('S/NO', inplace=True)

# Exemplo de regex usando str replace
join_tables['logradouro_da_entrega'] = join_tables['logradouro_da_entrega'].str.replace(
    r'(\d+|(?<=\bS/NO\b)[^\d\s]+|(?<=\bS/NO\b)\s*\d+|\bS/NO\b|\bS/NDEG\b|\bS/N\b|\b,.*\b)', '', regex=True).str.rstrip(', ').str.strip()

join_tables = join_tables.reindex(
    columns=join_tables.columns[[0, 1, -2, 3, -1, 2, 7, 4, 5, 6]])

join_tables = join_tables.drop_duplicates(
    subset=["id_escola", "subprefeitura"])

# Agora, calcule a média agrupada por 'subprefeitura'
groupby_subprefecture_courseware = join_tables.groupby('subprefeitura')[
    'quantidade_material'].sum()

join_tables = join_tables[join_tables['quantidade_material'] > 0]

# Obtem a próxima latitude e longitude
join_tables['next_latitude'] = join_tables['latitude'].shift(-1)
join_tables['next_longitude'] = join_tables['longitude'].shift(-1)

# Calculo da distância entre a escola atual e a próxima
join_tables['distancia'] = join_tables.apply(lambda row: data_analyzer.haversine(
    row['latitude'], row['longitude'], row['next_latitude'], row['next_longitude']), axis=1)

# Plotando gráfico
pontos_entrega_df = join_tables[['latitude', 'longitude']]

best_route = data_analyzer.nearest_neighbor(pontos_entrega_df)
ordered_df = join_tables.iloc[best_route].reset_index(drop=True)

data_plot_manager.plot_route(ordered_df)

map_obj = data_plot_manager.plot_on_map(ordered_df)
map_obj.save('map.html')

# Exportando dados para csv
join_tables.to_csv('rotas_seguidas.csv', index=False)
groupby_subprefecture_courseware.to_csv('total_material.csv')
