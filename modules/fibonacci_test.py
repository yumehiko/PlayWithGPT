
# generate first 10 Fibonacci numbers
fib = [0, 1]
for i in range(2, 10):
    fib.append(fib[i-1] + fib[i-2])

# write the Fibonacci numbers into "fibonacci_test.py" file
with open("fibonacci_test.py", "w") as f:
    f.write("fibonacci_numbers = " + str(fib))
