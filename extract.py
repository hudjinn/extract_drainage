"""
ETAPAS

Tratar DEM (fill sinks, fill depressions etc)
Extrair Bacias, sub-bacias
Extrair drenagem com coordenada Z e Classificação Strahler
Criar codificacao levando em consideração a bacia, a ordem de strahler e fluxo de acumulação
Alinhar drenagens de acordo com barragens (snap)
Detectar angulos de 90º e suavizar
Exportar como vetor
"""

import os
import subprocess

# Diretórios com caminho absoluto
dem = os.path.abspath('./input/dem.tif')
output = os.path.abspath('./output')

def run_saga(lib, tool, **kwargs):
    # Cria a lista de argumentos a partir dos parâmetros
    args = ['saga_cmd', lib, tool] + [f'-{k}={v}' for k, v in kwargs.items()]
    
    # Imprime o comando
    print("Comando executado:", '\033[31m '.join(args), '\033[0m')
    subprocess.run(args)
    
def sink_removal(dem, output):
    nosink_dem = os.path.join(output, 'nosink_dem.sdat')
    run_saga(lib='ta_preprocessor', tool='2', 
             DEM=dem,
             DEM_PREPROC=nosink_dem)
    return nosink_dem

def flat_detection(dem, output):
    noflat_dem = os.path.join(output, 'noflat_dem.sdat')
    run_saga(lib='ta_preprocessor', tool='0',
             DEM=dem,
             NOFLATS=noflat_dem)
    return noflat_dem

def strahler_order(dem, output):
    run_saga(lib='ta_channels', tool='6',
             DEM=dem,
             STRAHLER=os.path.join(output, 'strahler.sdat'))

def channel_drainage_basins(dem, output):
    run_saga(lib='ta_channels', tool='5',
             DEM=dem,
             BASIN=os.path.join(output, 'basins.shp'),
             SEGMENTS=os.path.join(output, 'drainage.shp'),
             ORDER=os.path.join(output, 'strahler.sdat'),
             NODES=os.path.join(output, 'nodes.sdat'),
             THRESHOLD=3)

def flow_accumulation(dem, output):
    flow_accum = os.path.join(output, 'flow_accum.sdat')
    
    # Executa a ferramenta saga_cmd ta_hydrology 0 com os parâmetros necessários
    run_saga(lib='ta_hydrology', tool='0',
             ELEVATION=dem,  # DEM de entrada
             FLOW=flow_accum,  # Arquivo de saída da acumulação de fluxo
             METHOD=4,  # Usar Multiple Flow Direction (padrão)
             FLOW_UNIT=1,  # Unidade: área da célula
             NO_NEGATIVES=1,  # Impedir acumulação negativa
             CONVERGENCE=1.1)  # Convergência padrão

    return flow_accum

if __name__ == '__main__':
    nosink_dem = sink_removal(dem, output)
    noflat_dem = flat_detection(nosink_dem, output)
    
    flow_accum = flow_accumulation(noflat_dem, output)
    strahler_output = strahler_order(noflat_dem, output)
    channel_drainage_basins(noflat_dem, output)
    
    drainage = os.path.join(output, 'drainage.shp')