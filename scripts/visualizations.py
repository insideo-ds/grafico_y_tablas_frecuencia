import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import matplotlib.dates as mdates

from config import DIR16_LABELS
from matplotlib.colors import ListedColormap

def get_polar_rose_plot(ax, df, r, theta, intervals, cardinales=DIR16_LABELS, normed=True):
    """Dibuja una rosa de vientos (barras polares apiladas) en el eje proporcionado.

    Comportamiento clave
    - Usa el `ax` que se le pasa; no crea un nuevo subplot internamente. Si el
      `ax` no es polar, intenta reemplazarlo por un eje polar en la misma
      ubicación del layout.
    - `r` y `theta` pueden ser nombres de columnas (str) presentes en `df` o
      arrays/Series del mismo largo que `df`.

    Parámetros
    ----------
    ax : matplotlib.axes.Axes
        Eje donde se dibujará la rosa. Debe pertenecer a la figura creada por
        `plt.subplots` (por ejemplo `fig, (ax_rosa, ax_tabla) = plt.subplots(1,2)`).
    df : pandas.DataFrame
        DataFrame con los datos. Si `r` o `theta` son nombres de columnas, se
        leerán de aquí.
    r : str o array-like
        Columna de `df` con los valores a agrupar (por ejemplo, velocidad)
        o directamente un array/Series con esos valores.
    theta : str o array-like
        Direcciones en radianes: nombre de columna en `df` (p. ej. 'dir_rad')
        o un array/Series de radianes.
    intervals : sequence
        Bordes de los intervalos para agrupar `r` (ej. [0,5,10,15]).
    cardinales : sequence, opcional
        Etiquetas para los sectores angulares. Por defecto usa `CARDINALES`.

    Devuelve
    -------
    matplotlib.axes.Axes
        El eje `ax` (polar) donde se dibujó la rosa. Esto permite encadenar
        llamadas o guardar/ajustar el `fig` que creó el llamador.

    Ejemplo de uso
    --------------
    # En main.py:
    fig, (ax_rosa, ax_tabla) = plt.subplots(1, 2, figsize=(16, 8))
    get_bar_polar(ax_rosa, df, r=columna_valor, theta='dir_rad', intervals=rangos_valor)

    """
    SECTORES = len(cardinales)
    # Asegurarse de que ax sea polar; si no lo es, intentar reemplazarlo
    if getattr(ax, 'name', '') != 'polar':
        fig = ax.figure
        try:
            polar_ax = fig.add_subplot(ax.get_subplotspec(), projection='polar')
            fig.delaxes(ax)
            ax = polar_ax
        except Exception:
            # Fallback: crear un nuevo polar axes (puede alterar layout)
            ax = plt.subplot(1, 2, 1, projection='polar')

    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    # Obtener arrays de valores
    if isinstance(r, str):
        if r not in df.columns:
            raise KeyError(f"Columna '{r}' no encontrada en el DataFrame")
        radio = df[r].values
    else:
        radio = np.asarray(r)

    if isinstance(theta, str):
        if theta not in df.columns:
            raise KeyError(f"Columna '{theta}' no encontrada en el DataFrame")
        theta_vals = df[theta].values
    else:
        theta_vals = np.asarray(theta)

    bins_valor = len(intervals) - 1

    width = 2 * np.pi / SECTORES

    theta_edges = np.linspace(-width / 2, 2 * np.pi - width / 2, SECTORES + 1)
    #print(theta_edges)

    direcciones_mod = np.mod(theta_vals, 2 * np.pi)
    hist, theta_bins, value_bins = np.histogram2d(
        direcciones_mod,
        radio,
        bins=[theta_edges, intervals]
    )

    # If requested, convert counts to percentage of total observations
    if normed:
        total = hist.sum()
        if total > 0:
            hist = hist / total * 100.0

    theta_centers = (theta_edges[:-1] + theta_edges[1:]) / 2

    colores = plt.cm.viridis(np.linspace(0, 1, bins_valor))

    bottom = np.zeros(SECTORES)
    for i in range(bins_valor):
        ax.bar(
            theta_centers,
            hist[:, i],
            width=width,
            bottom=bottom,
            color=colores[i],
            edgecolor='white',
            linewidth=0.5,
            label=f'{intervals[i]}-{intervals[i+1]}'
        )
        bottom += hist[:, i]
        #print(bottom, width, colores[i], theta_centers)

    ax.set_xticks(theta_centers)
    ax.set_xticklabels(cardinales)
    ax.set_title('Rosa', pad=20)
    ax.legend(bbox_to_anchor=(1.1, 1.0), title=f'Rangos de {r}')

    # Format radial tick labels as percentages when normed
    try:
        if normed:
            yticks = ax.get_yticks()
            ax.set_yticklabels([f"{t:.1f}%" for t in yticks])
    except Exception:
        # If tick formatting fails for some backends, ignore silently
        pass

    return ax

