import rioxarray as rxr
import xarray as xr
import matplotlib.pyplot as plt
import os
          
def clip_nodata(id_segmento, raster_path_to_clip):

    if os.path.exists(raster_path_to_clip):
        input = rxr.open_rasterio(raster_path_to_clip)
        print(raster_path_to_clip)
        os.remove(f'output/basins/processed/{id_segmento}.*')
        print(f'Arquivo original deletado: {raster_path_to_clip}')
        
        input = input.where(input > 0)
        input = input.dropna(dim='x',how='all')
        input = input.dropna(dim='y',how='all')

        input.rio.to_raster(f'output/basins/processed/{id_segmento}.tif')
        print(f'Arquivo TIFF criado: {id_segmento}.tif')
    else:
        print(f'Arquivo não encontrado: {raster_path_to_clip}')
