import geopandas as gpd
import pandas as pd
from tqdm import tqdm
import sys
import multiprocessing

# Carregar o arquivo GPKG
input_path = './output/drenagem_ceara_utm.gpkg'  # Caminho do seu arquivo GPKG
layer_name = 'drenagem_ceara_utm_refactor'  # Substitua pelo nome da camada dentro do GPKG
sys.setrecursionlimit(2000000)

class FDP:
    def __init__(self):
        pass

    def flatten(self, lst):
        flat_list = []
        for item in lst:
            if isinstance(item, list):
                flat_list.extend(self.flatten(item))  # Chamada recursiva se o item for uma lista
            else:
                flat_list.append(item)
        return flat_list

    # Função para obter os segmentos a montante
    def get_upstream_features(self, id_segmento):
        segmentos_upstream = df_rel[df_rel['id_foz'] == id_segmento]['id_nascente']
        if len(segmentos_upstream) == 0:
            return []
        lista_segmentos = [[segmento, self.get_upstream_features(segmento)] for segmento in segmentos_upstream]
        lista_flat = self.flatten(lista_segmentos)
        df_temp = pd.DataFrame({'id_foz': id_segmento, 'id_nascente': [lista_flat]})
        
        # Gravar diretamente no arquivo CSV (append)
        with open('output/lista_segmentos_jusante_montante_lista.csv', 'a') as f:
            df_temp.to_csv(f, header=False, index=False)
        
        return lista_flat

# Função worker para o multiprocessing
def process_segment(segmento):
    fdp = FDP()
    fdp.get_upstream_features(id_segmento=segmento)

if __name__ == '__main__':
    fdp = FDP()

    # Carregar o GeoDataFrame
    gdf = gpd.read_file(input_path, layer=layer_name)
    gdf['vertice_foz'] = gdf['geometry'].apply(lambda x: str(x.coords[-1]))
    gdf['vertice_nascente'] = gdf['geometry'].apply(lambda x: str(x.coords[0]))

    # Criar um DataFrame para identificar as correspondências montante-jusante
    df_rel = gdf.merge(gdf, left_on="vertice_foz", right_on="vertice_nascente")
    df_rel = df_rel.rename(columns={'id_segmento_x':'id_nascente', 'id_segmento_y':'id_foz'})[['id_nascente', 'id_foz']]

    # Obter IDs dos segmentos que não têm um segmento a jusante (últimos segmentos)
    last_segments = df_rel[~df_rel['id_foz'].isin(df_rel['id_nascente'])]['id_foz'].dropna().unique()
    print(last_segments)
    # Criar o arquivo CSV e escrever o cabeçalho
    with open('output/lista_segmentos_jusante_montante.csv', 'w') as f:
        f.write('id_foz,id_nascente\n')

    # Multiprocessing para processar em paralelo
    num_cores = multiprocessing.cpu_count()  # Número de núcleos disponíveis
    pool = multiprocessing.Pool(num_cores)

    # Usar tqdm para barra de progresso com multiprocessing
    for _ in tqdm(pool.imap_unordered(process_segment, last_segments), total=len(last_segments)):
        pass

    pool.close()
    pool.join()

    print("Processamento completo.")
