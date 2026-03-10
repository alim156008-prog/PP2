a = int(input())
num = [input() for _ in range(a)]
f = {}
for n in num:
    f[n] = f.get(n, 0) + 1
count = 0
for v in f.values():
    if v == 3:
        count += 1
print(count)