def get_table_frequency(fig, ax, tabla, eje_y, eje_x, porcentaje=True):
    """
    Dibuja una tabla de frecuencias entre dos columnas categóricas.

    Parámetros:
    - ax: eje de matplotlib donde se dibuja la tabla.
    - tabla: DataFrame con los datos.
    - eje_y: nombre de la columna para las filas.
    - eje_x: nombre de la columna para las columnas.
    - porcentaje: si es True, muestra porcentajes sobre el total de la tabla.
    """
    # Tabla de frecuencias
    if porcentaje:
        tabla_freq_raw = pd.crosstab(tabla[eje_y], tabla[eje_x], normalize=True) * 100
    else:
        tabla_freq_raw = pd.crosstab(tabla[eje_y], tabla[eje_x])

    # Calcular y adicionar totales sin redondear
    tabla_freq_raw['Total por fila'] = tabla_freq_raw.sum(axis=1)
    totales_columna = tabla_freq_raw.sum(axis=0)
    tabla_freq_raw.loc['Total por columna'] = totales_columna

    # Redondear tabla a 2 decimales
    tabla_freq = tabla_freq_raw.round(2)

    # Formatear celdas con símbolo % (solo si es True)
    if porcentaje:
        tabla_freq = tabla_freq.applymap(lambda x: f"{float(x):.2f}%")

    # Preparar datos para la tabla
    cell_text = tabla_freq.values
    row_labels = tabla_freq.index #.tolist() Solo se necesita .tolist si se están modificando o concatenando los labels antes del ploteo.
    col_labels = tabla_freq.columns #.tolist()

    # Dibujar tabla
    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    table = ax.table(
        cellText=cell_text,
        rowLabels=row_labels,
        colLabels=col_labels,
        cellLoc='center',
        loc='center',
        #bbox=[0, 0, 1, 1]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.2, 1.2)

    sufijo = "(%)" if porcentaje else "(conteos)"
    titulo = f'Tabla de Frecuencias {sufijo}: {eje_y} vs {eje_x}'
    ax.set_title(titulo, pad=10, fontsize=12)

def get_histogram(ax, data, bins, xlabel=None, ylabel='Frequency', title=None, color='C0', porcentaje=False, annotate=False):
    """Dibuja un histograma simple sobre el eje proporcionado.

    Parámetros
    ----------
    ax : matplotlib.axes.Axes
        Eje donde dibujar el histograma.
    data : array-like or pandas.Series
        Valores numéricos a graficar.
    bins : int o sequence, opcional
        Número de bins o secuencia de bordes (por defecto 10).
    xlabel : str, opcional
        Etiqueta para el eje x.
    ylabel : str, opcional
        Etiqueta para el eje y (por defecto 'Frequency').
    title : str, opcional
        Título del gráfico.
    color : str, opcional
        Color de las barras.

    Returns
    -------
    matplotlib.axes.Axes
        El eje donde se dibujó el histograma (útil para encadenar llamadas).

    Ejemplo
    -------
    fig, ax = plt.subplots()
    show_histogram(ax, df['velocidad'], bins=[0,5,10,15], xlabel='Velocidad (m/s)')
    plt.show()
    """

    ax.cla()
    # Remove NaNs from data for counting
    data_arr = pd.Series(data).dropna().values

    if porcentaje:
        # weights so that sum of bar heights equals 100 (percentage)
        if data_arr.size == 0:
            weights = None
        else:
            weights = np.ones_like(data_arr, dtype=float) / data_arr.size * 100.00
        n, bins_out, patches = ax.hist(data_arr, bins=bins, color=color, edgecolor='black', weights=weights)
        # adjust ylabel if not explicitly provided
        if ylabel == 'Frequency':
            ylabel = 'Frequency (%)'
    else:
        n, bins_out, patches = ax.hist(data_arr, bins=bins, color=color, edgecolor='black') #Este método bin la data en x y cuenta el número de ocurrencias en y.
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.grid(True, linestyle='--', alpha=0.4)
    # Format y-ticks as percentages when porcentaje=True
    if porcentaje:
        try:
            yt = ax.get_yticks()
            ax.set_yticklabels([f"{y:.1f}%" for y in yt])
        except Exception:
            pass
    # Annotate bars with values above each bin if requested
    if annotate:
        try:
            for patch in patches:
                h = patch.get_height()
                if h <= 0:
                    continue
                x = patch.get_x() + patch.get_width() / 2
                if porcentaje:
                    label = f"{h:.2f}%"
                else:
                    # show integer if close to int, otherwise one decimal
                    if abs(h - round(h)) < 0.01:
                        label = f"{int(round(h))}"
                    else:
                        label = f"{h:.1f}"
                ax.text(x, h, label, ha='center', va='bottom', fontsize=8)
        except Exception:
            # don't fail drawing if annotation causes issues
            pass
    return ax

def get_time_series(ax, df, x_col, y_cols, xlabel, ylabel, title, labels=None):
    """Simple time-series plotter.

    Requisitos mínimos: debe recibir `ax`, `df`, `x_col`, `y_cols`, `xlabel`,
    `ylabel` y `title` (todos obligatorios según lo solicitado).

    - x_col: nombre de la columna datetime en `df`.
    - y_cols: nombre de columna (str) o lista de columnas a graficar.
    - labels: dict opcional que mapea nombres de columnas a etiquetas personalizadas
              (ej: {'hs_m': 'Altura Significativa', 'tp_s': 'Periodo Pico'})
    """

    # Validate required parameters
    if x_col is None or y_cols is None or xlabel is None or ylabel is None or title is None:
        raise ValueError("x_col, y_cols, xlabel, ylabel y title son parámetros obligatorios")

    if x_col not in df.columns:
        raise KeyError(f"Columna de tiempo '{x_col}' no encontrada en el DataFrame")

    # Prepare dataframe and ensure datetime
    df_local = df.copy()
    df_local[x_col] = pd.to_datetime(df_local[x_col], errors='coerce', dayfirst=True, infer_datetime_format=True)

    if isinstance(y_cols, str):
        y_cols = [y_cols]

    for y in y_cols:
        if y not in df_local.columns:
            raise KeyError(f"Columna '{y}' no encontrada en el DataFrame")

    # Keep only rows where time is valid; allow NaNs in series (line will skip them)
    plot_df = df_local[[x_col] + y_cols].dropna(subset=[x_col])
    plot_df = plot_df.sort_values(by=x_col).reset_index(drop=True)

    # Interpolate missing values in y columns to fill gaps and show continuous line
    #for y in y_cols:
    #    plot_df[y] = plot_df[y].interpolate(method='linear', limit_direction='both')

    #ax.cla()

    # Styling similar to the example: simple black line, thin width, subtle grid
    for y in y_cols:
        # Use custom label if provided, otherwise use column name
        display_label = labels.get(y, y) if labels else y
        ax.plot(plot_df[x_col], plot_df[y], color='k', linewidth=0.9, solid_capstyle='round', label=display_label)

    # Axis labels and title
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    # Smart y-limits: include a small margin; don't force negative lower bound
    try:
        y_vals = plot_df[y_cols].values.flatten()
        y_vals = y_vals[~pd.isna(y_vals)]
        if y_vals.size > 0:
            y_min, y_max = float(y_vals.min()*0.75), float(y_vals.max()*1.25)
            yrange = max(1e-6, y_max - y_min)
            pad = yrange * 0.08
            lower = max(0.0, y_min - pad)
            upper = y_max + pad
            ax.set_ylim(lower, upper)
    except Exception:
        pass

    # Grid styling: horizontal lighter lines, vertical solid lines
    ax.grid(which='major', axis='y', linestyle='-', color='#dddddd', linewidth=0.5)
    ax.grid(which='major', axis='x', linestyle='-', color='#cccccc', linewidth=0.5)

    # Remove border (spines)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Date formatting on x-axis: weekly ticks (like the example)
    try:
        locator = mdates.WeekdayLocator(byweekday=mdates.MO)
        formatter = mdates.DateFormatter('%Y-%m-%d')
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.xaxis.set_minor_locator(mdates.DayLocator())
        for label in ax.get_xticklabels():
            label.set_rotation(0)
            label.set_ha('center')
            label.set_fontsize(8)
        # Hide tick marks but keep labels
        ax.tick_params(axis='x', which='both', length=0)
        ax.tick_params(axis='y', which='both', length=0)
    except Exception:
        try:
            fig = ax.get_figure()
            fig.autofmt_xdate()
        except Exception:
            pass

    # Legend as a small boxed label (rounded)
    leg = ax.legend(frameon=True, loc='upper left')
    if leg is not None:
        frame = leg.get_frame()
        frame.set_edgecolor('#444444')
        frame.set_linewidth(0.4)
        frame.set_alpha(0.9)

    # Tidy ticks
    ax.tick_params(axis='both', which='major', labelsize=8)

    return ax

def get_polar_from_windrose(fig, df, r, theta, bins, units='m', display_title=None):
    ax2 = WindroseAxes.from_ax(fig=fig)
    #ax2.set_xticklabels(('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'))
    ax2.set_xticklabels(('E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE'))

    # Create custom colormap matching the image: cyan, yellow, dark red
    #colors = ['#00BFFF', '#FFD700', '#8B0000']  # cyan, yellow, dark red
    #cmap = ListedColormap(colors)

    ax2.bar(df[theta], df[r], normed=True, bins=bins,
            opening=0.8, nsector=16, edgecolor='white',
            )#cmap=cmap)

    # Format radial grid labels as percentages based on the actual frequency data
    try:
        ymin, ymax = ax2.get_ylim()
        ymax_rounded = np.ceil(ymax / 10) * 10
        new_ticks = np.arange(0, ymax_rounded + 10, 10)
        ax2.set_yticks(new_ticks)
        yticks = ax2.get_yticks()
        # Format as percentages directly (yticks are already proportional values)
        yticklabels = [f'{int(y)}%' for y in yticks if y >= 0]
        ax2.set_yticklabels(yticklabels, fontsize=9)
    except Exception:
        pass

    # Use custom title label if provided, otherwise use column name
    display_title = display_title if display_title else r
    ax2.set_title(display_title, fontsize=12, weight='bold')
    legend = ax2.legend(title=f'{display_title} [{units}]', loc='lower right', framealpha=0.95)
    if legend is not None:
        legend.get_title().set_fontsize(10)

def get_bars(ax, df, eje_x, porcentaje=True, color='C0', xlabel='Categoría', ylabel='Frecuencia (%)'):
    """
    Dibuja un gráfico de barras categórico basado en los totales de una sola columna.

    Parámetros
    ----------
    ax : matplotlib.axes.Axes
        Eje donde se dibuja el gráfico.
    df : pandas.DataFrame
        DataFrame con los datos originales.
    eje_x : str
        Nombre de la columna categórica para el eje X.
    porcentaje : bool, opcional
        Si es True, muestra porcentajes sobre el total.
    color : str, opcional
        Color de las barras.

    Retorna
    -------
    matplotlib.axes.Axes
        El eje modificado.
    """
    ax.clear()

    # Ocurrencias por categoría
    conteos = df[eje_x].value_counts(sort=False)

    # Normalización
    if porcentaje:
        total = conteos.sum()
        conteos = conteos / total * 100
        ax.set_ylim(0, 100)

    # Redondear
    conteos = conteos.round(2)

    # Gráfico
    etiquetas = conteos.index.tolist()
    valores = conteos.values
    posiciones = range(len(etiquetas))

    barras = ax.bar(posiciones, valores, color='#AAA5A7', edgecolor='black', linewidth=0.7)

    # Etiquetas encima de cada barra (matching image style)
    for barra, valor in zip(barras, valores):
        texto = f"{valor:.2f}%" if porcentaje else f"{valor:.0f}"
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + 1,
            texto,
            ha='center',
            va='bottom',
            fontsize=9,
            fontweight='bold'
        )

    ax.set_xticks(posiciones)
    ax.set_xticklabels(etiquetas, rotation=0, ha='center', fontsize=9)

    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)

    ax.set_ylim(0, 100)
    ax.grid(True, axis='y', linestyle='-', color='#e0e0e0', linewidth=0.8, alpha=0.5)
    ax.set_axisbelow(True)



    return ax

