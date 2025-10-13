
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
        'Maximum height (Hmax)': 'hmax_m',
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
    for _col in ("dirtp_dgs", "tp_s", "hs_m", "hmax_m"):
        if _col in df.columns:
            df[_col] = pd.to_numeric(df[_col], errors="coerce")

    df = df[df["dirtp_dgs"] >= 0]  # remove invalid negative directions

    # create radians column for direction using the coerced numeric degrees
    df['dirtp_rad'] = np.radians(df["dirtp_dgs"]) if "dirtp_dgs" in df.columns else np.nan

    # select only the columns we need for downstream steps
    df = df[["date", "dirtp_dgs", "dirtp_rad", "tp_s", "hs_m", "hmax_m"]]

    # Drop rows that have missing values in any of the required measurement columns.
    # Use assignment (avoid inplace) and copy to ensure a clean DataFrame view.
    df = df.dropna(subset=["dirtp_dgs", "tp_s", "hs_m"]).copy()

    df['dir_bins16'] = deg_to_dir16(df["dirtp_dgs"])
    df['tp_bins'] = pd.cut(df["tp_s"],bins=tp_bins,right=False) #left-inclusive and right-exclusive
    df['hs_bins'] = pd.cut(df["hs_m"],bins=hs_bins,right=False) #left-inclusive and right-exclusive

    return df

def transformar_corrientes(df, cols_rename, cols_drop, cols_capas):

    dir_fondo = cols_capas.get('dir_fondo', 'dir_fondo')
    speed_fondo = cols_capas.get('speed_fondo', 'speed_fondo')
    dir_medio = cols_capas.get('dir_medio', 'dir_medio')
    speed_medio = cols_capas.get('speed_medio', 'speed_medio')
    dir_sup = cols_capas.get('dir_sup', 'dir_sup')
    speed_sup = cols_capas.get('speed_sup', 'speed_sup')

    df = df.copy()
    df.columns = df.columns.str.strip()
    df.drop(columns = cols_drop, errors='ignore', inplace=True)
    df.rename(columns = cols_rename, inplace = True)

    dir_cols = df.columns[df.columns.str.contains('dir', case=False)]
    speed_cols = df.columns[df.columns.str.contains('speed', case=False)]

    df["date"] = pd.to_datetime(df["date"])
    # Coerce key numeric columns to numeric values; invalid parses become NaN
    for _col in speed_cols:
        df[_col] = df[_col]*100 if _col in df.columns else np.nan # Convertir velocidad de metros a cm.

    for _col in dir_cols.union(speed_cols):
        if _col in df.columns:
            df[_col] = pd.to_numeric(df[_col], errors="coerce").mask(lambda x: x < 0)
    # Drop rows that have missing values in any of the required measurement columns.
    df = df.dropna(subset=dir_cols.union(speed_cols)).copy()

    # create radians column for direction using the coerced numeric degrees
    df['speed_fondo_cms'] = df[speed_fondo] if speed_fondo in df.columns else np.nan
    df['speed_medio_cms'] = df[speed_medio] if speed_medio in df.columns else np.nan
    df['speed_sup_cms'] = df[speed_sup] if speed_sup in df.columns else np.nan
    df['dir_fondo_rad'] = np.radians(df[dir_fondo]) if dir_fondo in df.columns else np.nan
    df['dir_medio_rad'] = np.radians(df[dir_medio]) if dir_medio in df.columns else np.nan
    df['dir_sup_rad'] = np.radians(df[dir_sup]) if dir_sup in df.columns else np.nan
    df['dir_fondo_bins16'] = deg_to_dir16(df[dir_fondo])
    df['dir_medio_bins16'] = deg_to_dir16(df[dir_medio])
    df['dir_sup_bins16'] = deg_to_dir16(df[dir_sup])

    # Calcular la velocidad y dirección promedio de cada registro.
    calcular_componentes_capas(df, dir_cols, speed_cols, dir_fondo, dir_medio, dir_sup)

    return df

def calcular_componentes_capas(df, dir_cols, speed_cols, dir_fondo, dir_medio, dir_sup):
    # Convertir direcciones a radianes

    for col in dir_cols:
        df[f'{col}_rad'] = np.radians(df[col])

    # Calcular componentes U (zonal-x) y V (meridional-y) para cada capa
    u_cols = []
    v_cols = []
    for dir_col, speed_col in zip(dir_cols, speed_cols):
        u_col = f'u_{dir_col}'
        v_col = f'v_{dir_col}'
        df[u_col] = df[speed_col] * np.sin(df[f'{dir_col}_rad'])
        df[v_col] = df[speed_col] * np.cos(df[f'{dir_col}_rad'])
        u_cols.append(u_col)
        v_cols.append(v_col)

    calcular_promedios_capas(df, u_cols, v_cols)
    calcular_promedios_capas(df, [f'u_{dir_fondo}', f'u_{dir_medio}', f'u_{dir_sup}'], [f'v_{dir_fondo}', f'v_{dir_medio}', f'v_{dir_sup}'])
    return df

def calcular_promedios_capas(df, u_cols, v_cols):
    suffix = len(u_cols)
    # Calcular promedios de U y V
    df[f'u_promedio_{suffix}'] = df[u_cols].mean(axis=1)
    df[f'v_promedio_{suffix}'] = df[v_cols].mean(axis=1)

    # Calcular velocidad y dirección promedio
    df[f'speed_promedio_{suffix}'] = np.sqrt(df[f'u_promedio_{suffix}']**2 + df[f'v_promedio_{suffix}']**2)
    df[f'dir_promedio_rad_{suffix}'] = np.arctan2(df[f'u_promedio_{suffix}'], df[f'v_promedio_{suffix}']) # Elige el cuadrante correcto.
    df[f'dir_promedio_dgs_{suffix}'] = (np.degrees(df[f'dir_promedio_rad_{suffix}']) + 360) % 360 # Convertir a grados y ajustar a [0, 360)
