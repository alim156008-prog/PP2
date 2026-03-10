n = int(input())
arr = [input() for _ in range(n)]

f = {}
for i, s in enumerate(arr):
    if s not in f:
        f[s] = i + 1 
for s in sorted(f.keys()):
    print(s, f[s])