def get_table_statistics_summary(fig, ax, df, colnames):
    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    summary = df[colnames].describe().round(2)
    ax.table(cellText=summary.values, rowLabels = summary.index, colLabels=summary.columns, loc='center')

    return ax

def get_occurrence_table(fig, ax, df: pd.DataFrame,
        hs_col: str = "hs_m",
        tp_col: str = "tp_s",
        dp_col: str = "dirtp_dgs",
        hs_bin: str = "hs_bins",
        tp_bin: str = "tp_bins",
        dir_bin: str = "dir_bins16",
        precision=2,
        export_xlsx = False,
        estacion = "estacion"):

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    df = df.copy()
    grp = df.groupby([dir_bin, hs_bin, tp_bin], observed=True).agg(
        Dp_mean=(dp_col, "mean"),
        Hs_mean=(hs_col, "mean"),
        Tp_mean=(tp_col, "mean"),
        conteo=(hs_col, "size")
        #ocurrencia = (hs_col, lambda x: (x.count() / len(df)) * 100 if len(df) > 0 else 0),
        #ocurrencia_anual = (hs_col, lambda x: (x.count() / len(df)) * 365 if len(df) > 0 else 0)
    ).reset_index()

    total = grp["conteo"].sum()
    grp["ocurrencia (%)"] = 100 * grp["conteo"] / total if total else 0
    grp["ocurrencia (dias/año)"] = 365 * grp["conteo"] / total if total else 0
    grp.round(precision)
    grp.sort_values("ocurrencia (%)", ascending= False).reset_index(drop=True)

    ax.table(cellText=grp.values, colLabels=grp.columns, loc='center')

    if export_xlsx:
        try:
            grp.to_excel(f"out/tabla_ocurrencia_{estacion}_hs_tp_dir.xlsx", index=False)
        except Exception as e:
            print(f"Error exporting occurrence table to Excel: {e}")

    return ax

def get_bar_x_estacion(ax, categories, counts):

    bar_container = ax.bar(categories, counts)
    ax.bar_label(bar_container, fmt='%.2f%%')

