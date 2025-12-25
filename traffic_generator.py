# traffic_generator.py
import time
import random
import os
import argparse

# Configuration
LANES = ['A', 'B', 'C', 'D']
LANE_FILES = {
    'A': 'lane_a.txt',
    'B': 'lane_b.txt',
    'C': 'lane_c.txt',
    'D': 'lane_d.txt'
}

# Arrival rate (vehicles per second). By default use Poisson arrivals with mean 1 vehicle/sec.
ARRIVAL_RATE = 1.0  # vehicles per second

def clear_files():
    """Clear content of lane files at startup."""
    for lane, filename in LANE_FILES.items():
        with open(filename, 'w') as f:
            f.write('')

def generate_traffic(rate=ARRIVAL_RATE):
    """Generates traffic using Poisson arrivals (exponential inter-arrival times).

    rate: mean arrival rate in vehicles per second.
    """
    print("Starting Traffic Generator...")
    print("Press Ctrl+C to stop.")
    
    vehicle_id_counter = 1
    
    try:
        while True:
            # Randomly select a road/lane to add a vehicle
            lane = random.choices(LANES, weights=[0.4, 0.2, 0.2, 0.2], k=1)[0]
            
            filename = LANE_FILES[lane]
            
            timestamp = time.time()
            vehicle_data = f"{vehicle_id_counter},{timestamp}\n"
            
            with open(filename, 'a') as f:
                f.write(vehicle_data)
            
            print(f"Generated Vehicle {vehicle_id_counter} on Lane {lane} (rate={rate:.2f} v/s)")
            
            vehicle_id_counter += 1
            
            # Poisson arrivals -> exponential inter-arrival times
            # random.expovariate expects the rate parameter (events per second)
            sleep_time = random.expovariate(rate) if rate > 0 else 1.0
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        print("\nTraffic Generator Stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Traffic generator using Poisson arrivals')
    parser.add_argument('--rate', '-r', type=float, default=ARRIVAL_RATE,
                        help='average arrival rate in vehicles per second (default 1.0)')
    args = parser.parse_args()
    clear_files()
    generate_traffic(rate=args.rate)
