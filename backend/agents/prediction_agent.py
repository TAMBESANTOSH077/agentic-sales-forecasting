from typing import Dict, Tuple

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def build_features(
    daily: pd.DataFrame
) -> pd.DataFrame:

    data = daily.copy()

    data["day_index"] = np.arange(len(data))

    data["day_of_week"] = (
        data["date"].dt.dayofweek
    )

    data["month"] = (
        data["date"].dt.month
    )

    data["day"] = (
        data["date"].dt.day
    )

    return data


def predict_sales(
    df: pd.DataFrame,
    forecast_days: int = 30
) -> Tuple[Dict, Dict]:

    # -------------------------
    # DAILY SALES
    # -------------------------

    daily = (
        df.groupby("date", as_index=False)["revenue"]
        .sum()
        .sort_values("date")
    )

    if len(daily) < 14:

        raise ValueError(
            "At least 14 days of historical "
            "data are required."
        )

    # -------------------------
    # FEATURES
    # -------------------------

    features = build_features(daily)

    feature_columns = [
        "day_index",
        "day_of_week",
        "month",
        "day"
    ]

    X = features[feature_columns]
    y = features["revenue"]

    # -------------------------
    # TRAIN / VALIDATION
    # -------------------------

    split = max(
        7,
        int(len(features) * 0.8)
    )

    model = RandomForestRegressor(
        n_estimators=250,
        random_state=42,
        min_samples_leaf=2
    )

    model.fit(
        X.iloc[:split],
        y.iloc[:split]
    )

    validation_predictions = model.predict(
        X.iloc[split:]
    )

    metrics = {
        "mae": round(
            float(
                mean_absolute_error(
                    y.iloc[split:],
                    validation_predictions
                )
            ),
            2
        ),

        "rmse": round(
            float(
                np.sqrt(
                    mean_squared_error(
                        y.iloc[split:],
                        validation_predictions
                    )
                )
            ),
            2
        ),

        "r2": round(
            float(
                r2_score(
                    y.iloc[split:],
                    validation_predictions
                )
            ),
            4
        )
    }

    # -------------------------
    # FINAL MODEL
    # -------------------------

    final_model = RandomForestRegressor(
        n_estimators=250,
        random_state=42,
        min_samples_leaf=2
    )

    final_model.fit(X, y)

    # -------------------------
    # FUTURE DATES
    # -------------------------

    last_date = daily["date"].max()

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=forecast_days
    )

    future = pd.DataFrame({
        "date": future_dates
    })

    future["day_index"] = np.arange(
        len(daily),
        len(daily) + forecast_days
    )

    future["day_of_week"] = (
        future["date"].dt.dayofweek
    )

    future["month"] = (
        future["date"].dt.month
    )

    future["day"] = (
        future["date"].dt.day
    )

    # -------------------------
    # PREDICTION
    # -------------------------

    future["predicted_revenue"] = (
        final_model.predict(
            future[feature_columns]
        )
    )

    future["predicted_revenue"] = (
        future["predicted_revenue"]
        .clip(lower=0)
    )

    # -------------------------
    # RESULT
    # -------------------------

    forecast = {

        "total_predicted_revenue": round(
            float(
                future["predicted_revenue"].sum()
            ),
            2
        ),

        "daily_average": round(
            float(
                future["predicted_revenue"].mean()
            ),
            2
        ),

        "start_date": (
            future_dates.min()
            .strftime("%Y-%m-%d")
        ),

        "end_date": (
            future_dates.max()
            .strftime("%Y-%m-%d")
        ),

        "daily_forecast": [

            {
                "date": row.date.strftime(
                    "%Y-%m-%d"
                ),

                "revenue": round(
                    float(row.predicted_revenue),
                    2
                )
            }

            for row in future.itertuples()
        ]
    }

    return forecast, metrics