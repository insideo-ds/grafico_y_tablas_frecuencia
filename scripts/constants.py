"""Project-wide constants for direction sectors and cardinal labels.

These are used by `main.py` and `visualizations.py`.
"""

# Labels for the 16 compass points, ordered clockwise starting at North
DIR16_LABELS = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
]

CONFIG = [
    {
        'path': './in/ADCP2-Olas verano - 2023.xlsx',
        'direccion_grados': 'Peak direction (DirTp)',
        'columna_valor': 'Peak period (Tp)',
        'rangos_valor': [0, 5, 10, 15, 20, 25],
        'nombre_salida': 'Olas_DirTp_Tp'
    },
]

"""     {
        'path': './in/ADCP2_corrientes Verano 2023.xlsx',
        'direccion_grados': 'Dir#1(1.4m)',
        'columna_valor': 'Speed#1(1.4m)',
        'rangos_valor': [0, 5, 10, 15, 20, 25],
        'nombre_salida': 'Corrientes_1.4m'
    } """
