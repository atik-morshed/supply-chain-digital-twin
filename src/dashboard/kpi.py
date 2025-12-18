import pandas as pd

def calculate_fill_rate(results_df):
    """Calculates the fill rate from the simulation results."""
    total_demand = results_df['daily_demand'].sum()
    total_fulfilled = results_df['fulfilled_demand'].sum()
    if total_demand == 0:
        return 1.0 # 100% fill rate if no demand
    return total_fulfilled / total_demand

def calculate_service_level(results_df):
    """Calculates the service level (days without stockouts)."""
    days_with_stockout = results_df[results_df['stockout'] > 0].shape[0]
    total_days = results_df.shape[0]
    if total_days == 0:
        return 1.0 # 100% service level if no days simulated
    return (total_days - days_with_stockout) / total_days

def calculate_inventory_turnover(results_df, total_cogs):
    """Calculates the inventory turnover ratio."""
    avg_inventory = results_df['inventory_level'].mean()
    if avg_inventory == 0:
        return float('inf') # Avoid division by zero
    return total_cogs / avg_inventory
