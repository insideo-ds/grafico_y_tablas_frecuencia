"""Project-wide constants for direction sectors and cardinal labels.

These are used by `main.py` and `visualizations.py`.
"""

# Labels for the 16 compass points, ordered clockwise starting at North
DIR16_LABELS = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
]

CONFIG_SEDIMENTOS = [
    {
        'path': './in/Sedimentos.xlsx',
        'report_title': 'Sedimentos',
        'analisis': 'sedimentos',
        'cols_rename': {
            'Estación de Muestreo': 'estacion',
            'Fecha de Muestreo': 'date',
            'Hora de Muestreo': 'hora',
            'Peso de la Muestra (g)': 'peso_muestra_g',
            'Código de Laboratorio': 'codigo_laboratorio',
            'Georeferencia': 'georeferencia',
            'Metriz': 'matriz',
            'MALLA - 10  (g)': 'malla_pas_10g', # pasa malla 10 = retenido en malla 18
            'MALLA + 10  (g)': 'malla_ret_10g', # no pasa malla 10
            'MALLA - 18  (g)': 'malla_pas_18g',
            'MALLA + 18  (g)': 'malla_ret_18g',
            'MALLA - 35  (g)': 'malla_pas_35g',
            'MALLA + 35  (g)': 'malla_ret_35g',
            'MALLA - 50  (g)': 'malla_pas_50g',
            'MALLA + 50  (g)': 'malla_ret_50g',
            'MALLA - 100  (g)': 'malla_pas_100g',
            'MALLA + 100  (g)': 'malla_ret_100g',
            'MALLA - 200  (g)': 'malla_pas_200g',
            'MALLA + 200  (g)': 'malla_ret_200g',
            'MALLA - 400  (g)': 'malla_pas_400g',
            'MALLA + 400  (g)': 'malla_ret_400g',
        },
    },
]

CONFIG_OLAS_HISTORICAS_TP_BINS = [
    {
        'path': './in/Data-Historica-Olas-Periodo_1979_2024.xlsx',
        'estacion': 'CSIRO_bins',
        'hs_bins': [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5],
        'tp_bins': [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32],
        'report_title': 'Olas_historicas_1979_2024',
        'analisis': 'olas',
        'cols_rename': {
            'Fecha': 'Date',
            'HORA': 'Hour',
            'Hs': 'hs_m',
            'Dp': 'dirtp_dgs',
            'Tp': 'tp_s',
        },
    }
]

CONFIG_OLAS_HISTORICAS = [
    {
        'path': './in/Data-Historica-Olas-Periodo_1979_2024.xlsx',
        'estacion': 'CSIRO',
        'hs_bins': [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5],
        'tp_bins': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32],
        'report_title': 'Olas_historicas_1979_2024',
        'analisis': 'olas',
        'cols_rename': {
            'Fecha': 'Date',
            'HORA': 'Hour',
            'Hs': 'hs_m',
            'Dp': 'dirtp_dgs',
            'Tp': 'tp_s',
        },
    }
]

CONFIG_CORRIENTES = [
    {
        'path': './in/ADCP2_corrientes Verano 2023.xlsx',
        'estacion': 'ADCP 2',
        'v_bins': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        'report_title': 'Corrientes_ADCP2_verano2023',
        'analisis': 'corrientes',
        'cols_rename': {
            'DateTime': 'date',
            },
        'cols_capas': {
            'dir_fondo': 'Dir#1(1.4m)',
            'speed_fondo': 'Speed#1(1.4m)',
            'dir_medio': 'Dir#5(5.4m)',
            'speed_medio': 'Speed#5(5.4m)',
            'dir_sup': 'Dir#10(10.4m)',
            'speed_sup': 'Speed#10(10.4m)'
        },
        'cols_drop': ['Battery', 'Heading', 'Pitch', 'Roll', 'AnalogIn1', 'AnalogIn2', 'AnalogIn3']
    },
    {
        'path': './in/ADCP4_Corrientes Invierno-2023.xlsx',
        'estacion': 'ADCP 4',
        'v_bins': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        'report_title': 'Corrientes_ADCP4_invierno2023',
        'analisis': 'corrientes',
        'cols_rename': {
            'DateTime': 'date',
        },
        'cols_capas': {
            'dir_fondo': 'Dir#1(1.5m)',
            'speed_fondo': 'Speed#1(1.5m)',
            'dir_medio': 'Dir#7(7.5m)',
            'speed_medio': 'Speed#7(7.5m)',
            'dir_sup': 'Dir#12(12.5m)',
            'speed_sup': 'Speed#12(12.5m)'
        },
        'cols_drop': ['Battery', 'Heading', 'Pitch', 'Roll', 'Pressure', 'Temperature', 'AnalogIn1', 'AnalogIn2', 'AnalogIn3']
    }
]
CONFIG_OLAS = [
    {
        'path': './in/ADCP1-olas invierno -2022.xlsx',
        'estacion': 'ADCP 1',
        'hs_bins': [0.15, 0.2, 0.25, 0.3, 0.4],
        'tp_bins': [0, 10, 12, 14, 16, 20],
        'report_title': 'Olas_ADCP1_invierno2022',
        'analisis': 'olas',
        'cols_rename': {
            'Month': 'month',
            'Day': 'day',
            'Year': 'year',
            'Significant height (Hm0)': 'hs_m',
            'Maximum height (Hmax)': 'hmax_m',
            'Peak direction (DirTp)': 'dirtp_dgs',
            'Peak period (Tp)': 'tp_s',
            'Error Code': 'error_code'
        },
    },
    {
        'path': './in/ADCP2-Olas verano - 2023-09-10-25.xlsx',
        'estacion': 'ADCP 2',
        'hs_bins': [0.35, 0.4, 0.45, 0.6],
        'tp_bins': [0, 10, 13, 16, 20],
        'report_title': 'Olas_ADCP2_verano2023',
        'analisis': 'olas',
        'cols_rename': {
            'Month': 'month',
            'Day': 'day',
            'Year': 'year',
            'Significant height (Hm0)': 'hs_m',
            'Maximum height (Hmax)': 'hmax_m',
            'Peak direction (DirTp)': 'dirtp_dgs',
            'Peak period (Tp)': 'tp_s',
            'Error Code': 'error_code'
        },
    },
    {
        'path': './in/ADCP3-Olas verano-2023.xlsx',
        'estacion': 'ADCP 3',
        'hs_bins': [0.3, 0.4, 0.5, 0.6, 0.8],
        'tp_bins': [0, 10, 12, 14, 16, 20],
        'report_title': 'Olas_ADCP3_verano2023',
        'analisis': 'olas',
        'cols_rename': {
            'Month': 'month',
            'Day': 'day',
            'Year': 'year',
            'Significant height (Hm0)': 'hs_m',
            'Maximum height (Hmax)': 'hmax_m',
            'Peak direction (DirTp)': 'dirtp_dgs',
            'Peak period (Tp)': 'tp_s',
            'Error Code': 'error_code'
        },
    }
]

CONFIG_OLAS_ADCP2_OLD = [
    {
        'path': './in/ADCP2-Olas verano - 2023.xlsx',
        'estacion': 'adcp2',
        'hs_bins': [0.35, 0.4, 0.45, 0.6],
        'tp_bins': [0, 10, 13, 16, 20],
        'report_title': 'Olas_ADCP2_verano2023',
        'analisis': 'olas'
    }
]

CONFIG_ANALISIS = CONFIG_SEDIMENTOS