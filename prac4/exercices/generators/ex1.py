def squares(n):
    for i in range(n + 1):
        yield i * i

for num in squares(5):
    print(num)