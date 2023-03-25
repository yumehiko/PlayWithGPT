
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    else:
        return (fibonacci(n-1) + fibonacci(n-2))

# フィボナッチ数列を10個表示するために、forループを使用する
for i in range(10):
    print(fibonacci(i))
