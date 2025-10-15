from matplotlib import pyplot as plt
from extract import extract
from report import report_corrientes, report_olas, report_sedimentos
from visualizations import get_occurrence_table
from transform import transformar, transformar_corrientes, transformar_sedimentos
from config import CONFIG_ANALISIS

if __name__ == "__main__":
    # Configuración personalizable
    for con in CONFIG_ANALISIS:
        estacion = con.get('estacion', 'estacion')
        hs_bins = con.get('hs_bins', [0, 0.35, 0.4, 0.45, 0.6])
        tp_bins = con.get('tp_bins', [0, 10, 13, 16, 20])
        cols_rename = con.get('cols_rename', None)
        analisis = con.get('analisis', None)

        #1. Extraer la datair
        df = extract(con['path'])

        #2. Limpiar y transformar datos
        if analisis == 'olas':
            print("Procesando olas...")
            df = transformar(df, tp_bins, hs_bins, cols_rename)
            df.to_excel(f'out/data_limpia_olas_{estacion}.xlsx')

            #Estas filas las cree temporalmente para la tabla de ocurrencias de la tabla histórica.
            #fig_table_ocurrence, ax_table_ocurrence = plt.subplots()
            #get_occurrence_table(fig_table_ocurrence, ax_table_ocurrence, df, precision = 2, export_xlsx = True, estacion = estacion)

            #3. Plotear — crear figuras separadas para cada gráfico (cada figura irá en su propia página del PDF)
            report_olas(df, con)

        if analisis == 'corrientes':
            print("Procesando corrientes...")
            df = transformar_corrientes(df, con['cols_rename'], con['cols_drop'], con['cols_capas'])
            df.to_excel(f'out/data_limpia_corrientes_{estacion}.xlsx')

            report_corrientes(df, con)

        if analisis == 'sedimentos':
            print("Procesando sedimentos...")
            df = transformar_sedimentos(df, cols_rename)
            df.to_excel(f'out/data_limpia_sedimentos.xlsx')

            report_sedimentos(df, con)






