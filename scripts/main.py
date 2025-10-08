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
from constants import CONFIG

if __name__ == "__main__":
    # Configuración personalizable
    for con in CONFIG:
        periodo_pico = "tp_s"
        intervalos = con['rangos_valor']

        #1. Extraer la data
        df = extract(con['path'])

        #2. Limpiar y transformar datos
        df = transformar(df)
        df.to_excel(f'data_limpia.xlsx')

        #3. Plotear
        fig, axes = plt.subplots(2, 2, figsize=(10, 6))
        axes = axes.flatten()

        ## Altura significativa
        #get_table_frequency(axes[2], df, par1="dir_rad", par2="hs")

        ## Periodo pico
        get_polar_rose_plot(axes[0], df, r = periodo_pico, theta = "dirtp_rad", intervals = intervalos)
        get_histogram(axes[3], df[periodo_pico], bins=intervalos, xlabel=periodo_pico, title='Histograma de '+periodo_pico)
        get_polar_rose_plot(axes[1], df, r = 'hs_m', theta = "dirtp_rad", intervals = intervalos)
        get_table_frequency(axes[2], df, eje_y="dir_bins16", eje_x="hs_bins")

        plt.tight_layout()
        plt.show()

        # Guardar resultados
        #plt.savefig(f'{nombre_salida}_rosa.png', dpi=300, bbox_inches='tight')
        #tabla_frecuencias.to_excel(f'{nombre_salida}_tabla_frecuencias.xlsx')






