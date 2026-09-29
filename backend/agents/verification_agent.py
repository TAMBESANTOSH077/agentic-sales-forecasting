import pandas as pd


def verify_forecast(
    df: pd.DataFrame,
    forecast: dict
) -> dict:

    historical_daily = (
        df.groupby("date")["revenue"]
        .sum()
    )

    historical_average = float(
        historical_daily.tail(30).mean()
    )

    predicted_average = float(
        forecast["daily_average"]
    )

    if historical_average == 0:

        ratio = 0

    else:

        ratio = (
            predicted_average
            / historical_average
        )

    # Sanity check
    passed = (
        0.4 <= ratio <= 2.5
    )

    if passed:

        message = (
            "Forecast passed sanity validation."
        )

    else:

        message = (
            "Forecast is outside the expected "
            "range. Review the model and data."
        )

    return {

        "passed": passed,

        "historical_daily_average": round(
            historical_average,
            2
        ),

        "predicted_daily_average": round(
            predicted_average,
            2
        ),

        "prediction_vs_history_ratio": round(
            ratio,
            3
        ),

        "message": message
    }