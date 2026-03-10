a = int(input())
b = list(map(int, input().split()))
b = sorted(b, reverse=True)
for i in range(len(b)):
    print(b[i], end=' ')