n = int(input())
arr = list(map(int, input().split()))

s = set()

for x in arr:
    if x in s:
        print("NO")
    else:
        print("YES")
        s.add(x)