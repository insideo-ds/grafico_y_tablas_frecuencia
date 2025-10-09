import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
from io import BytesIO
from PIL import Image

import numpy as np
from math import radians
from windrose import WindroseAxes


from extract import extract
from transform import get_bars, transformar
from visualizations import get_polar_rose_plot, get_table_frequency, get_histogram, get_time_series, get_polar_from_windrose
from constants import CONFIG

if __name__ == "__main__":
    # Configuración personalizable
    for con in CONFIG:

        hs_bins = con.get('hs_bins', [0, 0.35, 0.4, 0.45, 0.6])
        tp_bins = con.get('tp_bins', [0, 10, 13, 16, 20])

        #1. Extraer la data
        df = extract(con['path'])

        #2. Limpiar y transformar datos
        df = transformar(df)
        df.to_excel(f'out/data_limpia.xlsx')

        #3. Plotear
        fig, axes = plt.subplots(4, 1, figsize=(12, 36))
        axes = axes.flatten()

        ## Altura significativa
        #get_table_frequency(axes[2], df, par1="dir_rad", par2="hs")
        get_polar_rose_plot(axes[0], df, r = 'hs_m', theta = "dirtp_rad", intervals = hs_bins)
        #get_histogram(axes[1], df['hs_m'], bins=hs_bins, xlabel='hs_m', title='Histograma de '+'hs_m', porcentaje=True, annotate=True)
        get_bars(axes[1], df, eje_x="hs_bins")
        get_table_frequency(axes[2], df, eje_y="dir_bins16", eje_x="hs_bins")
        get_time_series(axes[3], df, 'date','hs_m', title='Serie temporal de '+'hs_m', xlabel='Fecha', ylabel='hs_m')
        get_polar_from_windrose(df, tp_bins)


        ## Periodo pico
        #get_polar_rose_plot(axes[2], df, r = 'tp_s', theta = "dirtp_rad", intervals = tp_bins)
        #get_histogram(axes[3], df['tp_s'], bins=tp_bins, xlabel='tp_s', title='Histograma de '+'tp_s')
        #Windrose con windrose


        plt.tight_layout()
        plt.show()

        # Guardar resultados
        #plt.savefig(f'{nombre_salida}_rosa.png', dpi=300, bbox_inches='tight')
        #tabla_frecuencias.to_excel(f'{nombre_salida}_tabla_frecuencias.xlsx')






