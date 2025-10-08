import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
from io import BytesIO
from PIL import Image

import numpy as np
from math import radians


from extract import extract
from scripts.report import report_olas
from transform import transformar
from visualizations import get_polar_rose_plot, get_table_frequency
from constants import CARDINALES, CONFIG, SECTORES

if __name__ == "__main__":
    # Configuración personalizable
    for con in CONFIG:
        df = extract(con['path'])

        dir_grados = con['direccion_grados']
        radio = con['columna_valor']
        intervalos = con['rangos_valor']
        nombre_salida = con.get('nombre_salida', 'rosa')

        # Limpiar y transformar datos
        df, tabla_frecuencias = transformar(df, dir_grados, radio, intervalos)

        # Define la figura y los ejes del reporte
        fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(16, 8)) # Define ubicación y tamaño de los subplots
        fig, axes = plt.subplots(2, 3, figsize=(10, 6))
        axes = axes.flatten()

        report_olas()
        # Generar rosa de vientos
        get_polar_rose_plot(ax_left,
                            df,
                            r = radio,
                            theta = "dir_rad",
                            intervals = intervalos)


        # Create the polar bar chart using Plotly
        px_fig = px.bar_polar(
            df,
            r=radio,
            theta="sector_direccion",
            color="rango_valor",
            template="plotly_dark",
            color_discrete_sequence=px.colors.sequential.Plasma_r,
        )

        # Render Plotly figure to PNG bytes and show in the matplotlib axis
        img_bytes = pio.to_image(px_fig, format="png", width=600, height=600, scale=2)
        img = Image.open(BytesIO(img_bytes))
        ax_right.clear()
        ax_right.imshow(img)
        ax_right.axis('off')

        # Crear tabla de frecuencias
        get_table_frequency(ax_right, tabla_frecuencias)

        plt.show()

        # Guardar resultados
        plt.savefig(f'{nombre_salida}_rosa.png', dpi=300, bbox_inches='tight')
        tabla_frecuencias.to_excel(f'{nombre_salida}_tabla_frecuencias.xlsx')






