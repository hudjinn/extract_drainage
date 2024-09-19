"""

"""

import os
from extract import run_saga

# Diretórios com caminho absoluto
output = os.path.abspath('./output/basins/processed/')

input_dir = os.path.abspath('output/basins')

dem_list = [file for file in os.listdir(input_dir) if file.endswith('.tif')]

def sink_removal(filename, dem, output):
    
    nosink_dem = os.path.join(output, f'nosink_{filename}.sdat')
    run_saga(lib='ta_preprocessor', tool='2', 
             DEM=dem,
             DEM_PREPROC=nosink_dem)
    return nosink_dem

def channel_drainage_basins(dem, output):
    run_saga(lib='ta_channels', tool='5',
             DEM=dem,
             DIRECTION=os.path.join(output, 'flow_dir.sdat'),
             ORDER=os.path.join(output, 'strahler.sdat'),
             BASIN=os.path.join(output, 'basin.sdat'),
             SEGMENTS=os.path.join(output, 'drainage.shp'),
             BASINS=os.path.join(output, 'basins.shp'),
             NODES=os.path.join(output, 'nodes.shp'),
             THRESHOLD=3)
    

if __name__ == '__main__':
    for dem in dem_list:

        dem_path = os.path.join(input_dir, dem)
        output_iter = os.path.join(output, dem[:5])
        if not os.path.exists(output_iter):
            os.makedirs(output_iter)
        print('Salvando em: ', output_iter)
        
        nosink_dem = sink_removal(filename=dem, dem=dem_path, output=output)
        channel_drainage_basins(dem=nosink_dem, output=output_iter)
