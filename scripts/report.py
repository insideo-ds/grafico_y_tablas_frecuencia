import os
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from visualizations import get_bar_x_estacion, get_occurrence_table, get_polar_rose_plot, get_table_frequency, get_table_statistics_summary, get_time_series, get_polar_from_windrose, get_bars, get_histogram

# Optionally show the main plot interactively (comment out to run headless)
# plt.show()

def report_olas(df, con):
    report_title = con.get('report_title', 'report')
    estacion = con.get('estacion', 'estacion')
    hs_bins = con.get('hs_bins', [0, 0.35, 0.4, 0.45, 0.6])
    tp_bins = con.get('tp_bins', [0, 10, 13, 16, 20])

    # Dp: barras
    fig_dir_bars, ax_dir_bars = plt.subplots(figsize=(8, 6))
    get_bars(ax_dir_bars, df, eje_x='dir_bins16', xlabel='Dp(°)', ylabel='Frecuencia (%)')

    # Dp: serie temporal
    fig_dir_ts, ax_dp_ts = plt.subplots(figsize=(10, 4))
    get_time_series(ax_dp_ts, df, 'date', 'dirtp_dgs', 'Fecha', 'Dp [°]', 'Serie temporal de dir_dgs', labels={'dirtp_dgs': 'Dp'})

    # HS: serie temporal
    fig_hs_ts, ax_hs_ts = plt.subplots(figsize=(10, 4))
    get_time_series(ax_hs_ts, df, 'date', 'hs_m', 'Fecha', 'Hs [m]', 'Serie temporal de hs_m', labels={'hs_m': 'Hs'})

    # H_max: serie temporal máximos
    if 'hmax_m' in df.columns:
        fig_hs_max_ts, ax_hs_max_ts = plt.subplots(figsize=(10, 4))
        get_time_series(ax_hs_max_ts, df, 'date', 'hmax_m', 'Fecha', 'Hmax [m]', 'Serie temporal de hmax_m', labels={'hmax_m': 'Hmax'})
    else:
        fig_hs_max_ts = None
    # HS: barras
    fig_hs_bars, ax_hs_bars = plt.subplots(figsize=(8, 6))
    get_bars(ax_hs_bars, df, eje_x='hs_bins', xlabel='Hs (m)', ylabel='Frecuencia (%)')

    # HS: rosa
    fig_hs_rose, ax_hs_rose = plt.subplots(figsize=(8, 6))
    get_polar_rose_plot(ax_hs_rose, df, r='hs_m', theta='dirtp_rad', intervals=hs_bins)

    # HS: rosa (plotly/windrose lib)
    fig_hs_rose_wr, ax_hs_rose_wr = plt.subplots(figsize=(8, 6))
    fig_hs_rose_wr.delaxes(fig_hs_rose_wr.axes[0]) # eliminar el eje creado por plt.subplots() para que windrose pueda usar toda la figura
    get_polar_from_windrose(fig_hs_rose_wr, df, 'hs_m', 'dirtp_dgs', hs_bins, units='m', display_title='Hs')

    # HS: tabla
    fig_hs_table, ax_hs_table = plt.subplots()
    get_table_frequency(fig_hs_table, ax_hs_table, df, eje_y='dir_bins16', eje_x='hs_bins')

    # TP: serie temporal
    fig_tp_ts, ax_tp_ts = plt.subplots(figsize=(10, 4))
    get_time_series(ax_tp_ts, df, 'date', 'tp_s', 'Fecha', 'Tp [seg]', 'Serie temporal de tp_s', labels={'tp_s': 'Tp'})

    # TP: barras
    fig_tp_bars, ax_tp_bars = plt.subplots(figsize=(8, 6))
    get_bars(ax_tp_bars, df, eje_x='tp_bins', xlabel='Tp (s)', ylabel='Frecuencia (%)')

    # TP: rosa
    fig_tp_rose, ax_tp_rose = plt.subplots(figsize=(8, 6))
    get_polar_rose_plot(ax_tp_rose, df, r='tp_s', theta='dirtp_rad', intervals=tp_bins)

    # TP: rosa (plotly/windrose lib)
    fig_tp_rose_wr, ax_tp_rose_wr = plt.subplots(figsize=(8, 6))
    fig_tp_rose_wr.delaxes(fig_tp_rose_wr.axes[0]) # eliminar el eje creado por plt.subplots() para que windrose pueda usar toda la figura
    get_polar_from_windrose(fig_tp_rose_wr, df, 'tp_s', 'dirtp_dgs', tp_bins, units='s', display_title='Tp')

    # TP: tabla
    fig_tp_table, ax_tp_table = plt.subplots()
    get_table_frequency(fig_tp_table, ax_tp_table, df, eje_y='dir_bins16', eje_x='tp_bins')

    # HS y TP: tabla
    fig_hs_tp_table, ax_hs_tp_table = plt.subplots()
    get_table_frequency(fig_hs_tp_table, ax_hs_tp_table, df, eje_y='hs_bins', eje_x='tp_bins')

    fig_table_describe, ax_table_describe = plt.subplots()
    get_table_statistics_summary(fig_table_describe, ax_table_describe, df, colnames=['hs_m', 'dirtp_dgs', 'tp_s'])

    fig_table_ocurrence, ax_table_ocurrence = plt.subplots()
    get_occurrence_table(fig_table_ocurrence, ax_table_ocurrence, df, precision = 2, export_xlsx = True, estacion = estacion)


    # Save plots and tables to a multi-page PDF
    out_dir = os.path.join('out')
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, f"{report_title}.pdf")

    with PdfPages(pdf_path) as pdf:
        # Title / cover page for this config
        try:
            fig_title = plt.figure(figsize=(8.27, 11.69))
            fig_title.clear()
            fig_title.text(0.5, 0.5, report_title, ha='center', va='center', fontsize=24, weight='bold')
            pdf.savefig(fig_title)
            plt.close(fig_title)
        except Exception:
            pass

        # DIR section cover
        try:
            fig_dir_title = plt.figure(figsize=(8.27, 11.69))
            fig_dir_title.clear()
            dir_title_text = f"DIR"
            fig_dir_title.text(0.5, 0.6, dir_title_text, ha='center', va='center', fontsize=22, weight='bold')
            fig_dir_title.text(0.5, 0.45, f"{estacion}", ha='center', va='center', fontsize=12)
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
            fig_hs_title.clear()
            hs_title_text = f"HS"
            fig_hs_title.text(0.5, 0.6, hs_title_text, ha='center', va='center', fontsize=22, weight='bold')
            fig_hs_title.text(0.5, 0.45, f"{estacion}", ha='center', va='center', fontsize=12)
            pdf.savefig(fig_hs_title)
            plt.close(fig_hs_title)
        except Exception:
            pass

        # Save HS figures
        for fig_obj in [fig_hs_ts, fig_hs_max_ts, fig_hs_bars, fig_hs_rose_wr, fig_hs_rose, fig_hs_table]: #,
            try:
                fig_obj.tight_layout()
            except Exception:
                pass
            pdf.savefig(fig_obj)
            plt.close(fig_obj)

        # TP section cover
        try:
            fig_tp_title = plt.figure(figsize=(8.27, 11.69))
            fig_tp_title.clear()
            tp_title_text = f"TP"
            fig_tp_title.text(0.5, 0.6, tp_title_text, ha='center', va='center', fontsize=22, weight='bold')
            fig_tp_title.text(0.5, 0.45, f"{estacion}", ha='center', va='center', fontsize=12)
            pdf.savefig(fig_tp_title)
            plt.close(fig_tp_title)
        except Exception:
            pass

        # Save TP figures
        for fig_obj in [fig_tp_ts, fig_tp_bars, fig_tp_rose_wr, fig_tp_rose, fig_tp_table, fig_hs_tp_table, fig_table_describe, fig_table_ocurrence]: #,
            try:
                fig_obj.tight_layout()
            except Exception:
                pass
            pdf.savefig(fig_obj)
            plt.close(fig_obj)

