import numpy as np

def calculate_eoq(demand, ordering_cost, holding_cost):
    """Calculates the Economic Order Quantity (EOQ)."""
    if holding_cost == 0:
        return float('inf') # Avoid division by zero
    return np.sqrt((2 * demand * ordering_cost) / holding_cost)

def calculate_reorder_point(lead_time_demand, safety_stock):
    """Calculates the Reorder Point (ROP)."""
    return lead_time_demand + safety_stock

if __name__ == '__main__':
    # Example Usage
    annual_demand = 1000 # units
    cost_per_order = 50 # currency
    holding_cost_per_unit = 2 # currency per unit per year

    eoq = calculate_eoq(annual_demand, cost_per_order, holding_cost_per_unit)
    print(f"Economic Order Quantity (EOQ): {eoq:.2f} units")

    avg_lead_time = 10 # days
    avg_daily_demand = annual_demand / 365
    lead_time_demand = avg_daily_demand * avg_lead_time
    safety_stock = 50 # units

    rop = calculate_reorder_point(lead_time_demand, safety_stock)
    print(f"Reorder Point (ROP): {rop:.2f} units")
