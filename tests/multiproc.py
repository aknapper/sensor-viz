#!/usr/bin/env python3

import multiprocessing

var = multiprocessing.Value('i', 0)

def worker_function(name):
    print(f"Worker {name} is executing.")
    with var.get_lock():
        var.value += 1

if __name__ == "__main__":
    # Create a multiprocessing Pool with 4 processes
    pool = multiprocessing.Pool(processes=4)

    # Create a list of tasks
    tasks = ["A", "B", "C", "D"]

    # Map the tasks to the worker function using the Pool
    pool.map(worker_function, tasks)

    # Close the Pool and wait for the worker processes to finish
    pool.close()
    pool.join()

    print(f"var {var.value}\n")

    print("All tasks completed.")