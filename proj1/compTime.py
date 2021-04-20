import time

class ComputingTime:

    def __init__(self):
        self.timestampStart = 0

    def computingTimeStart(self):
        self.timestampStart = time.time()

    def giveComputingTimeAndStop(self):
        myTime = time.time() - self.timestampStart
        return myTime