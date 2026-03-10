def cyclil(lst, k):
    for _ in range(k):
        for item in lst:
            yield item


lst = input().split()
k = int(input())

for v in cyclil(lst, k):
    print(v, end=" ")