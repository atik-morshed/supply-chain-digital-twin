import numpy as np
from datetime import timedelta

def get_lead_time(mean, std):
    return int(round(max(1, np.random.normal(mean, std))))

def procure_orders(current_date, inventory_level, on_order, product_id, inventory_info, supplier_info, demand_forecast):
    """Decides whether to place a new order based on inventory policy."""
    # Simple reorder point (ROP) policy
    reorder_point = ((supplier_info['lead_time_avg'] * (demand_forecast + 1)) + (2 * np.sqrt(supplier_info['lead_time_avg'] * (demand_forecast + 1))))
    
    if inventory_level <= reorder_point and on_order == 0:
        order_quantity = 200 # Using a fixed order quantity for simplicity
        lead_time = get_lead_time(supplier_info['lead_time_avg'], supplier_info['lead_time_std'])
        arrival_date = current_date + timedelta(days=lead_time)
        order = {'arrival_date': arrival_date, 'quantity': order_quantity, 'lead_time': lead_time}
        return order
    return None
