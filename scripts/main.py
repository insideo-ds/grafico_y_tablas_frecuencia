from extract import extract
from report import report_corrientes, report_olas
from transform import transformar, transformar_corrientes
from config import CONFIG_CORRIENTES

if __name__ == "__main__":
    # Configuración personalizable
    for con in CONFIG_CORRIENTES:
        adcp = con.get('adcp', 'adcp')
        hs_bins = con.get('hs_bins', [0, 0.35, 0.4, 0.45, 0.6])
        tp_bins = con.get('tp_bins', [0, 10, 13, 16, 20])

        limpieza = con.get('limpieza', None)

        #1. Extraer la datair
        df = extract(con['path'])

        #2. Limpiar y transformar datos
        if limpieza == 'olas':
            print("Procesando corrientes...")
            df = transformar(df, tp_bins, hs_bins)
            df.to_excel(f'out/data_limpia_olas_{adcp}.xlsx')

            #3. Plotear — crear figuras separadas para cada gráfico (cada figura irá en su propia página del PDF)
            report_olas(df, con)

        if limpieza == 'corrientes':
            print("Procesando corrientes...")
            df = transformar_corrientes(df, con['cols_rename'], con['cols_drop'], con['cols_capas'])
            df.to_excel(f'out/data_limpia_corrientes_{adcp}.xlsx')

            report_corrientes(df, con)

        # Guardar resultados
        #plt.savefig(f'{nombre_salida}_rosa.png', dpi=300, bbox_inches='tight')
        #tabla_frecuencias.to_excel(f'{nombre_salida}_tabla_frecuencias.xlsx')




