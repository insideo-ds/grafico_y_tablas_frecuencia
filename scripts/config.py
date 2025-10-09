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
        'path': './in/ADCP1-olas invierno -2022.xlsx',
        'adcp': 'adcp1',
        'hs_bins': [0.15, 0.2, 0.25, 0.3, 0.4],
        'tp_bins': [0, 10, 12, 14, 16, 20],
        'report_title': 'Olas_ADCP1_invierno2022',
        'limpieza': 'olas'
    },
    {
        'path': './in/ADCP2-Olas verano - 2023.xlsx',
        'adcp': 'adcp2',
        'hs_bins': [0.35, 0.4, 0.45, 0.6],
        'tp_bins': [0, 10, 13, 16, 20],
        'report_title': 'Olas_ADCP2_verano2023',
        'limpieza': 'olas'
    },
    {
        'path': './in/ADCP3-Olas verano-2023.xlsx',
        'adcp': 'adcp3',
        'hs_bins': [0.3, 0.4, 0.5, 0.6, 0.8],
        'tp_bins': [0, 10, 12, 14, 16, 20],
        'report_title': 'Olas_ADCP3_verano2023',
        'limpieza': 'olas'
    },
        {
        'path': './in/ADCP2_corrientes Verano 2023.xlsx',
        'adcp': 'adcp2',
        'v_bins': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        'report_title': 'Corrientes_ADCP2_verano2023',
        'limpieza': 'corrientes'
    }
]

"""     {
        'path': './in/ADCP2_corrientes Verano 2023.xlsx',
        'direccion_grados': 'Dir#1(1.4m)',
        'columna_valor': 'Speed#1(1.4m)',
        'rangos_valor': [0, 5, 10, 15, 20, 25],
        'nombre_salida': 'Corrientes_1.4m'
    } """
