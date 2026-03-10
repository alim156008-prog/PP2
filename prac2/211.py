a = list(map(int, input().split()))
b = list(map(int, input().split()))
b[a[1]-1:a[2]] = reversed(b[a[1]-1:a[2]])
print(*b , end=' ')
    