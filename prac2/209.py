a = int(input())
b = list(map(int, input().split()))
miv = min(b)
mav = max(b)
for i in range(len(b)):
    if b[i] == mav:
        b[i] = miv
for i in range(len(b)):
    print(b[i], end=' ')