# End-to-End Supply Chain Digital Twin

This project is a data-driven simulation of a company’s supply chain, built to model and analyze the impact of demand uncertainty, inventory policies, and supplier variability on operational performance.

## Problem Statement

In supply chain management, balancing inventory levels to meet customer demand without incurring excessive costs is a critical challenge. Under-stocking leads to lost sales and poor service levels, while over-stocking results in high holding costs and wasted capital. This digital twin was built to simulate these trade-offs, providing measurable insights into how different strategies affect key business outcomes.

## Architecture

The simulation is built on a modular, data-driven architecture that separates the core logic from the data inputs. This allows for easy scenario testing and analysis.

```
/supply-chain-digital-twin
|-- /data
|   |-- demand.csv
|   |-- suppliers.csv
|   |-- inventory.csv
|-- /src
|   |-- demand_forecast.py
|   |-- procurement.py
|   |-- inventory_policy.py
|   |-- warehouse.py
|   |-- delivery.py
|-- /outputs
|   |-- kpis.csv (Generated)
|   |-- inventory_over_time.png (Generated)
|-- run_simulation.py  (Main Engine)
|-- visualize.py       (Plot Generator)
|-- requirements.txt
|-- README.md
```

## How to Run

### 1. Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/atik-morshed/supply-chain-digital-twin.git
cd supply-chain-digital-twin
pip install -r requirements.txt
```

### 2. Run the Simulation

Execute the main simulation engine script from your terminal. This will read the data from `/data`, run a 365-day simulation, and generate a detailed KPI log in the `/outputs` directory.

```bash
python run_simulation.py
```

### 3. Generate Visualizations

After the simulation is complete, run the visualization script to generate plots from the KPI data. The plots will be saved in the `/outputs` directory.

```bash
python visualize.py
```

## KPI Explanation

The simulation generates a `kpis.csv` file with the following key metrics for each product on each day:

| Column            | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| `date`            | The date of the simulation day.                                             |
| `product_id`      | The unique identifier for the product.                                      |
| `total_demand`    | The quantity of the product demanded by customers.                          |
| `fulfilled`       | The quantity of demand that was successfully met from available inventory.  |
| `stockout`        | The quantity of demand that could not be met (lost sales).                  |
| `inventory_level` | The quantity of stock on hand at the end of the day.                        |
| `lead_time`       | The number of days for a new order to arrive (0 if no order was placed).    |
| `delivery_delay`  | Placeholder for delivery delay simulation (currently 0).                    |
| `total_cost`      | The sum of holding, stockout, and ordering costs for the day.               |

## Sample Results & Insights

The `visualize.py` script generates the following plots, which provide immediate insights into the simulation's performance.

**Inventory Level Over Time**

This chart shows the fluctuation of stock for each product over the simulation period. It helps identify trends, seasonality, and the effectiveness of the inventory policy.

*(This is where you would embed the `inventory_over_time.png` image)*

**Cost Breakdown Over Time**

This chart visualizes the total operational cost per day, helping to identify cost drivers and the financial impact of stockouts or excess inventory.

*(This is where you would embed the `cost_over_time.png` image)*

## Using with Power BI / Excel

The `outputs/kpis.csv` file is designed to be a direct data source for business intelligence tools. You can import this file into Power BI or Excel to create interactive dashboards and perform deeper analysis on metrics like:

- **Fill Rate**: `SUM(fulfilled) / SUM(total_demand)`
- **Service Level**: `(Total Days - Days with Stockouts) / Total Days`
- **Inventory Turnover**: `Total Cost of Goods Sold / Average Inventory Value`
