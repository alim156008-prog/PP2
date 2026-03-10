a = int(input())
b = input().split()
m = int(b[0])
index = 0
for i in range(1, a):
    if m < int(b[i]):
        m = int(b[i])
        index = i
print(index + 1 )
