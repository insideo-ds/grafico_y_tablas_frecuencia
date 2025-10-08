
import pandas as pd
import numpy as np
from math import radians

from constants import SECTORES, CARDINALES

def transformar(df, direccion_grados, columna_valor, rangos_valor, nombre_salida=None):

    if direccion_grados not in df.columns:
        raise ValueError(f"Columna {direccion_grados} no encontrada")
    if columna_valor not in df.columns:
        raise ValueError(f"Columna {columna_valor} no encontrada")

    df_clean = df[['Peak direction (DirTp)', 'Peak period (Tp)', 'Significant height (Hm0)', 'Error Code']].dropna()
    df_clean['dir_rad'] = np.radians(df_clean[direccion_grados])

    df_clean['sector_direccion'] = pd.cut(
        df_clean[direccion_grados] % 360,
        bins=np.linspace(0, 360, SECTORES + 1),
        labels=CARDINALES,
        right=False
    )
    df_clean['rango_valor'] = pd.cut(
        df_clean[columna_valor],
        bins=rangos_valor,
        right=False
    )

    return df_clean