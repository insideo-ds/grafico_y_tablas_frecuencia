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
from visualizations import get_polar_rose_plot, get_table_frequency
from constants import CARDINALES, CONFIG, SECTORES

if __name__ == "__main__":
    # Configuración personalizable
    for con in CONFIG:
        #1. Extraer la data
        df = extract(con['path'])
        print(df.head)

        dir_grados = con['direccion_grados']
        radio = con['columna_valor']
        intervalos = con['rangos_valor']
        nombre_salida = con.get('nombre_salida', 'rosa')

        #2. Limpiar y transformar datos
        df, tabla_frecuencias = transformar(df, dir_grados, radio, intervalos)
        print(df.head)

        #3. Plotear
        fig, axes = plt.subplots(2, 2, figsize=(10, 6))
        axes = axes.flatten()

        get_polar_rose_plot(axes[0], df, r = radio, theta = "dir_rad", intervals = intervalos)
        get_table_frequency(axes[3], tabla_frecuencias)

        plt.tight_layout()
        plt.show()

        # Guardar resultados
        #plt.savefig(f'{nombre_salida}_rosa.png', dpi=300, bbox_inches='tight')
        #tabla_frecuencias.to_excel(f'{nombre_salida}_tabla_frecuencias.xlsx')






