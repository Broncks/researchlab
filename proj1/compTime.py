import time

class ComputingTime:

    def __init__(self):
        self.timestampStart = 0

    def computingTimeStart(self):
        self.timestampStart = time.perf_counter_ns()

    def giveComputingTimeAndStop(self):
        myTime = time.perf_counter_ns() - self.timestampStart

        return myTime