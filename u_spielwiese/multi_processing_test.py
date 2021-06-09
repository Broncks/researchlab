import multiprocessing as mp
import os
import time

def kill_time():

    for i in range(10):
        time.sleep(1.0)
        print(i)

def modify_numbers(numbers, lock):
    with lock:
        for i in range(100):
            for j in range(len(numbers)):
                numbers[j] += 1

def modify_number(number):
    number.value += 100

if __name__ == "__main__":

    num_processes = os.cpu_count()
    processes = []

    for i in range(num_processes):
        processes.append(mp.Process(target=modify_numbers))

    for p in processes:
        p.start()

    for p in processes:
        p.join()
