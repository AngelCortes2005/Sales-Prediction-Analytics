import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import argparse
import numpy as np

# Step 1: Read transaction data from a default parquet file
def read_transaction_file() -> pd.DataFrame:
    parquet_file = "transactions.parquet"  # Default file name
    df = pd.read_parquet(parquet_file)
    return df

# Step 2: Aggregate and prepare time series data
def prepare_time_series(df: pd.DataFrame, channel_name: str) -> pd.Series:
    df["date"] = pd.to_datetime(df["date"])
    df_filtered = df[df['channel_name'] == channel_name]  # Filter by channel
    daily_sales = df_filtered.groupby("date")["amount"].sum()
    daily_sales = daily_sales.asfreq("D", fill_value=0)  # Ensure daily frequency
    return daily_sales

# Step 3: Fit the ARIMA model
def fit_arima_model(time_series: pd.Series, order=(5, 1, 0)):
    model = ARIMA(time_series, order=order)
    fitted_model = model.fit()
    return fitted_model

# Step 4: Generate sales predictions and confidence intervals
def predict_sales_with_confidence(fitted_model, target_date, steps, alpha=0.10):
    forecast_results = fitted_model.get_forecast(steps=steps)
    forecast_mean = forecast_results.predicted_mean
    confidence_intervals = forecast_results.conf_int(alpha=alpha)

    forecast_index = pd.date_range(start=forecast_mean.index[0], periods=steps, freq='D')

    forecast_df = pd.DataFrame({
        'Forecast': forecast_mean,
        'Lower CI Limit': confidence_intervals.iloc[:, 0],
        'Upper CI Limit': confidence_intervals.iloc[:, 1]
    }, index=forecast_index)

    target_date_forecast = forecast_df.loc[target_date]
    return target_date_forecast

# Step 5: Calculate confidence percentage based on confidence intervals
def calculate_confidence_from_intervals(forecast_df: pd.DataFrame) -> float:
    """Calculate the confidence based on the width of the confidence interval."""
    forecast = forecast_df['Forecast']
    lower_limit = forecast_df['Lower CI Limit']
    upper_limit = forecast_df['Upper CI Limit']
    
    # Calculate the width of the confidence interval
    ci_width = upper_limit - lower_limit
    
    # Calculate the percentage width relative to the forecast value
    relative_ci_width = (ci_width / forecast) * 100
    
    # Define a threshold for what would be considered a "narrow" confidence interval
    threshold = 10  # Example threshold (this can be adjusted)
    
    if relative_ci_width <= threshold:
        confidence_percentage = 100  # Full confidence
    else:
        # Reduce the confidence percentage proportionally to the width of the interval
        confidence_percentage = max(0, 100 - (relative_ci_width - threshold))
    
    return confidence_percentage

# Main function to handle argument parsing
def main():
    parser = argparse.ArgumentParser(description="Predict sales for a specific date across multiple channels.")
    parser.add_argument("--target_date", required=True, help="The date for sales prediction in YYYY-MM-DD format.")
    
    args = parser.parse_args()

    # Step 1: Load the transaction data (parquet file)
    df = read_transaction_file()

    # Step 2: Load the CSV file and map channel names
    channels_df = pd.read_csv("channels.csv")  # Default file name
    df = df.merge(channels_df, on="channel_id", how="left")

    # Step 3: List of channels to predict
    channels = ["Online", "In-Store", "Mobile"]

    # Step 4: Iterate over each channel and generate predictions
    target_date = args.target_date
    for channel_name in channels:
        print(f"\nPrediccion para el canal {channel_name} el dia {target_date}:")
        
        # Prepare the time series for the given channel
        time_series = prepare_time_series(df, channel_name)

        # Fit the ARIMA model
        arima_model = fit_arima_model(time_series)

        # Forecast for enough steps to include the target date (consider future dates)
        total_days = (pd.to_datetime(target_date) - time_series.index[-1]).days + 1
        forecast_result = predict_sales_with_confidence(arima_model, target_date, steps=total_days)

        if forecast_result is not None:
            # Step 5: Print the prediction results
            print(f"Forecasted Sales: {forecast_result['Forecast']:.2f}")

            # Step 6: Calculate and display the confidence percentage based on intervals
            confidence_percentage = calculate_confidence_from_intervals(forecast_result)
            print(f"La confianza de esta prediccion es: {confidence_percentage:.2f}%")

if __name__ == "__main__":
    main()
