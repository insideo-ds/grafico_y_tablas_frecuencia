import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import radians
import os

def generar_rosa_vientos(archivo_excel, columna_direccion, columna_valor, rangos_valor, nombre_salida=None):

    df = pd.read_excel(archivo_excel)
    
    if columna_direccion not in df.columns:
        raise ValueError(f"Columna {columna_direccion} no encontrada")
    if columna_valor not in df.columns:
        raise ValueError(f"Columna {columna_valor} no encontrada")
    
    df_clean = df[[columna_direccion, columna_valor]].dropna()
    
    direcciones_rad = np.radians(df_clean[columna_direccion])
    
    sectores_direccion = 16
    
    cardinales = [
        'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
        'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'
    ]
    
    df_clean['sector_direccion'] = pd.cut(
        df_clean[columna_direccion] % 360,
        bins=np.linspace(0, 360, sectores_direccion + 1),
        labels=cardinales,
        right=False
    )
    
    df_clean['rango_valor'] = pd.cut(
        df_clean[columna_valor],
        bins=rangos_valor,
        right=False
    )
    
    tabla_frecuencias = pd.crosstab(
        df_clean['sector_direccion'],
        df_clean['rango_valor'],
        normalize=True
    ) * 100
    
    fig, (ax_rosa, ax_tabla) = plt.subplots(1, 2, figsize=(16, 8))

    crear_rosa_vientos(ax_rosa, df_clean, direcciones_rad, columna_valor, rangos_valor, cardinales)
    
    crear_tabla_frecuencias(ax_tabla, tabla_frecuencias)
    
    plt.tight_layout()
    
    if nombre_salida is None:
        nombre_salida = 'rosa_vientos'
    
    plt.savefig(f'{nombre_salida}.png', dpi=300, bbox_inches='tight')
    tabla_frecuencias.to_excel(f'{nombre_salida}_tabla_frecuencias.xlsx')
    
    plt.show()
    
    return tabla_frecuencias

def crear_rosa_vientos(ax, df, direcciones_rad, columna_valor, rangos_valor, cardinales):
    """Crea la rosa de vientos en el eje polar (centros alineados con los cardinales)."""

    sectores = 16
    ax = plt.subplot(1, 2, 1, projection='polar')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    valores = df[columna_valor]
    bins_valor = len(rangos_valor) - 1

    width = 2 * np.pi / sectores

    theta_edges = np.linspace(-width/2, 2*np.pi - width/2, sectores + 1)

    direcciones_mod = np.mod(direcciones_rad, 2*np.pi)
    hist, theta_bins, value_bins = np.histogram2d(
        direcciones_mod,
        valores,
        bins=[theta_edges, rangos_valor]
    )

    theta_centers = (theta_edges[:-1] + theta_edges[1:]) / 2

    colores = plt.cm.viridis(np.linspace(0, 1, bins_valor))

    bottom = np.zeros(sectores)
    for i in range(bins_valor):
        ax.bar(
            theta_centers,
            hist[:, i],
            width=width,
            bottom=bottom,
            color=colores[i],
            edgecolor='white',
            linewidth=0.5,
            label=f'{rangos_valor[i]}-{rangos_valor[i+1]}'
        )
        bottom += hist[:, i]

    ax.set_xticks(theta_centers)
    ax.set_xticklabels(cardinales)
    ax.set_title('Rosa de Vientos', pad=20)
    ax.legend(bbox_to_anchor=(1.1, 1.0), title='Rangos de Valor')

def crear_tabla_frecuencias(ax, tabla):
    """Crea la tabla de frecuencias en el eje especificado"""
    ax.axis('off')
    tabla_plot = ax.table(
        cellText=np.round(tabla.values, 2),
        rowLabels=tabla.index,
        colLabels=tabla.columns,
        cellLoc='center',
        loc='center'
    )
    tabla_plot.auto_set_font_size(False)
    tabla_plot.set_fontsize(10)
    tabla_plot.scale(1, 1.5)
    ax.set_title('Tabla de Frecuencias (%)', pad=20)

# EJEMPLO DE USO
if __name__ == "__main__":
    # Configuración personalizable
    config = {
        'archivo_excel': 'ADCP2-Olas verano - 2023.xlsx',
        'columna_direccion': 'Peak direction (DirTp)',
        'columna_valor': 'Peak period (Tp)',
        'rangos_valor': [0, 10, 13, 16, 20],
        'nombre_salida': 'Olas_DirTp_Tp'
    }
    
    # Generar rosa de vientos
    tabla = generar_rosa_vientos(**config)

    print("Rosa de vientos generada exitosamente!")
    print("\nTabla de frecuencias:")
    print(tabla)

    config = {
        'archivo_excel': 'ADCP2_corrientes Verano 2023.xlsx',
        'columna_direccion': 'Dir#1(1.4m)',
        'columna_valor': 'Speed#1(1.4m)',
        'rangos_valor': [0, 5, 10, 15, 20, 25],
        'nombre_salida': 'Corrientes_1.4m'
    }

        # Generar rosa de vientos
    tabla = generar_rosa_vientos(**config)

    print("Rosa de vientos generada exitosamente!")
    print("\nTabla de frecuencias:")
    print(tabla)
    
