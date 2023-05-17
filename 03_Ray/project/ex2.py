# Exercise: Create large lists and python dictionaries, put them in object store. Write a Ray task to process them.

import cProfile

import ray


@ray.remote
def process_list(lst):
    new = [i * i for i in lst]
    print(new)
    return new


@ray.remote
def process_dict(dct):
    new = {k: int(v) + 1 for k, v in dct.items()}
    print(new)
    return new


@ray.remote
def process_dict_with_lists(dwl):
    new = {k: [j * j for j in ray.get(v)] for k, v in dwl.items()}
    print(new)
    return new


if __name__ == "__main__":
    ray.init(address='ray://localhost:10001')

    big_list = [i for i in range(100_000)]
    big_dict = {i: str(i) * 5 for i in range(100_000)}

    big_list_ref = ray.put(big_list)
    big_dict_ref = ray.put(big_dict)

    dict_with_lists = {i: ray.put([i for _ in range(100)]) for i in range(10)}

    print("Processing list")
    cProfile.run("process_list.remote(big_list_ref)")
    print("Processing dict")
    cProfile.run("process_dict.remote(big_dict_ref)")
    print("Processing dict with lists")
    cProfile.run("process_dict_with_lists.remote(dict_with_lists)")

    ray.shutdown()
