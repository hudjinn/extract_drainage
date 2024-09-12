import geopandas as gpd
import pandas as pd
from tqdm import tqdm

# Carregar o arquivo GPKG
input_path = './output/drenagem.gpkg'  # Caminho do seu arquivo GPKG
layer_name = 'drenagem'  # Substitua pelo nome da camada dentro do GPKG

class FDP:
    def __init__(self):
        self.df_export = pd.DataFrame()

    def flatten(self, lst):
        flat_list = []
        for item in lst:
            if isinstance(item, list):
                flat_list.extend(self.flatten(item))  # Chamada recursiva se o item for uma lista
            else:
                flat_list.append(item)
        return flat_list

    # Função para obter os segmentos a jusante
    def get_downstream_features(self, id_segmento):
        df_downstream = df_rel[df_rel['id_nascente'] == id_segmento['id_foz']]
        if len(df_downstream) == 0:
            return [id_segmento]
        return list(df_downstream['id_foz']) + [self.get_downstream_features(df_downstream.iloc[0])]

    # Função para obter os segmentos a montante
    def get_upstream_features(self, id_segmento):
        segmentos_upstream = df_rel[df_rel['id_foz'] == id_segmento]['id_nascente']          
        if len(segmentos_upstream) == 0:
            return []
        lista_segmentos = [[segmento, self.get_upstream_features(segmento)] for segmento in segmentos_upstream]
        lista_flat = self.flatten(lista_segmentos)
        df_temp = pd.DataFrame({'id_foz': id_segmento, 'id_nascente': lista_flat})
        if self.df_export.empty:
            self.df_export = df_temp
        else:
            self.df_export = pd.concat([self.df_export, df_temp])
        return lista_flat
        
if __name__ == '__main__':
    fdp = FDP()
    # Carregar o GeoDataFrame
    gdf = gpd.read_file(input_path, layer=layer_name)
    gdf['vertice_foz'] = gdf['geometry'].apply(lambda x: str(x.coords[-1]))
    gdf['vertice_nascente'] = gdf['geometry'].apply(lambda x: str(x.coords[0]))

    # Verificar a estrutura do GeoDataFrame
    print("GeoDataFrame carregado:")

    # Criar um DataFrame vazio para armazenar as correspondências montante-jusante
    df_rel = gdf.merge(gdf, left_on="vertice_foz", right_on="vertice_nascente")
    df_rel = df_rel.rename(columns={'id_segmento_x':'id_nascente', 'id_segmento_y':'id_foz'})[['id_nascente', 'id_foz']]

    # Obter IDs dos segmentos que não têm um segmento a jusante (últimos segmentos)
    last_segments = df_rel[~df_rel['id_foz'].isin(df_rel['id_nascente'])]['id_foz'].dropna().unique()

    # Exibir os segmentos que são os últimos (sem id_foz)
    print("IDs dos últimos segmentos:")
    # print(last_segments)
    for id_segmento in tqdm(last_segments):
        fdp.get_upstream_features(id_segmento=id_segmento)
    fdp.df_export.sort_values(by='id_foz').reset_index(drop=True).to_csv('output/lista_segmentos_jusante_montante.csv')