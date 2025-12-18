import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Configuration ---
KPI_FILE = 'outputs/kpis.csv'
OUTPUT_DIR = 'outputs'

def create_visualizations():
    """Reads the KPI data and generates visualizations."""
    if not os.path.exists(KPI_FILE):
        print(f"Error: KPI file not found at {KPI_FILE}. Please run the simulation first.")
        return

    df = pd.read_csv(KPI_FILE, parse_dates=['date'])

    # Set plot style
    sns.set_theme(style="whitegrid")

    # --- 1. Inventory Level Over Time ---
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='date', y='inventory_level', hue='product_id')
    plt.title('Inventory Level Over Time')
    plt.xlabel('Date')
    plt.ylabel('Inventory Level (Units)')
    plt.legend(title='Product ID')
    plt.tight_layout()
    inventory_plot_path = os.path.join(OUTPUT_DIR, 'inventory_over_time.png')
    plt.savefig(inventory_plot_path)
    print(f"Saved inventory plot to {inventory_plot_path}")
    plt.close()

    # --- 2. Cost Breakdown Over Time ---
    cost_df = df.groupby('date')[['total_cost']].sum().reset_index()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=cost_df, x='date', y='total_cost')
    plt.title('Total Cost Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Cost ($)')
    plt.tight_layout()
    cost_plot_path = os.path.join(OUTPUT_DIR, 'cost_over_time.png')
    plt.savefig(cost_plot_path)
    print(f"Saved cost plot to {cost_plot_path}")
    plt.close()

if __name__ == "__main__":
    create_visualizations()
