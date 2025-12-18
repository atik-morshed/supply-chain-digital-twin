# End-to-End Supply Chain Digital Twin (FLAGSHIP PROJECT)

## What it is

A data-driven simulation of a company’s supply chain, from demand and procurement to inventory and delivery. This project uses realistic, modular components to simulate daily operations and log key performance indicators (KPIs).

## Core Features

- **Data-Driven Simulation**: Uses sample CSV files for demand, suppliers, and inventory.
- **Modular Engine**: A central `run_simulation.py` script ties all supply chain components together.
- **Daily KPI Logging**: Logs key metrics like stock levels, stockouts, costs, and lead times to a CSV file for analysis.
- **Dashboard-Ready**: The output is designed to be easily imported into tools like Power BI or Excel to build interactive dashboards.

## Tech Stack

- Python (pandas, numpy)
- Power BI / Excel (for visualization)

## How to Use

This project includes an interactive web UI to run simulations and visualize the results.

### 1. Run the Web Application

1.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the Flask application from your terminal:
    ```bash
    python app/main.py
    ```
3.  Open your web browser and navigate to `http://127.0.0.1:8080`.

### 2. Run a Simulation

-   From the dropdown menu, select a simulation scenario (e.g., Base Case, High Demand).
-   Click the **Run Simulation** button.
-   The results, including high-level KPIs and an inventory chart, will be displayed on the page.

### 3. Customize Scenarios

You can add or modify simulation scenarios by editing the files in the `/scenarios` directory. Each subdirectory represents a different scenario and must contain:

-   `demand.csv`
-   `suppliers.csv`
-   `inventory.csv`
