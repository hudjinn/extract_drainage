import rioxarray as rxr
import os
          
def clip_nodata(id_segmento, bacia, raster_path_to_clip):

    if os.path.exists(raster_path_to_clip):
        input = rxr.open_rasterio(raster_path_to_clip)
        folder = f'output/basins/processed/dem_{bacia}'
        for file in os.listdir(folder):
            if file.startswith(str(id_segmento)):
                os.remove(os.path.join(folder, file))
        print(f'Arquivo original deletado: {raster_path_to_clip}')
        
        input = input.where(input > 0)
        input = input.dropna(dim='x',how='all')
        input = input.dropna(dim='y',how='all')

        input.rio.to_raster(f'output/basins/processed/dem_{bacia}/{id_segmento}.tif')
        print(f'Arquivo TIFF criado: {id_segmento}.tif')
    else:
        print(f'Arquivo não encontrado: {raster_path_to_clip}')
