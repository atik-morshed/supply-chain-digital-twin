import pandas as pd
import numpy as np

def moving_average(data, window_size):
    """Calculates the moving average for a given dataset."""
    return data.rolling(window=window_size).mean()

def forecast_demand(historical_data, method='moving_average', **kwargs):
    """Forecasts demand based on the selected method."""
    if method == 'moving_average':
        window = kwargs.get('window', 3) # Default window of 3 months/weeks
        return moving_average(historical_data, window)
    # Other forecasting methods can be added here
    else:
        raise ValueError("Unsupported forecasting method")

if __name__ == '__main__':
    # Example Usage
    # Create a sample historical sales data
    data = {
        'period': range(1, 13),
        'sales': [100, 110, 105, 120, 125, 130, 140, 135, 145, 150, 160, 155]
    }
    df = pd.DataFrame(data)
    df.set_index('period', inplace=True)

    # Forecast demand using a 3-period moving average
    df['forecast'] = forecast_demand(df['sales'], method='moving_average', window=3)

    print(df)
