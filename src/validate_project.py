"""Basic checks for generated project outputs; run after cleaning and EDA."""

from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "processed" / "sales_cleaned.csv"
REPORT = ROOT / "data" / "processed" / "data_quality_report.json"
EDA = ROOT / "reports" / "eda_summary.txt"


def main():
    missing = [p for p in [CSV, REPORT, EDA] if not p.exists()]
    if missing:
        print("Some outputs are not present yet:")
        for path in missing:
            print(f" - {path.relative_to(ROOT)}")
        print("Run the cleaning script and EDA script first.")
        return

    df = pd.read_csv(CSV)
    quality = json.loads(REPORT.read_text(encoding="utf-8"))

    assert len(df) > 0, "Cleaned dataset is empty."
    assert "sales" in df.columns and "profit" in df.columns
    assert df["sales"].notna().all(), "Sales contains missing values."
    assert df["profit"].notna().all(), "Profit contains missing values."

    print("Basic validation passed.")
    print(f"Cleaned rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print(f"Duplicates removed: {quality['duplicate_rows_removed']:,}")
    print(f"EDA summary exists: {EDA.exists()}")


if __name__ == "__main__":
    main()
