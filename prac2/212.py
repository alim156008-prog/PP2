a = int (input())
b = list(map(int, input().split()))
for i in range(0,a):
    print(b[i]**2, end=' ')
    