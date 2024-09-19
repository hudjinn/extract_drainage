import geopandas as gpd


# Carregar o arquivo GPKG
input_path = './output/drenagem_ceara_utm.gpkg'  # Caminho do seu arquivo GPKG
layer_name = 'drenagem_ceara_utm_refactor'  # Substitua pelo nome da camada dentro do GPKG

# Carregar o GeoDataFrame
gdf = gpd.read_file(input_path, layer=layer_name, max_features=5000)
gdf['vertice_foz'] = gdf['geometry'].apply(lambda x: str(x.coords[-1]))
gdf['vertice_nascente'] = gdf['geometry'].apply(lambda x: str(x.coords[0]))

# Criar um DataFrame para identificar as correspondências montante-jusante
df_rel = gdf.merge(gdf, left_on="vertice_foz", right_on="vertice_nascente")
df_rel = df_rel.rename(columns={'id_segmento_x':'id_nascente', 
                                'id_segmento_y':'id_foz',
                                'comprimento_km_x': 'comprimento_km',
                                'ordem_strahler_x': 'ordem_strahler'})[['id_nascente', 'id_foz', 'comprimento_km', 'ordem_strahler']]


gdf_com_segmento_jusante = gdf.merge(df_rel, left_on='id_segmento', right_on='id_nascente')
gdf_com_segmento_jusante = gdf_com_segmento_jusante.rename(columns={'id_foz':'segmento_jusante',
                                                                    'comprimento_km_x': 'comprimento_km',
                                                                    'ordem_strahler_x': 'ordem_strahler'})
gdf_com_segmento_jusante = gdf_com_segmento_jusante[['id_segmento', 'segmento_jusante', 'comprimento_km', 'ordem_strahler']]
print(gdf_com_segmento_jusante)