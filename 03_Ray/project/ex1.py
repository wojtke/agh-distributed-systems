import cProfile
import os

import numpy as np
import ray


#
# Exercise 1: Try using local bubble sort and remote bubble sort, show difference.
#


# Function for local execution
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


# Function for remote Ray task with just a wrapper
bubble_sort_distributed = ray.remote(bubble_sort)


# Normal Python in a single process
def run_local(arr):
    results = [bubble_sort(arr) for _ in range(os.cpu_count())]
    return results


# Distributed on a Ray cluster
def run_remote(arr):
    results = ray.get(
        [bubble_sort_distributed.remote(arr) for _ in range(os.cpu_count())]
    )
    return results


if __name__ == "__main__":
    ray.init(address='ray://localhost:10001')
    A = np.random.randint(0, 100, 1000)
    print("local run")
    cProfile.run("run_local(A)")
    print("remote run")
    cProfile.run("run_remote(A)")
    ray.shutdown()
