# python Elevator.py passenger_arrival_rate elevator_capacity mean_elevator_return_time elevator_standby_time max_simtime

from SimPy.Simulation import *
from random import Random,expovariate,uniform
import sys

class G: #globals
    Rnd = Random(12345)
    elevProc = None
    passProc = None

class Passenger(Process):

    def __init__(self):
      Process.__init__(self)
      G.passProc = self
      self.passengerArrivalRate = float(sys.argv[1])
      # self.arrvs will be arrivals waiting for pickup
      self.arrvs = [0.0]

    def Run(self):
      while True:
         # sim next arrival
         yield hold,self,G.Rnd.expovariate(self.passengerArrivalRate)
         self.arrvs.append(now())
         # reactivate Elevator after a passenger arrives
         if G.elevProc.isWaiting:
             reactivate(G.elevProc)

class Elevator(Process):

    totalSimulation = 0
    elevatorCapacity = int(sys.argv[2])
    meanElevatorReturnTime = float(sys.argv[3])
    totalWaitTime = 0.0
    totalpassengerCount = 0
    passengerOverflowCount = 0.0

    def __init__(self):
        Process.__init__(self)
        G.elevProc = self
        self.isWaiting = False
        self.startTime = 0

    def Run(self):
        while True:
            Elevator.totalSimulation += 1
            self.isWaiting = False
            self.startTime = now()
            # simulate elevator returning to first floor
            numPassengersWaiting = len(G.passProc.arrvs)
            if numPassengersWaiting == 0:
                # simulate elevator waiting for passengers
                self.isWaiting = True
                yield passivate,self
                self.isWaiting = False

            # board as much passengers as possible
            self.boardPassengers(numPassengersWaiting)

            # simulate elevator arriving
            # the rate is 1/mean
            yield hold,self,G.Rnd.expovariate(1/Elevator.meanElevatorReturnTime)

    def boardPassengers(self, numPassengersWaiting):
        maxPassengersToBoard = numPassengersWaiting
        # check how many times we didn't have enough room
        if numPassengersWaiting > Elevator.elevatorCapacity:
            maxPassengersToBoard = Elevator.elevatorCapacity
            Elevator.passengerOverflowCount += 1
        # calculate the total wait time and update number of passenger we serviced so far
        for _ in range(maxPassengersToBoard):
            passWaitTime = G.passProc.arrvs.pop(0)
            Elevator.totalWaitTime += self.startTime - passWaitTime
            Elevator.totalpassengerCount += 1

def main():
    initialize()
    elevator = Elevator()
    activate(elevator,elevator.Run())
    passengers = Passenger()
    activate(passengers, passengers.Run())
    maxSimtime = float(sys.argv[4])
    simulate(until=maxSimtime)
    print 'mean passenger wait:', Elevator.totalWaitTime / Elevator.totalpassengerCount
    print 'prop. of visits that leave passengers behind:', Elevator.passengerOverflowCount / Elevator.totalSimulation

if __name__ == '__main__': main()
