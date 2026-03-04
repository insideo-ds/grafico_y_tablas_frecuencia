
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

def transformar(df, tp_bins = [0, 10, 13, 16, 20], hs_bins = [0, 0.35, 0.4, 0.45, 0.6], cols_rename=None):
    '''La data de velocidad debe estar en m/s. Se convierte a cm/s'''
    df = df.copy()
    df.columns = df.columns.str.strip()

    if cols_rename:
        df.rename(columns = cols_rename, inplace = True)

    if "error_code" in df.columns:
        df = df[df["error_code"] == 0]
    if "Fecha y Hora" in df.columns:
        df["date"] = pd.to_datetime(df["Fecha y Hora"])
    elif "ate" in df.columns and "Hour" in df.columns:
        # Combine separate Date and Hour columns to preserve time
        df["date"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Hour"].astype(str), errors='coerce')
    elif "Date" in df.columns:
        df["date"] = pd.to_datetime(df["Date"])
    elif "year" in df.columns and "month" in df.columns and "day" in df.columns:
        # Combine year/month/day with hour if present
        if "hour" in df.columns:
            df["date"] = pd.to_datetime(df[["year", "month", "day", "hour"]], errors='coerce')
        else:
            df["date"] = pd.to_datetime(df[["year", "month", "day"]])
    else:
        # Fallback for any other date-like column
        df["date"] = pd.to_datetime(df.get("date", None), errors='coerce')
    # Coerce key numeric columns to numeric values; invalid parses become NaN
    for _col in ("dirtp_dgs", "tp_s", "hs_m", "hmax_m"):
        if _col in df.columns:
            df[_col] = pd.to_numeric(df[_col], errors="coerce")

    # filter out rows where maximum height is less than significant height
    if "hmax_m" in df.columns and "hs_m" in df.columns:
        df = df[df["hmax_m"] >= df["hs_m"]]

    df = df[df["dirtp_dgs"] >= 0]  # remove invalid negative directions

    # create radians column for direction using the coerced numeric degrees
    df['dirtp_rad'] = np.radians(df["dirtp_dgs"]) if "dirtp_dgs" in df.columns else np.nan

    # select only the columns we need for downstream steps
    #df = df[["date", "dirtp_dgs", "dirtp_rad", "tp_s", "hs_m", "hmax_m"]]

    # Drop rows that have missing values in any of the required measurement columns.
    # Use assignment (avoid inplace) and copy to ensure a clean DataFrame view.
    df = df.dropna(subset=["dirtp_dgs", "tp_s", "hs_m"]).copy()

    # Remove tp_s outliers using IQR (Interquartile Range) method
    if "tp_s" in df.columns and len(df) > 0:
        Q1 = df["tp_s"].quantile(0.25)
        Q3 = df["tp_s"].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df["tp_s"] >= lower_bound) & (df["tp_s"] <= upper_bound)].copy()

    df['dir_bins16'] = deg_to_dir16(df["dirtp_dgs"])
    df['tp_bins'] = pd.cut(df["tp_s"],bins=tp_bins,right=False) #left-inclusive and right-exclusive
    df['hs_bins'] = pd.cut(df["hs_m"],bins=hs_bins,right=False) #left-inclusive and right-exclusive

    print(df.head())
    return df

def transformar_corrientes(df, cols_rename, cols_drop, cols_capas):
    '''La data de velocidad debe estar en m/s. Se convierte a cm/s'''
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

def transformar_sedimentos(df, cols_rename, cols_drop = None):

    df = df.copy()
    df.columns = df.columns.str.strip()
    if cols_drop:
        df.drop(columns = cols_drop, errors='ignore', inplace=True)
    df.rename(columns = cols_rename, inplace = True)
    df["date"] = pd.to_datetime(df["date"])

    malla_cols = [col for col in df.columns if "malla_ret" in col] # o malla_cols = df.columns[df.columns.str.contains('malla_ret', case=False)]

    # Coerce key numeric columns to numeric values; invalid parses become NaN
    for _col in malla_cols:
        if _col in df.columns:
            df[_col] = pd.to_numeric(df[_col], errors="coerce").mask(lambda x: x < 0)
    # Drop rows that have missing values in any of the required measurement columns.
    df = df.dropna(subset=malla_cols).copy()

    #Enriquecimiento
    df["total_retenido_g"] = df[malla_cols].sum(axis=1)
    # Calcular porcentaje retenido por malla
    for col in malla_cols:
        df[f"%_{col}"] = (df[col] / df["peso_muestra_g"]) * 100

    # Calcular % retenido acumulado
    pct_cols = [f"%_{col}" for col in malla_cols]
    df["%_retenido_Acumulado"] = df[pct_cols].cumsum(axis=1).iloc[:, -1]

    # Calcular % que pasa por cada malla
    for col in malla_cols:
        df[f"%_pasa_{col}"] = 100 - df[[f"%_{c}" for c in malla_cols]].cumsum(axis=1)[f"%_{col}"]

    df["arena muy gruesa"] = df["%_malla_ret_10g"]
    df["arena gruesa"] = df["%_malla_ret_18g"]
    df["arena fina"] = df["%_malla_ret_35g"] + df["%_malla_ret_50g"]
    df["arena muy fina"] = df["%_malla_ret_100g"] + df["%_malla_ret_200g"]
    df["limo"] = df["%_pasa_malla_ret_200g"] #incluye malla 400
    #df.drop(subset=malla_cols)

    return df

"""
| Malla               | Representa el material que...           | Tamaño aproximado |
| ------------------- | --------------------------------------- | ----------------- |
| **#10**             | Es más grueso que #10 (no pasa por #10) | > 2 mm            |
| **#18**             | Pasa por #10 pero no por #18            | 1.0 – 2.0 mm      |
| **#35**             | Pasa por #18 pero no por #35            | 0.5 – 1.0 mm      |
| **#50**             | Pasa por #35 pero no por #50            | 0.3 – 0.5 mm      |
| **#100**            | Pasa por #50 pero no por #100           | 0.15 – 0.3 mm     |
| **#200**            | Pasa por #100 pero no por #200          | 0.075 – 0.15 mm   |
| **Fondo (bandeja)** | Pasa por #200                           | < 0.075 mm        |

"""