def cd(n):
    for num in range(n, -1, -1):
        yield num

n = int(input())

for num in cd(n):
    print(num)