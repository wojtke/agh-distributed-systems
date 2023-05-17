# 3.3 Take a look on implement parralel Pi computation
# based on https://docs.ray.io/en/master/ray-core/examples/highly_parallel.html
#
# Implement calculating pi as a combination of actor (which keeps the
# state of the progress of calculating pi as it approaches its final value)
# and a task (which computes candidates for pi)

import random
import time

import ray


@ray.remote
def pi4_sample(sample_count: int, pi_calculator):
    in_count = 0
    for _ in range(sample_count):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1:
            in_count += 1

    pi_calculator.add_sample.remote(in_count, sample_count)


@ray.remote
class PiCalculator:
    """Actor that keeps the state of the progress of calculating pi."""

    def __init__(self):
        self.numerator = 0
        self.denominator = 0

    def add_sample(self, in_count: int, sample_count: int):
        """Add a sample to the state of the actor."""
        self.numerator += in_count
        self.denominator += sample_count

    def get_cur_pi(self) -> float:
        """Return the current value of pi."""
        return 4 * self.numerator / self.denominator if self.denominator > 0 else -1


NUM_SAMPLES = 1_000_000
NUM_TASKS = 1_000

if __name__ == "__main__":
    ray.init(address='ray://localhost:10001')

    pi_calculator = PiCalculator.remote()
    task_refs = [pi4_sample.remote(NUM_SAMPLES, pi_calculator) for _ in range(NUM_TASKS)]

    while True:
        time.sleep(1)
        print(ray.get(pi_calculator.get_cur_pi.remote()))
