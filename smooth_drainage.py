import os
import subprocess
from extract import run_saga

# Diretórios com caminho absoluto
drainage = os.path.abspath('./output/drainage.shp')
output = os.path.abspath('./output')

def smooth_drainage(drainage, output_path):
    run_saga(lib='shapes_lines', tool='7',
             LINES_IN=drainage,
             LINES_OUT=os.path.join(output,'smooth_drainage.shp'),
             METHOD=0,
             SENSITIVITY=1,
             ITERATIONS=1,
             PRESERVATION=3.0,
             SIGMA=1.5)
    
if __name__ == '__main__':
    smooth_drainage(drainage=drainage, output_path=output)

