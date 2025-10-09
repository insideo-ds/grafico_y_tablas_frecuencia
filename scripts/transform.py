
import pandas as pd
import numpy as np
from math import radians

from config import DIR16_LABELS

def deg_to_dir16(deg_series: pd.Series) -> pd.Series:
    """
    Converts a pandas Series of degrees (0-360) into 16-point compass direction labels.
    Cerrado izquierda, abierto derecha [)
    """
    idx = (((deg_series + 11.25) % 360) // 22.5).astype("Int64")
    out = idx.map(lambda i: DIR16_LABELS[int(i)] if pd.notna(i) else pd.NA)
    return pd.Categorical(out, categories=DIR16_LABELS, ordered=True)

def transformar(df, tp_bins = [0, 10, 13, 16, 20], hs_bins = [0, 0.35, 0.4, 0.45, 0.6]):
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

    if "error_code" in df.columns:
        df = df[df["error_code"] == 0]
    if "Fecha y Hora" in df.columns:
        df["date"] = pd.to_datetime(df["Fecha y Hora"])
    elif "Date" in df.columns:
        df["date"] = pd.to_datetime(df["Date"])
    else:
        df["date"] = pd.to_datetime(df[["year", "month", "day"]])
    # Coerce key numeric columns to numeric values; invalid parses become NaN
    for _col in ("dirtp_dgs", "tp_s", "hs_m"):
        if _col in df.columns:
            df[_col] = pd.to_numeric(df[_col], errors="coerce")

    df = df[df["dirtp_dgs"] >= 0]  # remove invalid negative directions


    # create radians column for direction using the coerced numeric degrees
    df['dirtp_rad'] = np.radians(df["dirtp_dgs"]) if "dirtp_dgs" in df.columns else np.nan

    # select only the columns we need for downstream steps
    df = df[["date", "dirtp_dgs", "dirtp_rad", "tp_s", "hs_m"]]

    # Drop rows that have missing values in any of the required measurement columns.
    # Use assignment (avoid inplace) and copy to ensure a clean DataFrame view.
    df = df.dropna(subset=["dirtp_dgs", "tp_s", "hs_m"]).copy()

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
