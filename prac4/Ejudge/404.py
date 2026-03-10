def squares(a, b):
    for num in range(a, b + 1):
        yield num ** 2

n = input().split()
for value in squares(int(n[0]), int(n[1])):
    print(value)