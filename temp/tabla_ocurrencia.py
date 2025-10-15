
import argparse
import pandas as pd
import numpy as np
from pathlib import Path

DIR16_LABELS = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSO", "SO", "OSO", "O", "ONO", "NO", "NNO"
]

def deg_to_dir16(deg_series: pd.Series) -> pd.Series:
    idx = (((deg_series + 11.25) % 360) // 22.5).astype("Int64")
    out = idx.map(lambda i: DIR16_LABELS[int(i)] if pd.notna(i) else pd.NA)
    return pd.Categorical(out, categories=DIR16_LABELS, ordered=True)

def make_bin_edges(series: pd.Series, step: float, start=None, stop=None):
    if series.dropna().empty:
        raise ValueError("La serie está vacía; no se pueden generar bins.")
    data_min = series.min()
    data_max = series.max()
    if start is None:
        start = np.floor(data_min / step) * step
    if stop is None:
        stop = np.ceil(data_max / step) * step
    edges = np.arange(start, stop + step, step, dtype=float)
    return edges

def cut_series(series: pd.Series, edges, precision=2, closed="left"):
    cats = pd.cut(series, edges, right=False if closed=="left" else True, include_lowest=True)
    labels = []
    for intv in cats.cat.categories:
        a = round(float(intv.left), precision)
        b = round(float(intv.right), precision)
        lab = f"{a}–{b}"
        labels.append(lab)
    cats = cats.cat.rename_categories(labels)
    return cats

def build_occurrence_table(df: pd.DataFrame,
        hs_col: str = "Hs",
        tp_col: str = "Tp",
        dp_col: str = "Dp",
        hs_step: float = 0.5,
        tp_step: float = 3.0,
        hs_start=None,
        hs_stop=None,
        tp_start=2,
        tp_stop=None,
        precision=2):
    hs_edges = make_bin_edges(df[hs_col], hs_step, hs_start, hs_stop)
    hs_bins = cut_series(df[hs_col], hs_edges, precision=precision, closed="left")
    tp_edges = make_bin_edges(df[tp_col], tp_step, tp_start, tp_stop)
    tp_bins = cut_series(df[tp_col], tp_edges, precision=precision, closed="left")
    dir16 = deg_to_dir16(df[dp_col])

    temp = pd.DataFrame({
        "Hs_bin": hs_bins,
        "Tp_bin": tp_bins,
        "Dir16": dir16,
        "Hs": df[hs_col],
        "Tp": df[tp_col],
        "Dp": df[dp_col]
    })

    grp = temp.groupby(["Hs_bin", "Tp_bin", "Dir16"], observed=True).agg(
        conteo=("Hs", "size"),
        Hs_mean=("Hs", "mean"),
        Tp_mean=("Tp", "mean"),
        Dp_mean=("Dp", "mean")
    ).reset_index()

    total = grp["conteo"].sum()
    grp["porcentaje"] = 100 * grp["conteo"] / total if total else 0
    return grp.sort_values(["Hs_bin", "Tp_bin", "Dir16"]).reset_index(drop=True)

def pivot_hs_dir(grp: pd.DataFrame) -> pd.DataFrame:
    t = grp.groupby(["Hs_bin", "Dir16"], observed=True)["conteo"].sum().unstack(fill_value=0)
    t["Total"] = t.sum(axis=1)
    return t

def pivot_tp_dir(grp: pd.DataFrame) -> pd.DataFrame:
    t = grp.groupby(["Tp_bin", "Dir16"], observed=True)["conteo"].sum().unstack(fill_value=0)
    t["Total"] = t.sum(axis=1)
    return t

def read_input(path: Path,
        sep=None,
        decimal=".",
        fecha_col="Fecha",
        hora_col="HORA",
        hs_col="Hs",
        tp_col="Tp",
        dp_col="Dp",
        no_datetime=False):
    df = pd.read_csv(path, sep=sep, decimal=decimal, engine="python")
    if not no_datetime and fecha_col in df.columns and hora_col in df.columns:
        df["_datetime"] = pd.to_datetime(df[fecha_col].astype(str).str.strip() + " " + df[hora_col].astype(str).str.strip(), errors="coerce", dayfirst=True, infer_datetime_format=True)
    for c in [hs_col, tp_col, dp_col]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        else:
            raise KeyError(f"Columna '{c}' no encontrada en archivo.")
    return df

def write_csv(df: pd.DataFrame, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path

def parse_args():
    p = argparse.ArgumentParser(description="Tabla de ocurrencia Hs x Tp x Dir16 para datos de oleaje.")
    p.add_argument("--input", required=True, help="Ruta al archivo CSV de entrada.")
    p.add_argument("--output", required=True, help="Ruta al CSV de ocurrencias (principal).")
    p.add_argument("--hs-step", type=float, default=0.5)
    p.add_argument("--tp-step", type=float, default=2.0)
    p.add_argument("--hs-start", type=float, default=None)
    p.add_argument("--hs-stop", type=float, default=None)
    p.add_argument("--tp-start", type=float, default=None)
    p.add_argument("--tp-stop", type=float, default=None)
    p.add_argument("--sep", default=None)
    p.add_argument("--decimal", default=".")
    p.add_argument("--fecha-col", default="Fecha")
    p.add_argument("--hora-col", default="HORA")
    p.add_argument("--hs-col", default="Hs")
    p.add_argument("--tp-col", default="Tp")
    p.add_argument("--dp-col", default="Dp")
    p.add_argument("--no-datetime", action="store_true")
    p.add_argument("--export-hs-dir", default=None)
    p.add_argument("--export-tp-dir", default=None)
    return p.parse_args()

def main():
    args = parse_args()
    in_path = Path(args.input)
    out_path = Path(args.output)

    df = read_input(in_path,
                    sep=args.sep,
                    decimal=args.decimal,
                    fecha_col=args.fecha_col,
                    hora_col=args.hora_col,
                    hs_col=args.hs_col,
                    tp_col=args.tp_col,
                    dp_col=args.dp_col,
                    no_datetime=args.no_datetime)

    occ = build_occurrence_table(df,
        hs_col=args.hs_col,
        tp_col=args.tp_col,
        dp_col=args.dp_col,
        hs_step=args.hs_step,
        tp_step=args.tp_step,
        hs_start=args.hs_start,
        hs_stop=args.hs_stop,
        tp_start=args.tp_start,
        tp_stop=args.tp_stop)

    write_csv(occ, out_path)
    print(f"Tabla principal guardada en: {out_path}")

    if args.export_hs_dir:
        hs_dir = pivot_hs_dir(occ)
        write_csv(hs_dir.reset_index(), Path(args.export_hs_dir))
    if args.export_tp_dir:
        tp_dir = pivot_tp_dir(occ)
        write_csv(tp_dir.reset_index(), Path(args.export_tp_dir))

if __name__ == "__main__":
    main()
