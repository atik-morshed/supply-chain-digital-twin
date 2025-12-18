def fulfill_orders(inventory_level, demand):
    """Fulfills demand based on the current inventory level."""
    fulfilled = min(inventory_level, demand)
    stockout = demand - fulfilled
    return fulfilled, stockout
