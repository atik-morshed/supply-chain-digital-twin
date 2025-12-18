import pandas as pd
from datetime import datetime, timedelta
import os

# Import modular functions
from src.demand_forecast import forecast_demand
from src.procurement import procure_orders
from src.inventory_policy import update_inventory
from src.warehouse import fulfill_orders
from src.delivery import simulate_delivery

# --- Simulation Parameters ---
SIMULATION_DAYS = 365
OUTPUT_FILE = 'outputs/kpis.csv'

# --- Main Simulation Logic ---
def simulate():
    # Load datasets
    demand_df = pd.read_csv('data/demand.csv', parse_dates=['date'])
    suppliers_df = pd.read_csv('data/suppliers.csv')
    inventory_df = pd.read_csv('data/inventory.csv')

    # Initialize state variables
    inventory = inventory_df.set_index('product_id')['initial_stock'].to_dict()
    on_order = {p_id: 0 for p_id in inventory.keys()}
    lead_time_queue = {p_id: [] for p_id in inventory.keys()}
    kpis = []

    start_date = demand_df['date'].min()

    for day in range(SIMULATION_DAYS):
        current_date = start_date + timedelta(days=day)

        for product_id in inventory.keys():
            # --- 1. Receive incoming orders ---
            incoming_shipments = 0
            orders_due_today = [order for order in lead_time_queue[product_id] if order['arrival_date'] == current_date]
            for order in orders_due_today:
                incoming_shipments += order['quantity']
                on_order[product_id] -= order['quantity']
                lead_time_queue[product_id].remove(order)

            # --- 2. Forecast Demand ---
            daily_demand = forecast_demand(demand_df, current_date, product_id)

            # --- 3. Fulfill Orders from Warehouse ---
            fulfilled, stockout = fulfill_orders(inventory[product_id], daily_demand)

            # --- 4. Update Inventory ---
            inventory[product_id] = update_inventory(inventory[product_id], fulfilled, incoming_shipments)

            # --- 5. Procurement & Inventory Policy ---
            inventory_info = inventory_df[inventory_df['product_id'] == product_id].iloc[0]
            supplier_info = suppliers_df[suppliers_df['product_id'] == product_id].iloc[0]
            new_order = procure_orders(current_date, inventory[product_id], on_order[product_id], product_id, inventory_info, supplier_info, daily_demand)
            
            lead_time = 0
            ordering_cost = 0
            if new_order:
                on_order[product_id] += new_order['quantity']
                lead_time_queue[product_id].append(new_order)
                lead_time = new_order['lead_time']
                ordering_cost = inventory_info['ordering_cost']

            # --- 6. Simulate Delivery ---
            delivery_stats = simulate_delivery(fulfilled)

            # --- 7. Calculate Costs & Log KPIs ---
            holding_cost = inventory[product_id] * inventory_info['holding_cost']
            stockout_cost = stockout * inventory_info['stockout_cost']
            total_cost = holding_cost + stockout_cost + ordering_cost

            daily_kpi = {
                'date': current_date,
                'product_id': product_id,
                'total_demand': daily_demand,
                'fulfilled': fulfilled,
                'stockout': stockout,
                'inventory_level': inventory[product_id],
                'lead_time': lead_time,
                'delivery_delay': delivery_stats['delay_days'],
                'total_cost': total_cost
            }
            kpis.append(daily_kpi)

    # --- Save results ---
    kpi_df = pd.DataFrame(kpis)
    kpi_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Simulation complete. KPI data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    simulate()
