from __future__ import annotations

from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = [
    "Invoice_ID", "Date", "Branch", "City", "Customer_Type", "Gender",
    "Product_Line", "Unit_Price", "Quantity", "Tax_5pct", "Total", "COGS",
    "Gross_Margin_pct", "Gross_Income", "Payment", "Rating",
]


def load_and_clean(path: str | Path) -> tuple[pd.DataFrame, dict]:
    df = pd.read_csv(path)
    original_rows = len(df)
    missing_required = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_required:
        raise ValueError(f"Missing required columns: {missing_required}")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    numeric = [
        "Unit_Price", "Quantity", "Tax_5pct", "Total", "COGS",
        "Gross_Margin_pct", "Gross_Income", "Rating",
    ]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    missing_before = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated(subset=["Invoice_ID"]).sum())
    df = df.drop_duplicates(subset=["Invoice_ID"], keep="first").copy()

    for col in ["Quantity", "Rating"]:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())

    for col in ["Unit_Price", "Tax_5pct", "Total", "COGS", "Gross_Margin_pct", "Gross_Income"]:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())

    for col in ["Branch", "City", "Customer_Type", "Gender", "Product_Line", "Payment"]:
        if df[col].isna().any():
            df[col] = df[col].fillna("Unknown")

    df["Quantity"] = df["Quantity"].clip(lower=1).round().astype(int)
    df["Rating"] = df["Rating"].clip(0, 10).round(1)
    df["Revenue_Before_Tax"] = (df["Unit_Price"] * df["Quantity"]).round(2)
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Day_Name"] = df["Date"].dt.day_name()
    df["Profit_Margin_pct"] = (df["Gross_Income"] / df["Total"].replace(0, pd.NA) * 100).fillna(0).round(2)

    info = {
        "original_rows": original_rows,
        "final_rows": len(df),
        "duplicate_rows_removed": duplicate_rows,
        "missing_values_repaired": missing_before,
        "columns": list(df.columns),
    }
    return df, info
