# Traffic Queue Simulator Project

**Assignment**: Assignment #1 - Implementing Queue for solving the traffic light problem  
**Student Name**: Tamanna Katuwal
**Roll Number**: 36
**Date**: Dec 2025  

## 1. Summary of Work
This project simulates a smart traffic junction management system using Python and Pygame. It addresses the "Traffic Light Problem" by implementing a fair **Normal Condition** scheduling algorithm for regular flow and a specialized **Priority Queue** mechanism for high-traffic scenarios on Lane A.

The system consists of two main components:
- `traffic_generator.py`: Simulates vehicle arrivals using a Poisson process (exponential inter-arrival times) to mimic realistic traffic flow.
- `simulator.py`: The main entry point for the simulation. It orchestrates the system using the following modular files:
    - `traffic_config.py`: Stores configuration constants (screen size, colors, threshold values).
    - `traffic_logic.py`: Handles core data structures (Priority Queue), queue management, and light switching algorithms.
    - `traffic_visuals.py`: Manages all graphical rendering using Pygame (drawing roads, vehicles, and the status panel).

The simulator successfully handles the dynamic switching between "Normal Condition" (fair waiting times) and "High-Priority Condition" (Lane A flush), ensuring efficient traffic flow.

## 2. Data Structures Used

| Data Structure | Implementation Details | Purpose |
|----------------|------------------------|---------|
| **Vehicle Queue** | `collections.deque` (Doubly Ended Queue) | Stores waiting vehicles for each lane (A, B, C, D). Allows O(1) complexity for arriving (append) and serving (popleft) vehicles. |
| **Priority Queue** | `heapq` (Binary Heap) inside `PriorityQueue` class | Manages the scheduling order of traffic lights. Allows Lane A to jump to the front of the schedule when critical (>10 vehicles). |
| **List/Array** | `moving_vehicles = []` | Tracks vehicles currently animating across the intersection. |

## 3. Key Functions & Data Structure Usage
- `vehicle_queues[lane].append(vehicle)`: Adds a new car to the back of the specific road's queue.
- `vehicle_queues[lane].popleft()`: Removes the front car from the queue when the light is green.
- `PriorityQueue.add_task(road, priority)`: Inserts a road into the scheduling heap.
    - Normal Priority = 1
    - High Priority = 100 (for Lane A)
- `PriorityQueue.pop_task()`: Retrieves the road with the highest priority to serve next.

## 4. Algorithm Implementation
The traffic control logic handles two states:

### A. Normal Condition
- **Trigger**: When Lane A has < 10 vehicles.
- **Logic**: 
    1. Cycle through roads A -> B -> C -> D (Fair dispatch).
    2. Calculate Green Light Duration ($T$) dynamically:
       $$ T = \text{Avg}(\text{Waiting Vehicles on other lanes}) \times t_{\text{per\_vehicle}} $$
    3. This ensures fair distribution based on the average load of the junction.

### B. High-Priority Condition
- **Trigger**: When Lane A accumulates > 10 vehicles.
- **Logic**:
    1. Switch system to `PRIORITY_MODE`.
    2. Force Lane A Green immediately.
    3. Hold Lane A Green until its queue drops below 5 vehicles (Hysteresis).
    4. Resume Normal Condition once cleared.

## 5. Time Complexity Analysis
- **Enqueuing a Vehicle**: $O(1)$ using `deque.append`.
- **Dequeuing a Vehicle**: $O(1)$ using `deque.popleft`.
- **Scheduling Light Change**: 
    - Adding to Priority Queue: $O(\log N)$ where $N$ is number of roads (4).
    - Popping from Priority Queue: $O(\log N)$.
    - Since $N$ is constant (4), these operations are effectively $O(1)$ constant time in this specific simulation.
- **Queue Length Calculation**: $O(1)$ (Python `len()` on deque is constant time).

## 6. How to Run

1. **Start Traffic Generator**:
   Open a terminal and run:
   ```bash
   python traffic_generator.py
   ```
   (This will start generating `lane_*.txt` files with vehicle data).

2. **Start Simulator**:
   Open a second terminal and run:
   ```bash
   python simulator.py
   ```
   (The graphical window will appear).

## 7. References
- **Python Documentation**: `collections.deque` and `heapq` modules. https://docs.python.org/3/library/collections.html
- **Pygame Documentation**: Graphics and event handling. https://www.pygame.org/docs/
- **Queueing Theory**: Basics of M/M/1 queues and Poisson processes for traffic simulation.
- **Assignment 1 Problem Statement**: Logic formulas implementing Fair Dispatch and Priority Hysteresis.

## 8. Source Code
**Repository Link**: [https://github.com/TamannaKatuwal/DSA_QUEUE_SIMULATOR]
