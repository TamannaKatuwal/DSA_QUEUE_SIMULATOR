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
