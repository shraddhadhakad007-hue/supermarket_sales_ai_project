from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

OUT = Path(__file__).resolve().parent / "supermarket_sales.csv"
N = 1200

branches = {
    "A": ("Bhopal", 0.34),
    "B": ("Indore", 0.36),
    "C": ("Jabalpur", 0.30),
}
product_lines = [
    "Health and beauty",
    "Electronic accessories",
    "Home and lifestyle",
    "Sports and travel",
    "Food and beverages",
    "Fashion accessories",
]
payment_methods = ["Ewallet", "Cash", "Credit card"]
customer_types = ["Member", "Normal"]
genders = ["Female", "Male"]
start = date(2026, 1, 1)

rows = []
for i in range(1, N + 1):
    b = random.choices(list(branches), weights=[v[1] for v in branches.values()], k=1)[0]
    city = branches[b][0]
    d = start + timedelta(days=random.randint(0, 242))
    product = random.choice(product_lines)
    customer = random.choice(customer_types)
    gender = random.choice(genders)
    payment = random.choices(payment_methods, weights=[0.38, 0.31, 0.31], k=1)[0]

    base_price = {
        "Health and beauty": 48,
        "Electronic accessories": 55,
        "Home and lifestyle": 58,
        "Sports and travel": 63,
        "Food and beverages": 39,
        "Fashion accessories": 52,
    }[product]
    unit_price = max(10, np.random.normal(base_price, 14))
    quantity = int(np.clip(np.random.poisson(4) + 1, 1, 10))
    cogs = unit_price * quantity * np.random.uniform(0.52, 0.78)
    tax = unit_price * quantity * 0.05
    gross_income = (unit_price * quantity) - cogs
    total = unit_price * quantity + tax
    rating = float(np.clip(np.random.normal(7.1, 1.15), 4.0, 10.0))

    rows.append(
        {
            "Invoice_ID": f"INV-{i:05d}",
            "Date": d.isoformat(),
            "Branch": b,
            "City": city,
            "Customer_Type": customer,
            "Gender": gender,
            "Product_Line": product,
            "Unit_Price": round(unit_price, 2),
            "Quantity": quantity,
            "Tax_5pct": round(tax, 2),
            "Total": round(total, 2),
            "COGS": round(cogs, 2),
            "Gross_Margin_pct": round((gross_income / total) * 100, 2),
            "Gross_Income": round(gross_income, 2),
            "Payment": payment,
            "Rating": round(rating, 1),
        }
    )

df = pd.DataFrame(rows)
# Add a few deliberately imperfect values so the cleaning pipeline has real work to do.
dup = df.iloc[10].copy()
dup["Invoice_ID"] = "INV-DUP-001"
df = pd.concat([df, pd.DataFrame([dup])], ignore_index=True)
df.loc[25, "Rating"] = np.nan
df.loc[55, "Quantity"] = np.nan

# Inject two clear high-value anomalies for the AI section.
df.loc[100, "Unit_Price"] = 180.0
df.loc[100, "Quantity"] = 10
df.loc[101, "Unit_Price"] = 175.0
df.loc[101, "Quantity"] = 10

df.to_csv(OUT, index=False)
print(f"Wrote {len(df)} rows to {OUT}")
