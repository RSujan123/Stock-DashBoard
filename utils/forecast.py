from prophet import Prophet
import pandas as pd

def make_forecast(data, days=30):
    # Prepare data
    df = data[["Date", "Close"]].copy()
    df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)  # Remove timezone
    df = df.rename(columns={"Date": "ds", "Close": "y"})

    # Train Prophet
    model = Prophet(daily_seasonality=True)
    model.fit(df)

    # Forecast
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    return forecast, model
