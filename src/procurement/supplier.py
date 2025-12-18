import numpy as np

def get_lead_time(mean_lead_time, std_dev_lead_time):
    """Simulates supplier lead time with variability."""
    lead_time = np.random.normal(mean_lead_time, std_dev_lead_time)
    return int(round(max(1, lead_time))) # Ensure lead time is at least 1 day

if __name__ == '__main__':
    # Example Usage
    mean_lt = 10 # days
    std_dev_lt = 2 # days

    print("Simulated Lead Times:")
    for _ in range(10):
        print(get_lead_time(mean_lt, std_dev_lt))
