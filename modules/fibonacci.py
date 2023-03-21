def fibonacci(n):
    if n <= 1:
        return n
    else:
        return(fibonacci(n-1) + fibonacci(n-2))

fibonacci_sequence = []
for i in range(10):
    fibonacci_sequence.append(fibonacci(i))

print(fibonacci_sequence)
