a = int(input())
b = list(map(int, input().split()))
g = 0
for x in b:
    count = 0
    for j in range(0, a):
        if b[j] == x:
            count += 1
    if count > g or (count == g and x < m):
        g = count
        m = x
print(m)