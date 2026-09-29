from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "date",
    "product",
    "category",
    "region",
    "quantity",
    "price",
    "revenue"
}


def collect_data(csv_path: str) -> pd.DataFrame:

    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Sales file not found: {csv_path}"
        )

    df = pd.read_csv(path)

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: "
            f"{sorted(missing_columns)}"
        )

    if df.empty:
        raise ValueError("CSV file contains no records.")

    return df