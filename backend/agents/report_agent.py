def generate_report(
    df,
    forecast: dict,
    verification: dict
) -> list[str]:

    total_historical_revenue = float(
        df["revenue"].sum()
    )

    product_revenue = (
        df.groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    top_product = (
        product_revenue.index[0]
        if not product_revenue.empty
        else "N/A"
    )

    predicted_revenue = float(
        forecast["total_predicted_revenue"]
    )

    historical_average = float(
        verification[
            "historical_daily_average"
        ]
    )

    predicted_average = float(
        verification[
            "predicted_daily_average"
        ]
    )

    if historical_average:

        growth = (
            (
                predicted_average
                - historical_average
            )
            / historical_average
        ) * 100

    else:

        growth = 0

    return [

        (
            f"Historical revenue: "
            f"₹{total_historical_revenue:,.0f}"
        ),

        (
            f"Top revenue-generating product: "
            f"{top_product}"
        ),

        (
            f"Forecast revenue from "
            f"{forecast['start_date']} to "
            f"{forecast['end_date']}: "
            f"₹{predicted_revenue:,.0f}"
        ),

        (
            f"Predicted daily revenue is "
            f"{growth:+.1f}% compared with "
            f"the recent historical average."
        ),

        (
            "Verification status: PASSED."
            if verification["passed"]
            else
            "Verification status: REVIEW REQUIRED."
        )
    ]