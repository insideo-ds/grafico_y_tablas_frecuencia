
import pandas as pd
import numpy as np
from math import radians

from constants import DIR16_LABELS

def deg_to_dir16(deg_series: pd.Series) -> pd.Series:
    """
    Converts a pandas Series of degrees (0-360) into 16-point compass direction labels.
    Cerrado izquierda, abierto derecha [)
    """
    idx = (((deg_series + 11.25) % 360) // 22.5).astype("Int64")
    out = idx.map(lambda i: DIR16_LABELS[int(i)] if pd.notna(i) else pd.NA)
    return pd.Categorical(out, categories=DIR16_LABELS, ordered=True)

def transformar(df, tp_bins = [0, 10, 13, 16, 20], hs_bins = [0, 0.35, 0.4, 0.45, 0.6]):
    """
    Transforms the input DataFrame by renaming columns, filtering, and binning data.
    Parameters:
        df (pd.DataFrame): Input DataFrame containing wave data with specific columns.
        dir_bins (list or array-like): Bin edges for directional data (in degrees).
        tp_bins (list, optional): Bin edges for peak period (Tp) data. Default is [0, 10, 13, 16, 20].
        hs_bins (list, optional): Bin edges for significant wave height (Hm0) data. Default is [0, 0.35, 0.4, 0.45, 0.6].
    Returns:
        pd.DataFrame: Transformed DataFrame with renamed columns, filtered rows, and additional binned columns.
    Notes:
        - The function assumes the input DataFrame contains specific columns such as 'Month', 'Day', 'Year',
            'Significant height (Hm0)', 'Peak direction (DirTp)', 'Peak period (Tp)', and 'Error code'.
        - Rows with non-zero 'Error code' values are filtered out.
        - A new column 'date' is created by combining 'Year', 'Month', and 'Day'.
        - Directional data is converted to radians and stored in a new column 'dirtp_rad'.
        - Data is binned into categories for direction, peak period, and significant wave height.
    """

    df = df.copy()
    cols = {
        'Month': 'month',
        'Day': 'day',
        'Year': 'year',
        'Significant height (Hm0)': 'hs_m',
        'Peak direction (DirTp)': 'dirtp_dgs',
        'Peak period (Tp)': 'tp_s',
        'Error Code': 'error_code'
    }
    df.columns = df.columns.str.strip()
    df.rename(columns = cols, inplace = True)
    df = df[df["error_code"] == 0]
    if "Fecha y Hora" in df.columns:
        df["date"] = pd.to_datetime(df["Fecha y Hora"])
    else:
        df["date"] = pd.to_datetime(df[["year", "month", "day"]])
    df['dirtp_rad'] = np.radians(df["dirtp_dgs"]) # create radians column for direction

    df = df[["date", "dirtp_dgs", "dirtp_rad", "tp_s", "hs_m"]]
    df.dropna()

    df['dir_bins16'] = deg_to_dir16(df["dirtp_dgs"])
    df['tp_bins'] = pd.cut(df["tp_s"],bins=tp_bins,right=False) #left-inclusive and right-exclusive
    df['hs_bins'] = pd.cut(df["hs_m"],bins=hs_bins,right=False) #left-inclusive and right-exclusive

    return df

def get_bars(ax, tabla, eje_x, porcentaje=True, color='C0'):
    """
    Dibuja un gráfico de barras categórico basado en los totales de una sola columna.

    Parámetros
    ----------
    ax : matplotlib.axes.Axes
        Eje donde se dibuja el gráfico.
    tabla : pandas.DataFrame
        DataFrame con los datos originales.
    eje_x : str
        Nombre de la columna categórica para el eje X.
    porcentaje : bool, opcional
        Si es True, muestra porcentajes sobre el total.
    color : str, opcional
        Color de las barras.

    Retorna
    -------
    matplotlib.axes.Axes
        El eje modificado.
    """
    ax.clear()

    # Ocurrencias por categoría
    conteos = tabla[eje_x].value_counts(sort=False)

    # Normalización
    if porcentaje:
        total = conteos.sum()
        conteos = conteos / total * 100
        ax.set_ylim(0, 100)

    # Redondear
    conteos = conteos.round(2)

    # Gráfico
    etiquetas = conteos.index.tolist()
    valores = conteos.values
    posiciones = range(len(etiquetas))

    barras = ax.bar(posiciones, valores, color=color, edgecolor='black')

    # Etiquetas encima de cada barra
    for barra, valor in zip(barras, valores):
        texto = f"{valor:.2f}%" if porcentaje else f"{valor:.0f}"
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height(),
            texto,
            ha='center',
            va='bottom',
            fontsize=8
        )

    ax.set_xticks(posiciones)
    ax.set_xticklabels(etiquetas, rotation=45, ha='right')

    ax.set_xlabel(eje_x)
    ax.set_ylabel('Porcentaje (%)' if porcentaje else 'Frecuencia')
    sufijo = "(%)" if porcentaje else "(conteos)"
    ax.set_title(f'Totales por {eje_x} {sufijo}', pad=10)

    ax.grid(True, linestyle='--', alpha=0.4)
    return ax
