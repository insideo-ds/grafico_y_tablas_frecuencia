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
from visualizations import get_polar_rose_plot, get_table_frequency, get_histogram, get_time_series
from constants import CONFIG

if __name__ == "__main__":
    # Configuración personalizable
    for con in CONFIG:
        periodo_pico = "tp_s"
        hs_bins = [0.35, 0.4, 0.45, 0.6]
        tp_bins = [0, 10, 13, 16, 20]

        #1. Extraer la data
        df = extract(con['path'])

        #2. Limpiar y transformar datos
        df = transformar(df)
        df.to_excel(f'out/data_limpia.xlsx')

        #3. Plotear
        fig, axes = plt.subplots(2, 2, figsize=(10, 6))
        axes = axes.flatten()

        ## Altura significativa
        #get_table_frequency(axes[2], df, par1="dir_rad", par2="hs")
        get_polar_rose_plot(axes[0], df, r = 'hs_m', theta = "dirtp_rad", intervals = hs_bins)
        get_histogram(axes[1], df['hs_m'], bins=hs_bins, xlabel='hs_m', title='Histograma de '+'hs_m', porcentaje=True, annotate=True)
        get_table_frequency(axes[2], df, eje_y="dir_bins16", eje_x="hs_bins")
        #get_time_series(axes[3], df, 'date','hs_m', title='Serie temporal de '+'hs_m', xlabel='Fecha', ylabel='hs_m')
        get_bars(axes[3], df, eje_x="hs_bins")

        ## Periodo pico
        #get_polar_rose_plot(axes[2], df, r = 'tp_s', theta = "dirtp_rad", intervals = tp_bins)
        #get_histogram(axes[3], df['tp_s'], bins=tp_bins, xlabel='tp_s', title='Histograma de '+'tp_s')

        """
        Windrose con windrose
                ax = WindroseAxes.from_ax()
                ax.set_xticklabels(('E','NE','N','NW','W','SW','S','SE'))
                #ax.set_xticklabels(DIR16_LABELS)
                ax.bar(df["dirtp_dgs"], df["tp_s"], normed=True, bins = tp_bins, opening=0.8, nsector=16, edgecolor='white') #By default, the offset is zero, and the first sector is [-360/nsector/2, 360/nsector/2] or [-11.25, 11.25] for nsector=16.
                ax.set_title("tp_s", fontsize=12, weight='bold')
                ax.set_legend()
        """
        plt.tight_layout()
        plt.show()

        # Guardar resultados
        #plt.savefig(f'{nombre_salida}_rosa.png', dpi=300, bbox_inches='tight')
        #tabla_frecuencias.to_excel(f'{nombre_salida}_tabla_frecuencias.xlsx')






