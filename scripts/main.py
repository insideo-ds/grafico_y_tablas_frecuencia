import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

from extract import extract
from transform import get_bars, transformar, transformar_corrientes
from visualizations import get_polar_rose_plot, get_table_frequency, get_histogram, get_time_series, get_polar_from_windrose
from config import CONFIG
from windrose import WindroseAxes

if __name__ == "__main__":
    # Configuración personalizable
    for con in CONFIG:
        report_title = con.get('report_title', 'report')
        adcp = con.get('adcp', 'adcp')
        hs_bins = con.get('hs_bins', [0, 0.35, 0.4, 0.45, 0.6])
        tp_bins = con.get('tp_bins', [0, 10, 13, 16, 20])
        v_bins = con.get('v_bins', [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
        limpieza = con.get('limpieza', None)

        #1. Extraer la datair
        df = extract(con['path'])

        #2. Limpiar y transformar datos
        if limpieza == 'olas':
            print("Procesando corrientes...")
            df = transformar(df, tp_bins, hs_bins)
            df.to_excel(f'out/data_limpia_olas_{adcp}.xlsx')

            #3. Plotear — crear figuras separadas para cada gráfico (cada figura irá en su propia página del PDF)

            # Dp: barras
            fig_dir_bars, ax_dir_bars = plt.subplots(figsize=(8, 6))
            get_bars(ax_dir_bars, df, eje_x='dir_bins16')

            # Dp: serie temporal
            fig_dir_ts, ax_dp_ts = plt.subplots(figsize=(10, 4))
            get_time_series(ax_dp_ts, df, 'date', 'dirtp_dgs', 'Fecha', 'dir_dgs', 'Serie temporal de dir_dgs')

            # HS: serie temporal
            fig_hs_ts, ax_hs_ts = plt.subplots(figsize=(10, 4))
            get_time_series(ax_hs_ts, df, 'date', 'hs_m', 'Fecha', 'hs_m', 'Serie temporal de hs_m')

            # HS: barras
            fig_hs_bars, ax_hs_bars = plt.subplots(figsize=(8, 6))
            get_bars(ax_hs_bars, df, eje_x='hs_bins')

            # HS: rosa
            fig_hs_rose, ax_hs_rose = plt.subplots(figsize=(8, 6))
            get_polar_rose_plot(ax_hs_rose, df, r='hs_m', theta='dirtp_rad', intervals=hs_bins)

            # HS: rosa (plotly/windrose lib)
            fig_hs_rose_wr, ax_hs_rose_wr = plt.subplots(figsize=(8, 6))
            get_polar_from_windrose(fig_hs_rose_wr, df, 'hs_m', hs_bins)

            # HS: tabla
            fig_hs_table, ax_hs_table = plt.subplots(figsize=(8.27, 11.69))
            get_table_frequency(ax_hs_table, df, eje_y='dir_bins16', eje_x='hs_bins')

            # TP: serie temporal
            fig_tp_ts, ax_tp_ts = plt.subplots(figsize=(10, 4))
            get_time_series(ax_tp_ts, df, 'date', 'tp_s', 'Fecha', 'tp_s', 'Serie temporal de tp_s')

            # TP: barras
            fig_tp_bars, ax_tp_bars = plt.subplots(figsize=(8, 6))
            get_bars(ax_tp_bars, df, eje_x='tp_bins')

            # TP: rosa
            fig_tp_rose, ax_tp_rose = plt.subplots(figsize=(8, 6))
            get_polar_rose_plot(ax_tp_rose, df, r='tp_s', theta='dirtp_rad', intervals=tp_bins)

            # TP: rosa (plotly/windrose lib)
            fig_tp_rose_wr, ax_tp_rose_wr = plt.subplots(figsize=(8, 6))
            get_polar_from_windrose(fig_tp_rose_wr, df, 'tp_s', tp_bins)

            # TP: tabla
            fig_tp_table, ax_tp_table = plt.subplots(figsize=(8.27, 11.69))
            get_table_frequency(ax_tp_table, df, eje_y='dir_bins16', eje_x='tp_bins')

            # HS y TP: tabla
            fig_hs_tp_table, ax_hs_tp_table = plt.subplots(figsize=(8.27, 11.69))
            get_table_frequency(ax_hs_tp_table, df, eje_y='hs_bins', eje_x='tp_bins')

            # Save plots and tables to a multi-page PDF
            out_dir = os.path.join('out')
            os.makedirs(out_dir, exist_ok=True)
            pdf_path = os.path.join(out_dir, f"{report_title}.pdf")

            with PdfPages(pdf_path) as pdf:
                # Title / cover page for this config
                try:
                    fig_title = plt.figure(figsize=(8.27, 11.69))
                    fig_title.clf()
                    fig_title.text(0.5, 0.5, report_title, ha='center', va='center', fontsize=24, weight='bold')
                    pdf.savefig(fig_title)
                    plt.close(fig_title)
                except Exception:
                    pass

                # DIR section cover
                try:
                    fig_dir_title = plt.figure(figsize=(8.27, 11.69))
                    fig_dir_title.clf()
                    dir_title_text = f"DIR"
                    fig_dir_title.text(0.5, 0.6, dir_title_text, ha='center', va='center', fontsize=22, weight='bold')
                    fig_dir_title.text(0.5, 0.45, f"{adcp}", ha='center', va='center', fontsize=12)
                    pdf.savefig(fig_dir_title)
                    plt.close(fig_dir_title)
                except Exception:
                    pass

                # Save DIR figures
                for fig_obj in [fig_dir_bars, fig_dir_ts]:
                    try:
                        fig_obj.tight_layout()
                    except Exception:
                        pass
                    pdf.savefig(fig_obj)
                    plt.close(fig_obj)

                # HS section cover
                try:
                    fig_hs_title = plt.figure(figsize=(8.27, 11.69))
                    fig_hs_title.clf()
                    hs_title_text = f"HS"
                    fig_hs_title.text(0.5, 0.6, hs_title_text, ha='center', va='center', fontsize=22, weight='bold')
                    fig_hs_title.text(0.5, 0.45, f"{adcp}", ha='center', va='center', fontsize=12)
                    pdf.savefig(fig_hs_title)
                    plt.close(fig_hs_title)
                except Exception:
                    pass

                # Save HS figures
                for fig_obj in [fig_hs_ts, fig_hs_bars, fig_hs_rose, fig_hs_rose_wr, fig_hs_table]:
                    try:
                        fig_obj.tight_layout()
                    except Exception:
                        pass
                    pdf.savefig(fig_obj)
                    plt.close(fig_obj)

                # TP section cover
                try:
                    fig_tp_title = plt.figure(figsize=(8.27, 11.69))
                    fig_tp_title.clf()
                    tp_title_text = f"TP"
                    fig_tp_title.text(0.5, 0.6, tp_title_text, ha='center', va='center', fontsize=22, weight='bold')
                    fig_tp_title.text(0.5, 0.45, f"{adcp}", ha='center', va='center', fontsize=12)
                    pdf.savefig(fig_tp_title)
                    plt.close(fig_tp_title)
                except Exception:
                    pass

                # Save TP figures
                for fig_obj in [fig_tp_ts, fig_tp_bars, fig_tp_rose, fig_tp_rose_wr, fig_tp_table, fig_hs_tp_table]:
                    try:
                        fig_obj.tight_layout()
                    except Exception:
                        pass
                    pdf.savefig(fig_obj)
                    plt.close(fig_obj)

        else:
            print("Procesando corrientes...")
            df = transformar_corrientes(df)
            df.to_excel(f'out/data_limpia_corrientes_{adcp}.xlsx')

            #3. Plotear — crear figuras separadas para cada gráfico (cada figura irá en su propia página del PDF)
            fig_v1_4_rose, ax_v1_4_rose = plt.subplots(figsize=(8, 6))
            get_polar_rose_plot(ax_v1_4_rose, df, r='speed_1.4_ms', theta='dir_1.4_rad', intervals=v_bins)

            fig_v5_4_rose, ax_v5_4_rose = plt.subplots(figsize=(8, 6))
            get_polar_rose_plot(ax_v5_4_rose, df, r='speed_5.4_ms', theta='dir_5.4_rad', intervals=v_bins)

            fig_v10_4_rose, ax_v10_4_rose = plt.subplots(figsize=(8, 6))
            get_polar_rose_plot(ax_v10_4_rose, df, r='speed_10.4_ms', theta='dir_10.4_rad', intervals=v_bins)

            # Save plots and tables to a multi-page PDF
            out_dir = os.path.join('out')
            os.makedirs(out_dir, exist_ok=True)
            pdf_path = os.path.join(out_dir, f"{report_title}.pdf")

            with PdfPages(pdf_path) as pdf:
                # Title / cover page for this config
                try:
                    fig_title = plt.figure(figsize=(8.27, 11.69))
                    fig_title.clf()
                    fig_title.text(0.5, 0.5, report_title, ha='center', va='center', fontsize=24, weight='bold')
                    pdf.savefig(fig_title)
                    plt.close(fig_title)
                except Exception:
                    pass

                # Save HS figures
                for fig_obj in [fig_v1_4_rose, fig_v5_4_rose, fig_v10_4_rose]:
                    try:
                        fig_obj.tight_layout()
                    except Exception:
                        pass
                    pdf.savefig(fig_obj)
                    plt.close(fig_obj)

        # Optionally show the main plot interactively (comment out to run headless)
        # plt.show()

        # Guardar resultados
        #plt.savefig(f'{nombre_salida}_rosa.png', dpi=300, bbox_inches='tight')
        #tabla_frecuencias.to_excel(f'{nombre_salida}_tabla_frecuencias.xlsx')




