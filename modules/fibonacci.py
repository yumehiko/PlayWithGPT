

def fibonacci(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    else:
        memo[n] = fibonacci(n-1) + fibonacci(n-2)
        return memo[n]

fibonacci_sequence = []
for i in range(10):
    fibonacci_sequence.append(fibonacci(i))

print(fibonacci_sequence)