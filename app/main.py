import sys
import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, send_file

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.simulation.main import SupplyChainSimulation
from src.dashboard.kpi import calculate_fill_rate, calculate_service_level, calculate_inventory_turnover

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_simulation_route():
    # Get parameters from form
    initial_inventory = int(request.form.get('initial_inventory', 200))
    days = int(request.form.get('simulation_days', 365))
    reorder_point = int(request.form.get('reorder_point', 100))
    order_quantity = int(request.form.get('order_quantity', 200))

    # Generate dummy demand data
    np.random.seed(42)
    demand = {day: np.random.randint(10, 30) for day in range(1, days + 1)}

    # Define inventory policy
    policy = {
        'reorder_point': reorder_point,
        'order_quantity': order_quantity,
        'mean_lead_time': 7,
        'std_dev_lead_time': 2
    }

    # Run simulation
    sim = SupplyChainSimulation(initial_inventory=initial_inventory, demand_data=demand, inventory_policy=policy)
    results_df = sim.run_simulation(days)

    # Calculate KPIs
    fill_rate = calculate_fill_rate(results_df)
    service_level = calculate_service_level(results_df)
    cost_per_unit = 50
    total_cogs = results_df['fulfilled_demand'].sum() * cost_per_unit
    inventory_turnover = calculate_inventory_turnover(results_df, total_cogs)

    kpis = {
        'fill_rate': f"{fill_rate:.2%}",
        'service_level': f"{service_level:.2%}",
        'inventory_turnover': f"{inventory_turnover:.2f}"
    }

    # Prepare data for the chart
    chart_data = {
        'labels': results_df['day'].tolist(),
        'values': results_df['inventory_level'].tolist()
    }

    # Save full results to a temporary CSV file for download
    results_df.to_csv('output/simulation_log.csv', index=False)

    # Convert dataframe to HTML table for display
    results_html = results_df.tail(10).to_html(classes='table table-striped table-hover', index=False)

    return render_template('index.html', results=results_html, kpis=kpis, chart_data=chart_data)

@app.route('/download')
def download_log():
    return send_file('../output/simulation_log.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
