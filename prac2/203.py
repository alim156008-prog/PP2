a = int(input())
b = input().split()
c = 0
for i in range(0, len(b)):
    c += int(b[i])
print(c)