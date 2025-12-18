import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# --- Helper Functions ---
def get_lead_time(mean, std):
    return int(round(max(1, np.random.normal(mean, std))))

# --- Main Simulation Logic ---
def run_simulation(scenario_name='base_case', sim_days=30):
    # Define paths based on scenario
    base_path = f'scenarios/{scenario_name}'
    demand_path = os.path.join(base_path, 'demand.csv')
    suppliers_path = os.path.join(base_path, 'suppliers.csv')
    inventory_path = os.path.join(base_path, 'inventory.csv')

    # Load data
    demand_df = pd.read_csv(demand_path, parse_dates=['date'])
    suppliers_df = pd.read_csv(suppliers_path)
    inventory_df = pd.read_csv(inventory_path)

    # Initialize state
    inventory = inventory_df.set_index('product_id')['initial_stock'].to_dict()
    on_order = {p_id: 0 for p_id in inventory.keys()}
    lead_time_queue = {p_id: [] for p_id in inventory.keys()}
    kpi_log = []

    start_date = demand_df['date'].min()

    for day in range(sim_days):
        current_date = start_date + timedelta(days=day)

        for product_id in inventory.keys():
            # 1. Receive incoming orders
            orders_due_today = [order for order in lead_time_queue[product_id] if order['arrival_date'] == current_date]
            for order in orders_due_today:
                inventory[product_id] += order['quantity']
                on_order[product_id] -= order['quantity']
                lead_time_queue[product_id].remove(order)

            # 2. Fulfill demand
            try:
                daily_demand = int(demand_df[(demand_df['date'] == current_date) & (demand_df['product_id'] == product_id)]['quantity'].iloc[0])
            except IndexError:
                daily_demand = 0

            fulfilled_demand = min(inventory[product_id], daily_demand)
            stockout = daily_demand - fulfilled_demand
            inventory[product_id] -= fulfilled_demand

            # 3. Inventory Policy & Ordering
            product_info = inventory_df[inventory_df['product_id'] == product_id].iloc[0]
            supplier_info = suppliers_df[suppliers_df['product_id'] == product_id].iloc[0]

            reorder_point = ((supplier_info['lead_time_avg'] * (daily_demand + 1)) + (2 * np.sqrt(supplier_info['lead_time_avg'] * (daily_demand + 1))))
            if inventory[product_id] <= reorder_point and on_order[product_id] == 0:
                order_quantity = 200
                on_order[product_id] += order_quantity
                lead_time = get_lead_time(supplier_info['lead_time_avg'], supplier_info['lead_time_std'])
                arrival_date = current_date + timedelta(days=lead_time)
                lead_time_queue[product_id].append({'arrival_date': arrival_date, 'quantity': order_quantity})
            else:
                lead_time = 0

            # 4. Calculate Costs
            holding_cost = inventory[product_id] * product_info['holding_cost']
            stockout_cost = stockout * product_info['stockout_cost']
            ordering_cost = product_info['ordering_cost'] if on_order[product_id] > 0 and lead_time > 0 else 0
            total_cost = holding_cost + stockout_cost + ordering_cost

            # 5. Log KPIs
            kpi_log.append({
                'date': current_date,
                'product_id': product_id,
                'demand': daily_demand,
                'inventory_stock': inventory[product_id],
                'stockout_qty': stockout,
                'order_lead_time': lead_time,
                'delivery_delay': 0,
                'total_cost': total_cost
            })

    return pd.DataFrame(kpi_log)

if __name__ == "__main__":
    # Example of running the simulation directly
    if not os.path.exists('output'):
        os.makedirs('output')
    results = run_simulation('base_case', 30)
    results.to_csv('output/kpis.csv', index=False)
    print("Simulation complete. Results saved to output/kpis.csv")
