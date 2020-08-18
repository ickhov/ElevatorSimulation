# ElevatorSimulation

## Description
This program simulates the operation of an elevator from the point of view of the first floor. When the elevator arrives at the first floor, it will pick up the passengers who are waiting, up to its capacity, and leave immediately. Those unable to board will have to wait. If no one is waiting when the elevator arrives, the elevator will wait until a passenger arrives; he/she will board and the elevator will leave immediately.

## Running the program
In order to run the program, you need to install the SimPy library for Python. You can find the installation guide [here](https://pypi.org/project/simpy/).<br /><br />
You can run the program using the following format.

```python
% python Elevator.py passenger_arrival_rate elevator_capacity mean_elevator_return_time max_simtime 
```

You have to specify the following parameter:
* passenger_arrival_rate (0.0 - 1.0): Rate at which the passenger will be arriving.
* elevator_capacity (1 - Infinity): Maximum number of passengers allowed into the elevator.
* mean_elevator_return_time (0.1 - Infinity): Mean time elapsed from an elevator departure to next time it returns back to the first floor.
* max_simtime (0.1 - Infinity): Amount of simulated time to run the simulation.

A sample run command would look like this.

```python
% python Elevator.py 1.0 5 2.0 25000
```

The result of running the above command would be

```python
mean passenger wait:  2.49207188575
prop. of visits that leave passengers behind:  0.147056203794
```
