import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
from io import BytesIO
from PIL import Image

import numpy as np
from math import radians


from extract import extract
from transform import transformar
from visualizations import get_polar_rose_plot, get_table_frequency, get_histogram
from constants import CARDINALES, CONFIG, SECTORES

if __name__ == "__main__":
    # Configuración personalizable
    for con in CONFIG:
        #1. Extraer la data
        df = extract(con['path'])
        dir_grados = con['direccion_grados']

        periodo_pico = "Peak period (Tp)"
        intervalos = con['rangos_valor']
        nombre_salida = con.get('nombre_salida', 'rosa')

        #2. Limpiar y transformar datos
        df = transformar(df, dir_grados, periodo_pico, intervalos)
        print(df.columns)

        #3. Plotear
        fig, axes = plt.subplots(2, 2, figsize=(10, 6))
        axes = axes.flatten()

        ## Altura significativa
        get_table_frequency(axes[2], df)

        ## Periodo pico
        get_polar_rose_plot(axes[0], df, r = periodo_pico, theta = "dir_rad", intervals = intervalos)
        get_histogram(axes[3], df[periodo_pico], bins=intervalos, xlabel=periodo_pico, title='Histograma de '+periodo_pico)
        get_polar_rose_plot(axes[1], df, r = 'Significant height (Hm0)', theta = "dir_rad", intervals = intervalos)

        plt.tight_layout()
        plt.show()

        # Guardar resultados
        #plt.savefig(f'{nombre_salida}_rosa.png', dpi=300, bbox_inches='tight')
        #tabla_frecuencias.to_excel(f'{nombre_salida}_tabla_frecuencias.xlsx')






