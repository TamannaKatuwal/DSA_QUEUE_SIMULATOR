# traffic_logic.py
import time
import heapq
import random
import os
from collections import deque
from traffic_config import *

# this class helps us manage which road gets the green light next
class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.entry_finder = {} # stores the tasks 
        self.counter = 0     # simply counts things to keep order

    # add a task with a specific priority
    def add_task(self, task, priority=0):
        if task in self.entry_finder:
            self.remove_task(task)
        count = self.counter
        self.counter += 1
        # using negative priority because heapq is a min-heap by default
        entry = [-priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.heap, entry)

    # marks a task as removed so we skip it later
    def remove_task(self, task):
        entry = self.entry_finder.pop(task)
        entry[-1] = '<REMOVED>'

    # gets the highest priority task
    def pop_task(self):
        while self.heap:
            priority, count, task = heapq.heappop(self.heap)
            if task != '<REMOVED>':
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    def is_empty(self):
        return not bool(self.entry_finder)

# --- State Variables ---
vehicle_queues = {
    'A': deque(),
    'B': deque(),
    'C': deque(),
    'D': deque()
}

road_priority_queue = PriorityQueue()
traffic_lights = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
moving_vehicles = [] # list for cars that are driving across the intersection
last_served_time = {'A': 0.0, 'B': 0.0, 'C': 0.0, 'D': 0.0}

# Timing stuff
last_switch_time = 0
current_green_road = None
current_duration = 5.0
PRIORITY_MODE = False

# simple function to read the text files for each lane
def read_lane_files():
    for lane in LANE_FILES:
        try:
            fn = LANE_FILES[lane]
            if os.path.exists(fn):
                with open(fn, 'r+') as f:
                    lines = f.readlines()
                    # clear the file after reading so we dont read same car twice
                    f.seek(0)
                    f.truncate()
                    for line in lines:
                        if line.strip():
                            p = line.strip().split(',')
                            if len(p) >= 1:
                                # assigning a random color to the car
                                vehicle_queues[lane].append({
                                    'id': p[0], 
                                    'time': float(p[1]) if len(p)>1 else time.time(),
                                    'color': random.choice([BLUE, YELLOW, WHITE, ORANGE])
                                })
        except Exception as e:
            print(f"File Error: {e}")

# core logic for switching lights
def update_lights_logic():
    global current_green_road, last_switch_time, PRIORITY_MODE, current_duration
    
    current_time = time.time()
    
    # 1. Update Priorities based on queue length
    # check if lane A is getting too full
    if len(vehicle_queues['A']) > AL2_PRIORITY_THRESHOLD:
        PRIORITY_MODE = True
        road_priority_queue.add_task('A', priority=100) # give it super high priority
    elif len(vehicle_queues['A']) < AL2_NORMAL_THRESHOLD:
        # if we cleared enough cars, go back to normal
        if PRIORITY_MODE:
             PRIORITY_MODE = False
             road_priority_queue.add_task('A', priority=1) 
    
    # make sure other roads are in the queue with normal priority
    for r in ['B', 'C', 'D']:
        road_priority_queue.add_task(r, priority=1)
    if not PRIORITY_MODE:
        road_priority_queue.add_task('A', priority=1)

    # 2. Check if we need to switch lights
    # time to switch if duration is passed or no green light is on
    if current_green_road is None or (current_time - last_switch_time > current_duration):
        next_road = None
        
        if PRIORITY_MODE:
            next_road = 'A'
            current_duration = 5.0 # quick flush duration
        else:
            # simple round robin logic
            roads = ['A', 'B', 'C', 'D']
            if current_green_road is None:
                next_road = 'A'
            else:
                curr_idx = roads.index(current_green_road)
                next_road = roads[(curr_idx + 1) % 4]
            
            # calculating dynamic duration based on assignment formula
            other_roads = [r for r in roads if r != next_road]
            total_waiting_others = sum(len(vehicle_queues[r]) for r in other_roads)
            avg_waiting = total_waiting_others / 3.0
            
            t_per_vehicle = 3.0 
            vehicles_to_serve = max(2, round(avg_waiting)) 
            current_duration = vehicles_to_serve * t_per_vehicle
            
            # keep it reasonable, dont let it stay green forever
            current_duration = min(current_duration, 30.0) 

        # actually changing the light states
        if next_road != current_green_road:
            for r in ['A', 'B', 'C', 'D']:
                traffic_lights[r] = 1 if r == next_road else 0
            
            current_green_road = next_road
            last_switch_time = current_time

# function to move cars from queue to intersection
def process_vehicles():
    current_time = time.time()
    for road in ['A', 'B', 'C', 'D']:
        # if light is Green (1) and cars are waiting
        if traffic_lights[road] == 1 and vehicle_queues[road]:
            # throttle the flow so they don't all go at once
            if current_time - last_served_time[road] >= MIN_GAP:
                v = vehicle_queues[road].popleft()
                
                # set spawn position based on the road
                if road == 'A':
                    mv = {'lane': 'A', 'x': 370.0, 'y': 280.0, 'dx': 0.0, 'dy': 1.0, 'w': 20, 'h': 28}
                elif road == 'B':
                    mv = {'lane': 'B', 'x': 410.0, 'y': 520.0, 'dx': 0.0, 'dy': -1.0, 'w': 20, 'h': 28}
                elif road == 'C':
                    mv = {'lane': 'C', 'x': 520.0, 'y': 370.0, 'dx': -1.0, 'dy': 0.0, 'w': 28, 'h': 20}
                elif road == 'D':
                    mv = {'lane': 'D', 'x': 260.0, 'y': 410.0, 'dx': 1.0, 'dy': 0.0, 'w': 28, 'h': 20}
                
                mv['speed'] = MOVE_SPEED
                moving_vehicles.append(mv)
                last_served_time[road] = current_time

# updates position of moving cars
def update_moving_vehicles(dt):
    to_rem = []
    for i, mv in enumerate(moving_vehicles):
        mv['x'] += mv['dx'] * mv['speed'] * dt
        mv['y'] += mv['dy'] * mv['speed'] * dt
        
        # if car goes off screen, remove it
        if mv['x'] < -50 or mv['x'] > WIDTH + 50 or mv['y'] < -50 or mv['y'] > HEIGHT + 50:
            to_rem.append(i)
            
    for i in reversed(to_rem):
        moving_vehicles.pop(i)
