import json
from datetime import datetime

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from app.config import (
    TRAIN_END,
    TRAIN_START,
    WALMART_CACHE,
    WALMART_CSV,
)

FEATURE_COLUMNS = [
    "mesec",
    "Holiday_Flag",
    "Temperature",
    "Fuel_Price",
    "CPI",
    "Unemployment",
    "srednja_zarada",
]
TARGET_COLUMN = "Weekly_Sales"


def _parse_date(value: str) -> datetime:
    return datetime.strptime(value.strip(), "%d-%m-%Y")


def _load_dataset() -> pd.DataFrame:
    frame = pd.read_csv(WALMART_CSV)
    frame["Date"] = pd.to_datetime(frame["Date"], format="%d-%m-%Y")
    frame["mesec"] = frame["Date"].dt.month
    return frame


def _add_store_average_sales(frame: pd.DataFrame, train_mask: pd.Series) -> pd.DataFrame:
    store_means = (
        frame.loc[train_mask]
        .groupby("Store")["Weekly_Sales"]
        .mean()
        .rename("srednja_zarada")
    )
    return frame.merge(store_means, on="Store", how="left")


def _build_train_mask(frame: pd.DataFrame) -> pd.Series:
    start = _parse_date(TRAIN_START)
    end = _parse_date(TRAIN_END)
    return (frame["Date"] >= start) & (frame["Date"] <= end)


def _correlation_table(frame: pd.DataFrame) -> list[dict]:
    columns = FEATURE_COLUMNS + [TARGET_COLUMN]
    correlation = frame[columns].corr().round(4)
    rows: list[dict] = []
    for row_name in correlation.index:
        row = {"parameter": row_name}
        for column_name in correlation.columns:
            row[column_name] = float(correlation.loc[row_name, column_name])
        rows.append(row)
    return rows


def _sample_predictions(
    test_frame: pd.DataFrame,
    predictions,
    *,
    limit: int = 10,
) -> list[dict]:
    sample = test_frame.head(limit).copy()
    sample["predicted_weekly_sales"] = predictions[:limit]
    rows: list[dict] = []
    for _, row in sample.iterrows():
        rows.append(
            {
                "store": int(row["Store"]),
                "date": row["Date"].strftime("%d-%m-%Y"),
                "actual_weekly_sales": round(float(row[TARGET_COLUMN]), 2),
                "predicted_weekly_sales": round(float(row["predicted_weekly_sales"]), 2),
            }
        )
    return rows


def run_walmart_regression(*, refresh: bool = False) -> dict:
    if not refresh and WALMART_CACHE.exists():
        return json.loads(WALMART_CACHE.read_text(encoding="utf-8"))

    frame = _load_dataset()
    train_mask = _build_train_mask(frame)
    frame = _add_store_average_sales(frame, train_mask)

    train_frame = frame.loc[train_mask]
    test_frame = frame.loc[~train_mask]

    model = LinearRegression()
    model.fit(train_frame[FEATURE_COLUMNS], train_frame[TARGET_COLUMN])
    predictions = model.predict(test_frame[FEATURE_COLUMNS])
    mse = float(mean_squared_error(test_frame[TARGET_COLUMN], predictions))

    coefficients = [
        {"feature": feature, "coefficient": round(float(value), 6)}
        for feature, value in zip(FEATURE_COLUMNS, model.coef_, strict=True)
    ]

    payload = {
        "source_file": WALMART_CSV.name,
        "train_period": {"from": TRAIN_START, "to": TRAIN_END},
        "train_rows": int(len(train_frame)),
        "test_rows": int(len(test_frame)),
        "features": FEATURE_COLUMNS,
        "target": TARGET_COLUMN,
        "mse_test": round(mse, 2),
        "intercept": round(float(model.intercept_), 6),
        "coefficients": coefficients,
        "correlation_table": _correlation_table(frame),
        "sample_predictions": _sample_predictions(test_frame, predictions),
    }

    WALMART_CACHE.parent.mkdir(parents=True, exist_ok=True)
    WALMART_CACHE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload
