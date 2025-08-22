import ray
ray.init()

@ray.remote
def f(x):
    return x * x
if __name__ == "__main__":


    futures = [f.remote(i) for i in range(4)]
    print(ray.get(futures)) # [0, 1, 4, 9]