import pandas as pd

def forecast_demand(demand_data, current_date, product_id):
    """Fetches the demand for a given product on a specific date."""
    try:
        demand = int(demand_data[(demand_data['date'] == current_date) & (demand_data['product_id'] == product_id)]['demand'].iloc[0])
    except IndexError:
        demand = 0 # No demand for this product on this day
    return demand
