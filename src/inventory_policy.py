def update_inventory(inventory_level, fulfilled_demand, incoming_orders):
    """Updates the inventory level based on demand and new arrivals."""
    inventory_level -= fulfilled_demand
    inventory_level += incoming_orders
    return inventory_level
