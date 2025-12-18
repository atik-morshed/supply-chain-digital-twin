import sys
import os
from flask import Flask, render_template, request

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.simulation_engine import run_simulation

app = Flask(__name__)

@app.route('/')
def index():
    scenarios = [d for d in os.listdir('scenarios') if os.path.isdir(os.path.join('scenarios', d))]
    return render_template('index.html', scenarios=scenarios)

@app.route('/run', methods=['POST'])
def run_simulation_route():
    scenario = request.form.get('scenario')
    if not scenario:
        return "Error: No scenario selected", 400

    # Run simulation
    results_df = run_simulation(scenario_name=scenario, sim_days=30)

    # Calculate high-level KPIs
    total_cost = results_df['total_cost'].sum()
    total_stockouts = results_df['stockout_qty'].sum()
    avg_inventory = results_df['inventory_stock'].mean()

    kpis = {
        'total_cost': f"${total_cost:,.2f}",
        'total_stockouts': f"{total_stockouts:,}",
        'avg_inventory': f"{avg_inventory:,.2f}"
    }

    # Prepare data for the chart (showing inventory for the first product)
    first_product = results_df['product_id'].unique()[0]
    product_df = results_df[results_df['product_id'] == first_product]
    chart_data = {
        'labels': product_df['date'].dt.strftime('%Y-%m-%d').tolist(),
        'values': product_df['inventory_stock'].tolist()
    }

    # Get a list of available scenarios for the dropdown
    scenarios = [d for d in os.listdir('scenarios') if os.path.isdir(os.path.join('scenarios', d))]

    return render_template('index.html', kpis=kpis, chart_data=chart_data, scenarios=scenarios, selected_scenario=scenario)

if __name__ == '__main__':
    app.run(debug=True, port=8080)

