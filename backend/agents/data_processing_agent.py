import pandas as pd


def process_data(df: pd.DataFrame) -> pd.DataFrame:

    data = df.copy()

    # Convert date
    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce"
    )

    # Convert numeric columns
    for column in [
        "quantity",
        "price",
        "revenue"
    ]:

        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    # Calculate missing revenue
    missing_revenue = data["revenue"].isna()

    data.loc[missing_revenue, "revenue"] = (
        data.loc[missing_revenue, "quantity"]
        * data.loc[missing_revenue, "price"]
    )

    # Remove invalid rows
    data = data.dropna(
        subset=[
            "date",
            "quantity",
            "price",
            "revenue"
        ]
    )

    # Remove duplicates
    data = data.drop_duplicates()

    # Remove negative values
    data["quantity"] = data["quantity"].clip(lower=0)
    data["price"] = data["price"].clip(lower=0)
    data["revenue"] = data["revenue"].clip(lower=0)

    # Sort
    data = data.sort_values("date")

    return data.reset_index(drop=True)