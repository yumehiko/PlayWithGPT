

from typing import List

def fibonacci(n: int, cache: List[int] = [0, 1]) -> int:
    if n < len(cache):
        return cache[n]
    else:
        res = fibonacci(n-1) + fibonacci(n-2)
        cache.append(res)
        return res

if __name__ == "__main__":
    for i in range(10):
        print(fibonacci(i))