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
