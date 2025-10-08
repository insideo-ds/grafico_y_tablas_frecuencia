import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes

from constants import DIR16_LABELS

def get_polar_rose_plot(ax, df, r, theta, intervals, cardinales=DIR16_LABELS):
    """Dibuja una rosa de vientos (barras polares apiladas) en el eje proporcionado.

    Comportamiento clave
    - Usa el `ax` que se le pasa; no crea un nuevo subplot internamente. Si el
      `ax` no es polar, intenta reemplazarlo por un eje polar en la misma
      ubicación del layout.
    - `r` y `theta` pueden ser nombres de columnas (str) presentes en `df` o
      arrays/Series del mismo largo que `df`.

    Parámetros
    ----------
    ax : matplotlib.axes.Axes
        Eje donde se dibujará la rosa. Debe pertenecer a la figura creada por
        `plt.subplots` (por ejemplo `fig, (ax_rosa, ax_tabla) = plt.subplots(1,2)`).
    df : pandas.DataFrame
        DataFrame con los datos. Si `r` o `theta` son nombres de columnas, se
        leerán de aquí.
    r : str o array-like
        Columna de `df` con los valores a agrupar (por ejemplo, velocidad)
        o directamente un array/Series con esos valores.
    theta : str o array-like
        Direcciones en radianes: nombre de columna en `df` (p. ej. 'dir_rad')
        o un array/Series de radianes.
    intervals : sequence
        Bordes de los intervalos para agrupar `r` (ej. [0,5,10,15]).
    cardinales : sequence, opcional
        Etiquetas para los sectores angulares. Por defecto usa `CARDINALES`.

    Devuelve
    -------
    matplotlib.axes.Axes
        El eje `ax` (polar) donde se dibujó la rosa. Esto permite encadenar
        llamadas o guardar/ajustar el `fig` que creó el llamador.

    Ejemplo de uso
    --------------
    # En main.py:
    fig, (ax_rosa, ax_tabla) = plt.subplots(1, 2, figsize=(16, 8))
    get_bar_polar(ax_rosa, df, r=columna_valor, theta='dir_rad', intervals=rangos_valor)

    """
    SECTORES = len(cardinales)
    # Asegurarse de que ax sea polar; si no lo es, intentar reemplazarlo
    if getattr(ax, 'name', '') != 'polar':
        fig = ax.figure
        try:
            polar_ax = fig.add_subplot(ax.get_subplotspec(), projection='polar')
            fig.delaxes(ax)
            ax = polar_ax
        except Exception:
            # Fallback: crear un nuevo polar axes (puede alterar layout)
            ax = plt.subplot(1, 2, 1, projection='polar')

    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    # Obtener arrays de valores
    if isinstance(r, str):
        if r not in df.columns:
            raise KeyError(f"Columna '{r}' no encontrada en el DataFrame")
        radio = df[r].values
    else:
        radio = np.asarray(r)

    if isinstance(theta, str):
        if theta not in df.columns:
            raise KeyError(f"Columna '{theta}' no encontrada en el DataFrame")
        theta_vals = df[theta].values
    else:
        theta_vals = np.asarray(theta)

    bins_valor = len(intervals) - 1

    width = 2 * np.pi / SECTORES

    theta_edges = np.linspace(-width / 2, 2 * np.pi - width / 2, SECTORES + 1)

    direcciones_mod = np.mod(theta_vals, 2 * np.pi)
    hist, theta_bins, value_bins = np.histogram2d(
        direcciones_mod,
        radio,
        bins=[theta_edges, intervals]
    )

    theta_centers = (theta_edges[:-1] + theta_edges[1:]) / 2

    colores = plt.cm.viridis(np.linspace(0, 1, bins_valor))

    bottom = np.zeros(SECTORES)
    for i in range(bins_valor):
        ax.bar(
            theta_centers,
            hist[:, i],
            width=width,
            bottom=bottom,
            color=colores[i],
            edgecolor='white',
            linewidth=0.5,
            label=f'{intervals[i]}-{intervals[i+1]}'
        )
        bottom += hist[:, i]

    ax.set_xticks(theta_centers)
    ax.set_xticklabels(cardinales)
    ax.set_title('Rosa', pad=20)
    ax.legend(bbox_to_anchor=(1.1, 1.0), title=f'Rangos de {r}')

    return ax

def get_table_frequency(ax, tabla):

    tabla = pd.crosstab(
        tabla['sector_direccion'],
        tabla['rango_valor'],
        normalize=True
    ) * 100

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


def get_histogram(ax, data, bins=10, xlabel=None, ylabel='Frequency', title=None, color='C0'):
    """Dibuja un histograma simple sobre el eje proporcionado.

    Parámetros
    ----------
    ax : matplotlib.axes.Axes
        Eje donde dibujar el histograma.
    data : array-like or pandas.Series
        Valores numéricos a graficar.
    bins : int o sequence, opcional
        Número de bins o secuencia de bordes (por defecto 10).
    xlabel : str, opcional
        Etiqueta para el eje x.
    ylabel : str, opcional
        Etiqueta para el eje y (por defecto 'Frequency').
    title : str, opcional
        Título del gráfico.
    color : str, opcional
        Color de las barras.

    Returns
    -------
    matplotlib.axes.Axes
        El eje donde se dibujó el histograma (útil para encadenar llamadas).

    Ejemplo
    -------
    fig, ax = plt.subplots()
    show_histogram(ax, df['velocidad'], bins=[0,5,10,15], xlabel='Velocidad (m/s)')
    plt.show()
    """

    ax.cla()
    ax.hist(data, bins=bins, color=color, edgecolor='black') #Este método bin la data en x y cuenta el número de ocurrencias en y.
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.grid(True, linestyle='--', alpha=0.4)
    return ax