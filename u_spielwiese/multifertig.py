from multiprocessing import Process
import time


def multiFunc():
    time.sleep(1)
    print("funcy")
    return "WOW"

timeStart = time.perf_counter_ns()

myTime = time.perf_counter_ns()

if __name__ == '__main__':
    process1 = Process(target=multiFunc())
    process2 = Process(target=multiFunc())

    print(multiFunc())

    processstarttime = time.perf_counter()
    process1.start()
    process2.start()

    print(process1.join())
    print("Process 1: ", time.perf_counter())
    print(process2.join())
    print("Process 2: ",time.perf_counter())
