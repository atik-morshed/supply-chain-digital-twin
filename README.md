# End-to-End Supply Chain Digital Twin (FLAGSHIP PROJECT)

## What it is

A full simulation of a company’s supply chain:
Demand → Procurement → Inventory → Warehouse → Delivery

## Core features

- Demand forecasting (monthly/weekly)
- Supplier lead time variability
- Inventory policy (EOQ / Reorder Point)
- Stockout & overstock simulation
- Delivery delay tracking

## KPI dashboard:

- Fill rate
- Service level
- Inventory turnover
- Cost impact

## Tech stack

- Python (pandas, numpy, matplotlib)
- Excel / Power BI (dashboard)
- Optional: Flask web UI

## How to Use

### Running the Simulation (Web UI)

1.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the Flask application:
    ```bash
    python app/main.py
    ```
3.  Open your web browser and navigate to `http://127.0.0.1:5000`.
4.  Enter your desired simulation parameters and click "Run Simulation".

### Using with Excel / Power BI

After running a simulation in the web UI, you can download the full simulation log as a CSV file by clicking the **Download Full Log (CSV)** button.

This CSV file can be easily opened in **Microsoft Excel** for data analysis, pivot tables, and custom charts.

To use the data in **Power BI**:

1.  Open Power BI Desktop.
2.  On the Home ribbon, click **Get Data** and select **Text/CSV**.
3.  Navigate to the downloaded `simulation_log.csv` file and open it.
4.  Click **Load** to import the data into your Power BI model.
5.  You can now use the Power BI report builder to create interactive dashboards and visualizations based on the simulation data.
