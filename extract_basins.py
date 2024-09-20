import os
import geopandas as gpd
from extract import run_saga
from clip_raster import clip_nodata

# Caminho dos arquivos
exutorios_dir = os.path.abspath('output/basins/exutorios_ceara.gpkg')
layer_name = 'exutorios_ceara'

# Diretório Leitura dos DEM NoSink
input_dir = os.path.abspath('output/basins/processed')
dem_list = [file for file in os.listdir(input_dir) if file.endswith('.sdat')]

# Carregar o shapefile de exutórios
exutorios = gpd.read_file(exutorios_dir, layer=layer_name)

files_dict = {
            'Coreaú': '0',
            'Jaguaribe': '1',
            'Acaraú': '2',
            'Litoral': '3',
            'Curu': '4',
            'Metropolitana': '5',
            'Serra da Ibiapaba': '6',
            'Sertões de Crateús': '7'
            }

# Iterar sobre cada exutório
for index, row in exutorios.iterrows():
    id_segmento = row.id_segmento  # ID único para salvar cada bacia separadamente
    geom = row.geometry  # Geometria do exutório
    x = geom.x  # Coordenada X
    y = geom.y  # Coordenada Y
    bacia = files_dict.get(row.Bacia)

    # Definir caminho de saída para cada bacia
    output = os.path.abspath('output/basins/processed')
    output_path = os.path.join(output, f'dem_{bacia}')
    output_file = os.path.join(output_path, f'{str(id_segmento)}.sdat')
    dem_path = os.path.join(input_dir, f'nosink_dem_{bacia}.tif.sdat')
    
    # Testar se arquivo do exutório já existe em tif
    if os.path.exists(os.path.join(output_path, f'{id_segmento}.tif')):
        print(f'Arquivo {id_segmento}.tif encontrado. Pulando iteração...')
        continue
    
    # Imprimir coordenadas e parâmetros para verificação    
    print(f'Processando exutório {id_segmento} nas coordenadas ({x}, {y})')
    print(f'Arquivo de saída: {output_file}')

    # Executar o comando SAGA para delimitar a bacia para o exutório atual
    run_saga(lib='ta_hydrology', tool='4',
             TARGET_PT_X=x,
             TARGET_PT_Y=y,
             ELEVATION=dem_path,
             AREA=output_file,
             METHOD='2')

    # Alterar valor NoData no arquivo de saída
    if os.path.exists(output_file):
        clip_nodata(id_segmento, bacia, raster_path_to_clip=output_file)
    else:
        print(f'Erro ao criar o arquivo de saída: {output_file}')

print("Delimitação das bacias concluída.")
