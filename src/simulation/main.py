import pandas as pd
import numpy as np

from src.demand.forecasting import forecast_demand
from src.procurement.supplier import get_lead_time
from src.inventory.policy import calculate_reorder_point, calculate_eoq
from src.dashboard.kpi import calculate_fill_rate, calculate_service_level, calculate_inventory_turnover

class SupplyChainSimulation:
    def __init__(self, initial_inventory, demand_data, inventory_policy):
        self.inventory_level = initial_inventory
        self.demand_data = demand_data
        self.policy = inventory_policy
        self.simulation_log = []
        self.on_order = 0
        self.lead_time_queue = []

    def run_simulation(self, days):
        for day in range(1, days + 1):
            # Receive orders that are due
            if day in [d for d, qty in self.lead_time_queue]:
                order_index = [d for d, qty in self.lead_time_queue].index(day)
                order_due = self.lead_time_queue.pop(order_index)
                self.inventory_level += order_due[1]
                self.on_order -= order_due[1]

            # Get daily demand
            daily_demand = self.demand_data.get(day, 0)

            # Fulfill demand
            fulfilled_demand = min(self.inventory_level, daily_demand)
            stockout = daily_demand - fulfilled_demand
            self.inventory_level -= fulfilled_demand

            # Check inventory and place order
            if self.inventory_level <= self.policy['reorder_point'] and self.on_order == 0:
                order_quantity = self.policy['order_quantity']
                self.on_order += order_quantity
                lead_time = get_lead_time(self.policy['mean_lead_time'], self.policy['std_dev_lead_time'])
                arrival_day = day + lead_time
                self.lead_time_queue.append((arrival_day, order_quantity))

            # Log results
            self.simulation_log.append({
                'day': day,
                'inventory_level': self.inventory_level,
                'daily_demand': daily_demand,
                'fulfilled_demand': fulfilled_demand,
                'stockout': stockout,
                'on_order': self.on_order
            })

        return pd.DataFrame(self.simulation_log)

if __name__ == '__main__':
    # Example Usage
    # Generate some dummy demand data
    np.random.seed(42)
    days = 365
    demand = {day: np.random.randint(10, 30) for day in range(1, days + 1)}

    # Define inventory policy
    policy = {
        'reorder_point': 100,
        'order_quantity': 200,
        'mean_lead_time': 7,
        'std_dev_lead_time': 2
    }

    sim = SupplyChainSimulation(initial_inventory=200, demand_data=demand, inventory_policy=policy)
    results_df = sim.run_simulation(days)

    print(results_df.tail())

    # Calculate and print KPIs
    fill_rate = calculate_fill_rate(results_df)
    service_level = calculate_service_level(results_df)

    # For inventory turnover, we need COGS. Let's assume a cost per unit.
    cost_per_unit = 50
    total_cogs = results_df['fulfilled_demand'].sum() * cost_per_unit
    inventory_turnover = calculate_inventory_turnover(results_df, total_cogs)

    print("\n--- KPIs ---")
    print(f"Fill Rate: {fill_rate:.2%}")
    print(f"Service Level: {service_level:.2%}")
    print(f"Inventory Turnover: {inventory_turnover:.2f}")
