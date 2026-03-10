def powtwo(n):
    for i in range(n + 1):
        yield 2 ** i


n = int(input())
for power in powtwo(n):
    print(power, end=" ")