def report_corrientes(df, con):
    report_title = con.get('report_title', 'report')
    v_bins = con.get('v_bins', [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])

    # Plotear — crear figuras separadas para cada gráfico (cada figura irá en su propia página del PDF)
    fig_sup_rose, ax_sup_rose = plt.subplots(figsize=(8, 6))
    get_polar_rose_plot(ax_sup_rose, df, r='speed_sup_cms', theta='dir_sup_rad', intervals=v_bins)

    fig_sup_rose_wr, ax_sup_rose_wr = plt.subplots(figsize=(8, 6))
    get_polar_from_windrose(fig_sup_rose_wr, df, r='speed_sup_cms', theta=con['cols_capas']['dir_sup'], bins=v_bins)

    fig_medio_rose, ax_medio_rose = plt.subplots(figsize=(8, 6))
    get_polar_rose_plot(ax_medio_rose, df, r='speed_medio_cms', theta='dir_medio_rad', intervals=v_bins)

    fig_fondo_rose, ax_fondo_rose = plt.subplots(figsize=(8, 6))
    get_polar_rose_plot(ax_fondo_rose, df, r='speed_fondo_cms', theta='dir_fondo_rad', intervals=v_bins)

    # Calibración
    dir_cols = df.columns[df.columns.str.contains('dir', case=False) & ~df.columns.str.contains('_')]
    speed_cols = df.columns[df.columns.str.contains('speed', case=False) & ~df.columns.str.contains('_')]
    suffix = len(dir_cols)
    fig_dir_ts, ax_dp_ts = plt.subplots(figsize=(10, 4))
    get_time_series(ax_dp_ts, df, 'date', f'dir_promedio_dgs_{suffix}', 'Fecha', 'dir_promedio_dgs', 'Serie temporal de dir_promedio_dgs')

    fig_v_ts, ax_v_ts = plt.subplots(figsize=(10, 4))
    get_time_series(ax_v_ts, df, 'date', f'speed_promedio_{suffix}', 'Fecha', 'speed_promedio', 'Serie temporal de speed_promedio')

    fig_promedio_rose, ax_promedio_rose = plt.subplots(figsize=(8, 6))
    get_polar_rose_plot(ax_promedio_rose, df, r=f'speed_promedio_{suffix}', theta=f'dir_promedio_rad_{suffix}', intervals=v_bins, normed = False)

    fig_promedio_rose_3, ax_promedio_rose_3 = plt.subplots(figsize=(8, 6))
    get_polar_rose_plot(ax_promedio_rose_3, df, r=f'speed_promedio_3', theta=f'dir_promedio_rad_3', intervals=v_bins, normed = False)

    # plotear rosas de viento por cada capa
    height_per_plot = 6
    fig_resumen_rose, ax_resumen_rose = plt.subplots(nrows=len(dir_cols), ncols=1, figsize=(8, height_per_plot*len(dir_cols)))
    for idx, (dir_col, speed_col) in enumerate(zip(dir_cols, speed_cols)):
        get_polar_rose_plot(ax_resumen_rose[idx], df, r=speed_col, theta=f'{dir_col}_rad', intervals=v_bins, normed = False)
        #get_polar_from_windrose(fig_sup_rose_wr, df, r='speed_sup_cms', theta=con['cols_capas']['dir_sup'], bins=v_bins)


    # Save plots and tables to a multi-page PDF
    out_dir = os.path.join('out')
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, f"{report_title}.pdf")

    with PdfPages(pdf_path) as pdf:
        # Title / cover page for this config
        try:
            fig_title = plt.figure(figsize=(8.27, 11.69))
            fig_title.clear()
            fig_title.text(0.5, 0.5, report_title, ha='center', va='center', fontsize=24, weight='bold')
            pdf.savefig(fig_title)
            plt.close(fig_title)
        except Exception:
            pass

        # Save HS figures
        for fig_obj in [fig_sup_rose_wr, fig_sup_rose, fig_medio_rose, fig_fondo_rose, fig_dir_ts, fig_v_ts, fig_promedio_rose, fig_promedio_rose_3, fig_resumen_rose]:
            try:
                fig_obj.tight_layout()
            except Exception:
                pass
            pdf.savefig(fig_obj)
            plt.close(fig_obj)

