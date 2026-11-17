"""Clean the Sample Superstore CSV and export a standardized dataset."""

from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "SampleSuperstore.csv"
OUT_DIR = ROOT / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.astype(str).str.strip().str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return df


def clean_data(df: pd.DataFrame):
    df = normalize_columns(df)
    rows_before = len(df)
    duplicate_rows = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype("string").str.strip()

    for col in ["order_date", "ship_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    for col in ["sales", "quantity", "discount", "profit", "postal_code"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    missing_before = {k: int(v) for k, v in df.isna().sum().items()}

    required = [c for c in ["order_id", "order_date", "sales", "profit"] if c in df.columns]
    if required:
        df = df.dropna(subset=required).copy()

    if "postal_code" in df.columns:
        df["postal_code"] = df["postal_code"].astype("Int64")

    if "order_date" in df.columns:
        df["order_year"] = df["order_date"].dt.year.astype("Int64")
        df["order_month"] = df["order_date"].dt.month.astype("Int64")
        df["month_name"] = df["order_date"].dt.month_name()
        df["order_quarter"] = "Q" + df["order_date"].dt.quarter.astype("Int64").astype(str)

    if {"order_date", "ship_date"}.issubset(df.columns):
        df["days_to_ship"] = (df["ship_date"] - df["order_date"]).dt.days

    if {"sales", "profit"}.issubset(df.columns):
        df["profit_margin_pct"] = np.where(
            df["sales"].ne(0), df["profit"] / df["sales"] * 100, np.nan
        )

    report = {
        "rows_before_cleaning": int(rows_before),
        "rows_after_cleaning": int(len(df)),
        "columns_after_cleaning": int(len(df.columns)),
        "duplicate_rows_removed": duplicate_rows,
        "missing_values_before_cleaning": missing_before,
        "missing_values_after_cleaning": {k: int(v) for k, v in df.isna().sum().items()},
        "data_types": {k: str(v) for k, v in df.dtypes.items()},
    }
    return df, report


def main():
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_FILE}\n"
            "Place SampleSuperstore.csv inside data/raw/."
        )

    raw = pd.read_csv(RAW_FILE, encoding="utf-8-sig")
    cleaned, report = clean_data(raw)

    csv_path = OUT_DIR / "sales_cleaned.csv"
    json_path = OUT_DIR / "data_quality_report.json"
    cleaned.to_csv(csv_path, index=False, encoding="utf-8-sig")
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Rows before: {report['rows_before_cleaning']:,}")
    print(f"Rows after: {report['rows_after_cleaning']:,}")
    print(f"Duplicates removed: {report['duplicate_rows_removed']:,}")
    print(f"Saved: {csv_path}")
    print(f"Saved: {json_path}")


if __name__ == "__main__":
    main()