def report_sedimentos(df, con):
    report_title = con.get('report_title', 'report')

    # histograma
    rows = len(df)
    height_per_plot = 6
    fig_bar_sedimentos, ax_bar_sedimentos = plt.subplots(nrows=rows, ncols=1, figsize=(8, height_per_plot*rows))

    cols = ['date', 'estacion', 'arena muy gruesa', 'arena gruesa', 'arena fina', 'arena muy fina', 'limo']
    df = df.copy()[cols].reset_index() # añade la columna index

    df = pd.melt(
        df,
        id_vars=['index', 'date','estacion'],              # columns to keep fixed
        var_name='fraccion',             # name of new "variable" column
        value_name='porcentaje'          # name of new "value" column
    )

    print(df.head())
    for idx in range(rows):
        df_est = df[df['index'] == idx]
        get_bar_x_estacion(ax_bar_sedimentos[idx], df_est["fraccion"], df_est["porcentaje"])

    # Promedio por estación
    #df_mean = df.groupby('estacion')[cols].mean() #se agrupa para el ploteo
    #print(df_mean)

    #fig_bar_sedimentos, ax_bar_sedimentos = plt.subplots()
    # Crear gráfico de barras
    #df_mean.plot(kind='bar', figsize=(8, 6), ax=ax_bar_sedimentos)
    #ax_bar_sedimentos.set_ylabel('%')
    #ax_bar_sedimentos.set_title('Distribución granulométrica por estación') #apiladas, stacked=True
    #ax_bar_sedimentos.legend(title='Fracción', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save plots and tables to a multi-page PDF
    out_dir = os.path.join('out')
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, f"{report_title}.pdf")

    with PdfPages(pdf_path) as pdf:
        # Title / cover page for this config
        try:
            fig_title = plt.figure(figsize=(8.27, 11.69))
            fig_title.clear()
            fig_title.text(0.5, 0.5, report_title, ha='center', va='center', fontsize=24, weight='bold')
            pdf.savefig(fig_title)
            plt.close(fig_title)
        except Exception:
            pass

        # Save figures
        for fig_obj in [fig_bar_sedimentos]:
            try:
                fig_obj.tight_layout()
            except Exception:
                pass
            pdf.savefig(fig_obj)
            plt.close(fig_obj)